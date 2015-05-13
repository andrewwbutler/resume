About
-----
This repo contains the source I use to automatically generate [my resume]
(http://ellismichael.com/resume/) as a webpage and PDF from YAML input.

It was forked from [bamos/cv](https://github.com/bamos/cv) and has been heavily
modified to fit my use case. Many of the features that were in the original repo
have been removed to be added back in at a later date if/when I need them. See
the original repo for details about the choices of YAML, LaTeX, and Markdown.


How to run
----------
The dependencies are included in `requirements.txt` and can be installed using
`pip` with `pip install -r requirements.txt`. I recommend doing this inside a
`virtualenv`.

`make` will call generate.py and build the LaTeX documents with latexmk.

The Makefile can also open the compiled PDF with `make viewpdf`.


What to Modify
--------------
All that you need to modify is `resume.yaml` (and of course the image file to be
included in the top right corner of the resume). You should also look through
the template files to make sure there isn't any special-case code that needs to
be modified.

Of course, you'll probably want to modify the templates as well. That is left as
an exercise for the reader.

If you use Sublime Text 2, `resume.sublime-project` can be easily modified to
work on your system and make the `PyLinter` plugin recognize a `virtualenv`.

### Warnings
1. Strings in `resume.yaml` should be LaTeX (though, the actual LaTeX formatting
   should be in the left in the templates as much as possible).
2. If you do include any new LaTeX commands, make sure that one of the
   `REPLACEMENTS` in `generate.py` converts them properly.
3. The LaTeX templates use modified Jinja delimiters to avoid overlaps with
   normal LaTeX. See `generate.py` for details.


License
-------
All of bamos' original work is distributed under the MIT license found in
`LICENSE-bamos.mit`.

My modifications are distributed under the MIT license found in
`LICENSE-emichael.mit`.
