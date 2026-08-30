PROJECT := scientific_computing_2026
BUILD := build
DIST := dist

.PHONY: all pdf clean

all: pdf

pdf:
	mkdir -p $(BUILD) $(DIST)
	tectonic -X compile main.tex --outdir $(BUILD) --keep-logs
	cp $(BUILD)/main.pdf $(DIST)/$(PROJECT).pdf

clean:
	rm -rf $(BUILD)
