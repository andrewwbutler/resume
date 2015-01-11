#!/usr/bin/env python

"""Generates LaTeX, markdown, and plaintext copies of my resume."""

__author__ = [
    'Brandon Amos <http://bamos.io>',
    'Ellis Michael <http://ellismichael.com>',
]

import argparse
import re
import yaml

from copy import copy
from datetime import date
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class RenderContext(object):
    DEFAULT_SECTION = 'items'

    def __init__(self, output_file, templates_dir, base_template, file_ending,
            jinja_options, replacements):
        self._file_ending = file_ending
        self._replacements = replacements

        self._output_file = output_file
        self._base_template = base_template

        self._jinja_options = jinja_options.copy()
        self._jinja_options['loader'] = FileSystemLoader(
            searchpath=templates_dir)
        self._jinja_env = Environment(**self._jinja_options)

    def make_replacements(self, yaml_data):
        # Make a copy of the yaml_data so that this function is idempotent
        yaml_data = copy(yaml_data)

        if isinstance(yaml_data, str):
            for o, r in self._replacements:
                yaml_data = re.sub(o, r, yaml_data)

        elif isinstance(yaml_data, dict):
            for k, v in yaml_data.items():
                yaml_data[k] = self.make_replacements(v)

        elif isinstance(yaml_data, list):
            for idx, item in enumerate(yaml_data):
                yaml_data[idx] = self.make_replacements(item)

        return yaml_data

    def render_template(self, template_name, yaml_data):
        return self._jinja_env.get_template(template_name).render(yaml_data)

    def write_to_outfile(self, output_data):
        with open(self._output_file, 'w') as out:
            out.write(output_data)

    def process_resume(self, yaml_data):
        # Make the replacements first on the yaml_data
        yaml_data = self.make_replacements(yaml_data)

        body = ''
        for section_data in yaml_data['sections']:
            section_type = (self.DEFAULT_SECTION if not 'type' in section_data
                else section_data['type'])
            section_template = section_type + self._file_ending

            # Revert to default section if template unavailable
            try:
                self._jinja_env.get_template(section_template)
            except TemplateNotFound:
                section_template = self.DEFAULT_SECTION + self._file_ending

            # TODO: fix tablist and groups
            if section_type == 'tablist':
                groups = []
                items_temp = list(section_data['items'])
                while len(items_temp):
                    g = []
                    for _ in range(2):
                        try:
                            g.append(items_temp.pop(0))
                        except IndexError:
                            break
                    groups.append(tuple(g))

                section_data['groups'] = groups

            rendered_section = self.render_template(
                section_template, section_data)
            body += rendered_section + '\n\n'

        yaml_data['body'] = body
        yaml_data['today'] = date.today().strftime("%B %d, %Y")
        rendered_resume = self.render_template(self._base_template, yaml_data)

        self.write_to_outfile(rendered_resume)


LATEX_CONTEXT = RenderContext(
    'build/resume.tex',
    'templates/latex/',
    'resume.tex',
    '.tex',
    dict(
        block_start_string='~<',
        block_end_string='>~',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<#',
        comment_end_string='#>',
        trim_blocks=True,
        lstrip_blocks=True
    ),
    []
)

MARKDOWN_CONTEXT = RenderContext(
    'build/resume.md',
    'templates/markdown/',
    'resume.md',
    '.md',
    dict(
        trim_blocks=True,
        lstrip_blocks=True
    ),
    [
        (r'\\ ', '&nbsp;'),                # LaTeX spaces to &nbsp;
        (r'\\textbf{(.*)}', r'**\1**'),    # Bold text
        (r'\\TeX', r'TeX')                 # \TeX to boring old TeX
    ]
)


def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description=
        'Generates LaTeX and Markdown resumes from data in YAML files.')
    parser.add_argument('yamls', metavar='YAML_FILE', nargs='+',
        help='the YAML files that contain the resume details, in order of '
             'increasing precedence')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--latex', action='store_true',
        help='only generate LaTeX resume')
    group.add_argument('-m', '--markdown', action='store_true',
        help='only generate Markdown resume')
    args = parser.parse_args()

    resume_data = {}
    for yaml_file in args.yamls:
        with open(yaml_file) as f:
            resume_data.update(yaml.load(f))

    if not args.markdown:
        LATEX_CONTEXT.process_resume(resume_data)
    if not args.latex:
        MARKDOWN_CONTEXT.process_resume(resume_data)

if __name__ == "__main__":
    main()
