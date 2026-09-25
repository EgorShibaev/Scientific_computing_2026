PROJECT := scientific_computing_2026
BUILD := build
DIST := dist

.PHONY: all pdf lecture-04-slides clean

all: pdf

pdf:
	mkdir -p $(BUILD) $(DIST)
	tectonic -X compile main.tex --outdir $(BUILD) --keep-logs
	cp $(BUILD)/main.pdf $(DIST)/$(PROJECT).pdf

lecture-04-slides:
	mkdir -p $(BUILD)/lecture-04-slides
	tectonic -X compile presentations/lecture-04/lecture-04.tex --outdir $(BUILD)/lecture-04-slides --keep-logs
	cp $(BUILD)/lecture-04-slides/lecture-04.pdf presentations/lecture-04/lecture-04.pdf

clean:
	rm -rf $(BUILD)
