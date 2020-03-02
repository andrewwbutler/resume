# Makefile to build PDF and Markdown resume from YAML.
#
# Brandon Amos <http://bamos.io> and Ellis Michael <http://ellismichael.com>

TEMPLATES=$(shell find templates -type f)

BUILD_DIR=build
BUILD_DEPS=$(TEMPLATES) resume.yaml generate.py | $(BUILD_DIR)
PDF=$(BUILD_DIR)/resume.pdf
MD=$(BUILD_DIR)/resume.md
HTML=$(BUILD_DIR)/resume.html
TXT=$(BUILD_DIR)/resume.txt

GENERATE_CMD=./generate.py -b publications.yaml resume.yaml

define build_latex
	latexmk -pdf -cd- -quiet -jobname=$(BUILD_DIR)/resume $(BUILD_DIR)/resume || latexmk -pdf -cd- -verbose -jobname=$(BUILD_DIR)/resume $(BUILD_DIR)/resume
	latexmk -c -cd $(BUILD_DIR)/resume
endef

.PHONY: all private viewpdf clean

all: $(PDF) $(MD) $(HTML)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(PDF) $(MD) $(HTML) $(TXT): $(BUILD_DEPS)
	$(GENERATE_CMD)
	$(call build_latex)

private: private.yaml $(BUILD_DEPS)
	$(GENERATE_CMD) private.yaml
	$(call build_latex)

viewpdf: $(PDF)
	xdg-open $(PDF)

clean:
	rm -rf $(BUILD_DIR)
