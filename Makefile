# Makefile to build PDF and Markdown resume from YAML.
#
# Brandon Amos <http://bamos.io> and Ellis Michael <http://ellismichael.com>

WEBSITE_DIR=$(HOME)/Projects/andrewwbutler.github.io

TEMPLATES=$(shell find templates -type f)

BUILD_DIR=build
TEX=$(BUILD_DIR)/resume.tex
PDF=$(BUILD_DIR)/resume.pdf
MD=$(BUILD_DIR)/resume.md
HTML=$(BUILD_DIR)/resume.html

GENERATE_CMD=./generate.py -b publications.yaml

ifneq ("$(wildcard resume.hidden.yaml)","")
	YAML_FILES = resume.yaml resume.hidden.yaml
else
	YAML_FILES = resume.yaml
endif

.PHONY: all public viewpdf clean

all: $(PDF) $(MD)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

public: $(TEMPLATES) $(YAML_FILES) generate.py | $(BUILD_DIR)
	$(GENERATE_CMD) resume.yaml

$(TEX) $(MD) $(HTML): $(TEMPLATES) $(YAML_FILES) generate.py | $(BUILD_DIR)
	$(GENERATE_CMD) $(YAML_FILES)

$(PDF): $(TEX)
	latexmk -pdf -cd- -quiet -jobname=$(BUILD_DIR)/resume $(BUILD_DIR)/resume || latexmk -pdf -cd- -verbose -jobname=$(BUILD_DIR)/resume $(BUILD_DIR)/resume
	latexmk -c -cd $(BUILD_DIR)/resume

viewpdf: $(PDF)
	gnome-open $(PDF)

stage: $(PDF) $(MD)
	cp $(PDF) $(WEBSITE_DIR)/assets/resume.pdf
	cp $(HTML) $(WEBSITE_DIR)/resume.html

jekyll: stage
	cd $(WEBSITE_DIR) && bundle exec jekyll serve

push: stage
	git -C $(WEBSITE_DIR) add $(WEBSITE_DIR)/assets/resume.pdf
	git -C $(WEBSITE_DIR) add $(WEBSITE_DIR)/resume.html
	git -C $(WEBSITE_DIR) commit -m "Update resume."
	git -C $(WEBSITE_DIR) push

clean:
	rm -rf $(BUILD_DIR)
