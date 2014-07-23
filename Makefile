# Makefile to build PDF, Markdown, and plaintext CV from YAML.
#
# Brandon Amos <http://bamos.io> and Ellis Michael <http://ellismichael.com>

BLOG_DIR=$(HOME)/ellismichael.com
TEMPLATE_DIR=templates
BUILD_DIR=build

all: $(BUILD_DIR)/resume.pdf

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/resume.tex: $(BUILD_DIR) $(TEMPLATE_DIR)/latex/* generate.py
	python generate.py

$(BUILD_DIR)/resume.pdf: $(BUILD_DIR) $(BUILD_DIR)/resume.tex
	latexmk -pdf -cd- -quiet -jobname=$(BUILD_DIR)/resume $(BUILD_DIR)/resume
	latexmk -c -cd $(BUILD_DIR)/resume
	gnome-open $(BUILD_DIR)/resume.pdf

.PHONY: stage
stage: $(BUILD_DIR)/resume.pdf
	cp $(BUILD_DIR)/resume.pdf $(BLOG_DIR)/assets/resume.pdf

.PHONY: jekyll
jekyll: stage
	cd $(BLOG_DIR) && jekyll server
	google-chrome http://localhost:4000/assets/resume.pdf

push: stage
	git -C $(BLOG_DIR) add $(BLOG_DIR)/data/cv.pdf
	git -C $(BLOG_DIR) add $(BLOG_DIR)/cv.md
	git -C $(BLOG_DIR) commit -m "Update vitae."
	git -C $(BLOG_DIR) push

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)
