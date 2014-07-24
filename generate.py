#!/usr/bin/env python

# Generates LaTeX, markdown, and plaintext copies of my CV.
#
# Brandon Amos <http://bamos.io> and Ellis Michael <http://ellismichael.com>
# 2014.7.23

import re
import yaml

from datetime import date
from jinja2 import Environment, FileSystemLoader


REPLACEMENTS = [
    (r'\\ ', '&nbsp;'),
    (r'\\textbf{(.*)}', r'**\1**'),
    (r'\\TeX', r'TeX')
]

YAML_FILE = 'resume.yaml'

LATEX_OUTPUT_FILE = 'build/resume.tex'
LATEX_TEMPLATES_DIR = 'templates/latex/'
LATEX_TEMPLATE = 'resume.tex'
LATEX_SECTION_TEMPLATES = {
    'normal': 'section.tex',
    'items': 'itemsection.tex',
    'education': 'educationsection.tex',
    'experience': 'experiencesection.tex',
    'tablist': 'tablistsection.tex',
}
latex_template_env = Environment(
    loader=FileSystemLoader(searchpath=LATEX_TEMPLATES_DIR),
    block_start_string='~{',
    block_end_string='}~',
    variable_start_string='~{{',
    variable_end_string='}}~',
    comment_start_string='~{#',
    comment_end_string='#}~',
    trim_blocks=True,
    lstrip_blocks=True
)


MARKDOWN_OUTPUT_FILE = 'build/resume.md'
MARKDOWN_TEMPLATES_DIR = 'templates/markdown/'
MARKDOWN_TEMPLATE = 'resume.md'
MARKDOWN_SECTION_TEMPLATES = {
    'normal': 'section.md',
    'items': 'itemsection.md',
    'tablist': 'itemsection.md',
    'education': 'educationsection.md',
    'experience': 'experiencesection.md',
}

markdown_template_env = Environment(
    loader=FileSystemLoader(searchpath=MARKDOWN_TEMPLATES_DIR),
    trim_blocks=True,
    lstrip_blocks=True
)


with open(YAML_FILE) as f:
    yaml_contents = yaml.load(f)


def latexToMd(s):
    if isinstance(s, str):
        for o, r in REPLACEMENTS:
            s = re.sub(o, r, s)
    elif isinstance(s, dict):
        for k, v in s.items():
            s[k] = latexToMd(v)
    elif isinstance(s, list):
        for idx, item in enumerate(s):
            s[idx] = latexToMd(item)
    return s


def make_groups(l, size):
    groups = []
    l_temp = list(l)
    while len(l_temp):
        g = []
        for _ in range(size):
            try:
                g.append(l_temp.pop(0))
            except IndexError:
                break
        groups.append(tuple(g))
    return groups


def render_latex_section(title, section_type, data, row_size=2):
    template = latex_template_env.get_template(
        LATEX_SECTION_TEMPLATES[section_type])
    context = {}
    context['title'] = title

    if 'legend' in data:
        context['legend'] = data['legend']
    if 'items' in data:
        context['items'] = data['items']
    else:
        context['items'] = data

    if section_type == 'tablist':
        context['groups'] = make_groups(context['items'], row_size)
    elif section_type == 'normal':
        context['data'] = context['items']

    return template.render(context)


def render_markdown_section(title, section_type, data):
    template = markdown_template_env.get_template(
        MARKDOWN_SECTION_TEMPLATES[section_type])
    context = {}
    context['title'] = title

    if 'legend' in data:
        context['legend'] = data['legend']
    if 'items' in data:
        context['items'] = data['items']
    else:
        context['items'] = data

    if section_type == 'normal':
        context['data'] = context['items']

    return template.render(context)


def main():
    # LaTeX first...
    body = ''
    for section in yaml_contents['sections']:
        title = section['title']
        section_type = section['type']
        data = yaml_contents[title]

        if 'rowsize' in section:
            rendered_section = render_latex_section(
                title, section_type, data, section['rowsize'])
        else:
            rendered_section = render_latex_section(title, section_type, data)
        body += rendered_section + '\n\n'

    template = latex_template_env.get_template(LATEX_TEMPLATE)
    yaml_contents['body'] = body
    rendered_resume = template.render(yaml_contents)

    with open(LATEX_OUTPUT_FILE, 'w') as o:
        o.write(rendered_resume)

    # Now, Markdown
    body = ''
    for section in yaml_contents['sections']:
        title = section['title']
        section_type = section['type']
        data = latexToMd(yaml_contents[title])
        rendered_section = render_markdown_section(title, section_type, data)
        body += rendered_section + '\n\n'

    template = markdown_template_env.get_template(MARKDOWN_TEMPLATE)
    yaml_contents['today'] = date.today().strftime("%B %d, %Y")
    yaml_contents['body'] = body
    rendered_resume = template.render(yaml_contents)
    with open(MARKDOWN_OUTPUT_FILE, 'w') as o:
        o.write(rendered_resume)


if __name__ == "__main__":
    main()
