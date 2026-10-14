PROJECT := scientific_computing_2026
BUILD := build
DIST := dist

.PHONY: all pdf lecture-03-slides lecture-04-slides lecture-05-slides lecture-06-slides seminar-01 clean

all: pdf

pdf:
	mkdir -p $(BUILD) $(DIST)
	tectonic -X compile main.tex --outdir $(BUILD) --keep-logs
	cp $(BUILD)/main.pdf $(DIST)/$(PROJECT).pdf

lecture-03-slides:
	mkdir -p $(BUILD)/lecture-03-slides
	tectonic -X compile presentations/lecture-03/lecture-03.tex --outdir $(BUILD)/lecture-03-slides --keep-logs
	cp $(BUILD)/lecture-03-slides/lecture-03.pdf presentations/lecture-03/lecture-03.pdf

lecture-04-slides:
	mkdir -p $(BUILD)/lecture-04-slides
	tectonic -X compile presentations/lecture-04/lecture-04.tex --outdir $(BUILD)/lecture-04-slides --keep-logs
	cp $(BUILD)/lecture-04-slides/lecture-04.pdf presentations/lecture-04/lecture-04.pdf

lecture-05-slides:
	mkdir -p $(BUILD)/lecture-05-slides
	tectonic -X compile presentations/lecture-05/lecture-05.tex --outdir $(BUILD)/lecture-05-slides --keep-logs
	cp $(BUILD)/lecture-05-slides/lecture-05.pdf presentations/lecture-05/lecture-05.pdf

lecture-06-slides:
	mkdir -p $(BUILD)/lecture-06-slides
	tectonic -X compile presentations/lecture-06/lecture-06.tex --outdir $(BUILD)/lecture-06-slides --keep-logs
	cp $(BUILD)/lecture-06-slides/lecture-06.pdf presentations/lecture-06/lecture-06.pdf

seminar-01:
	mkdir -p $(BUILD)/seminar-01
	tectonic -X compile seminars/seminar_01_problems.tex --outdir $(BUILD)/seminar-01 --keep-logs
	cp $(BUILD)/seminar-01/seminar_01_problems.pdf seminars/seminar_01_problems.pdf

clean:
	rm -rf $(BUILD)
