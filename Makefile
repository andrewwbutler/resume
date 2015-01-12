# Makefile to build PDF and Markdown resume from YAML.
#
# Brandon Amos <http://bamos.io> and Ellis Michael <http://ellismichael.com>

BLOG_DIR=$(HOME)/ellismichael.com

TEMPLATES=$(shell find templates -type f)

BUILD_DIR=build
TEX=$(BUILD_DIR)/resume.tex
PDF=$(BUILD_DIR)/resume.pdf
MD=$(BUILD_DIR)/resume.md
HTML=$(BUILD_DIR)/resume.html

ifneq ("$(wildcard resume.hidden.yaml)","")
	YAML_FILES = resume.yaml resume.hidden.yaml
else
	YAML_FILES = resume.yaml
endif

.PHONY: all public viewpdf stage jekyll push clean

all: $(PDF) $(MD)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

public: $(BUILD_DIR) $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py resume.yaml

$(TEX) $(MD) $(HTML): $(BUILD_DIR) $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py $(YAML_FILES)

$(PDF): $(TEX)
	latexmk -pdf -cd- -quiet -jobname=$(BUILD_DIR)/resume $(BUILD_DIR)/resume
	latexmk -c -cd $(BUILD_DIR)/resume

viewpdf: $(PDF)
	gnome-open $(PDF)

stage: $(PDF) $(HTML)
	cp $(PDF) $(BLOG_DIR)/assets/resume.pdf
	cp $(HTML) $(BLOG_DIR)/resume.html

jekyll: stage
	cd $(BLOG_DIR) && jekyll server

push: stage
	git -C $(BLOG_DIR) add $(BLOG_DIR)/assets/resume.pdf
	git -C $(BLOG_DIR) add $(BLOG_DIR)/resume.md
	git -C $(BLOG_DIR) commit -m "Update resume"
	git -C $(BLOG_DIR) push

clean:
	rm -rf $(BUILD_DIR)
