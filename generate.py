#!/usr/bin/env python3

# Generates LaTeX, markdown, and plaintext copies of my CV.
#
# Brandon Amos <http://bamos.io> and Ellis Michael <http://ellismichael.com>
# 2014.7.23

import re
import yaml

from jinja2 import Environment, FileSystemLoader


YAML_FILE = 'resume.yaml'

LATEX_OUTPUT_FILE = 'build/resume.tex'
LATEX_TEMPLATES_DIR = './templates/latex/'
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

with open(YAML_FILE) as f:
    yaml_contents = yaml.load(f)


def latexToMd(s):
    if isinstance(s, str):
        s = s.replace(r'\\', '\n\n')
        s = s.replace(r'\it', '')
        s = s.replace('--', '-')
        s = s.replace('``', '"')
        s = s.replace("''", '"')
        s = s.replace(r"\LaTeX", "LaTeX")
        s = s.replace(r"\#", "#")
        s = s.replace(r"\&", "&")
        s = re.sub(r'\\[hv]space\*?\{[^}]*\}', '', s)
        s = s.replace(r"*", r"\*")
        s = re.sub(r'\{ *\\bf *([^\}]*)\}', r'**\1**', s)
        s = re.sub(r'\{([^\}]*)\}', r'\1', s)
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


def render_tex_section(title, section_type, data, row_size=2):
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


def main():
    body = ''
    for section in yaml_contents['sections']:
        title = section['title']
        section_type = section['type']
        data = yaml_contents[title]

        if 'rowsize' in section:
            rendered_section = render_tex_section(
                title, section_type, data, section['rowsize'])
        else:
            rendered_section = render_tex_section(title, section_type, data)
        body += rendered_section + '\n\n'

    template = latex_template_env.get_template(LATEX_TEMPLATE)
    yaml_contents['body'] = body
    rendered_resume = template.render(yaml_contents)

    with open(LATEX_OUTPUT_FILE, 'w') as o:
        o.write(rendered_resume)


if __name__ == "__main__":
    main()
