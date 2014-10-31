# Makefile to build PDF and Markdown resume from YAML.
#
# Brandon Amos <http://bamos.io> and Ellis Michael <http://ellismichael.com>

BLOG_DIR=$(HOME)/ellismichael.com
TEMPLATE_DIR=templates
BUILD_DIR=build

TEX=$(BUILD_DIR)/resume.tex
PDF=$(BUILD_DIR)/resume.pdf
MD=$(BUILD_DIR)/resume.md

.PHONY: all viewpdf stage jekyll push clean

all: $(PDF) $(MD)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(TEX) $(MD): $(BUILD_DIR) $(TEMPLATE_DIR)/latex/* $(TEMPLATE_DIR)/markdown/* \
							resume.yaml generate.py
	python generate.py

$(PDF): $(BUILD_DIR) $(TEX)
	latexmk -pdf -cd- -quiet -jobname=$(BUILD_DIR)/resume $(BUILD_DIR)/resume
	latexmk -c -cd $(BUILD_DIR)/resume

viewpdf: $(PDF)
	gnome-open $(PDF)

stage: $(PDF) $(MD)
	cp $(PDF) $(BLOG_DIR)/assets/resume.pdf
	cp $(MD) $(BLOG_DIR)/resume.md

jekyll: stage
	cd $(BLOG_DIR) && jekyll server

push: stage
	git -C $(BLOG_DIR) add $(BLOG_DIR)/assets/resume.pdf
	git -C $(BLOG_DIR) add $(BLOG_DIR)/resume.md
	git -C $(BLOG_DIR) commit -m "Update resume"
	git -C $(BLOG_DIR) push

clean:
	rm -rf $(BUILD_DIR)
