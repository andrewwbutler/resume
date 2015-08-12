#!/usr/bin/env python

"""Generates LaTeX, markdown, and plaintext copies of my resume."""

__author__ = [
    'Brandon Amos <http://bamos.io>',
    'Ellis Michael <http://ellismichael.com>',
]

import argparse
import os
import re
import yaml

from copy import copy
from git import Repo
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from time import localtime, strftime


class RenderContext(object):
    BUILD_DIR = 'build'
    TEMPLATES_DIR = 'templates'
    SECTIONS_DIR = 'sections'
    DEFAULT_SECTION = 'items'
    BASE_FILE_NAME = 'resume'

    def __init__(self, context_name, file_ending, jinja_options, replacements):
        self._file_ending = file_ending
        self._replacements = replacements

        context_templates_dir = os.path.join(self.TEMPLATES_DIR, context_name)

        self._output_file = os.path.join(
            self.BUILD_DIR, self.BASE_FILE_NAME + self._file_ending)
        self._base_template = self.BASE_FILE_NAME + self._file_ending

        self._context_type_name = context_name + 'type'

        self._jinja_options = jinja_options.copy()
        self._jinja_options['loader'] = FileSystemLoader(
            searchpath=context_templates_dir)
        self._jinja_options['undefined'] = StrictUndefined
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

    def _render_template(self, template_name, yaml_data):
        return self._jinja_env.get_template(template_name).render(yaml_data)

    @staticmethod
    def _make_double_list(items):
        groups = []
        items_temp = list(items)
        while len(items_temp):
            group = {}
            group['first'] = items_temp.pop(0)
            if len(items_temp):
                group['second'] = items_temp.pop(0)
            groups.append(group)
        return groups

    def render_resume(self, yaml_data):
        # Make the replacements first on the yaml_data
        yaml_data = self.make_replacements(yaml_data)

        body = ''
        for section_data in yaml_data['sections']:
            section_type = self.DEFAULT_SECTION
            if self._context_type_name in section_data:
                section_type = section_data[self._context_type_name]
            elif 'type' in section_data:
                section_type = section_data['type']

            if section_type == 'doubleitems':
                section_data['items'] = self._make_double_list(
                    section_data['items'])

            section_template_name = os.path.join(
                self.SECTIONS_DIR, section_type + self._file_ending)

            rendered_section = self._render_template(
                section_template_name, section_data)
            body += rendered_section.rstrip() + '\n\n\n'

        yaml_data['body'] = body
        # Grab the timestamp of the last commit
        timestamp = Repo().head.commit.committed_date
        yaml_data['generated'] = strftime("%B %d", localtime(timestamp))

        return self._render_template(
            self._base_template, yaml_data).rstrip() + '\n'

    def write_to_outfile(self, output_data):
        with open(self._output_file, 'w') as out:
            out.write(output_data)


LATEX_CONTEXT = RenderContext(
    'latex',
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
    'markdown',
    '.md',
    dict(
        trim_blocks=True,
        lstrip_blocks=True
    ),
    [
        (r'\\ ', ' '),                     # spaces
        (r'\\textbf{([^}]*)}', r'**\1**'), # bold text
        (r'\\textit{([^}]*)}', r'*\1*'),   # italic text
        (r'\\LaTeX', 'LaTeX'),             # \LaTeX to boring old LaTeX
        (r'\\TeX', 'TeX'),                 # \TeX to boring old TeX
        ('---', '-'),                      # em dash
        ('--', '-'),                       # en dash
        (r'``([^\']*)\'\'', r'"\1"'),      # quotes
    ]
)

HTML_CONTEXT = RenderContext(
    'html',
    '.html',
    dict(
        trim_blocks=True,
        lstrip_blocks=True
    ),
    [
        (r'\\ ', '&nbsp;'),                             # spaces
        (r'\\textbf{([^}]*)}', r'<strong>\1</strong>'), # bold
        (r'\\textit{([^}]*)}', r'<em>\1</em>'),         # italic
        (r'\\LaTeX', 'LaTeX'),                          # \LaTeX
        (r'\\TeX', 'TeX'),                              # \TeX
        ('---', '&mdash;'),                             # em dash
        ('--', '&ndash;'),                              # en dash
        (r'``([^\']*)\'\'', r'"\1"'),                   # quotes
    ]
)


def process_resume(context, yaml_data, preview):
    rendered_resume = context.render_resume(yaml_data)
    if preview:
        print rendered_resume
    else:
        context.write_to_outfile(rendered_resume)

def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description=
        'Generates HTML, LaTeX, and Markdown resumes from data in YAML files.')
    parser.add_argument('yamls', metavar='YAML_FILE', nargs='+',
        help='the YAML files that contain the resume details, in order of '
             'increasing precedence')
    parser.add_argument('-p', '--preview', action='store_true',
        help='prints generated resumes to stdout instead of writing to file')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--html', action='store_true',
        help='only generate HTML resume')
    group.add_argument('-l', '--latex', action='store_true',
        help='only generate LaTeX resume')
    group.add_argument('-m', '--markdown', action='store_true',
        help='only generate Markdown resume')
    args = parser.parse_args()

    yaml_data = {}
    for yaml_file in args.yamls:
        with open(yaml_file) as f:
            yaml_data.update(yaml.load(f))

    if args.html or args.latex or args.markdown:
        if args.html:
            process_resume(HTML_CONTEXT, yaml_data, args.preview)
        elif args.latex:
            process_resume(LATEX_CONTEXT, yaml_data, args.preview)
        elif args.markdown:
            process_resume(MARKDOWN_CONTEXT, yaml_data, args.preview)
    else:
        process_resume(HTML_CONTEXT, yaml_data, args.preview)
        process_resume(LATEX_CONTEXT, yaml_data, args.preview)
        process_resume(MARKDOWN_CONTEXT, yaml_data, args.preview)


if __name__ == "__main__":
    main()
