SHELL:=/bin/bash -e
export SHELLOPTS=pipefail
image_files = $(foreach i, 1 2 3 4 5 6 7 8 9, img/example_$(i).png)

.PHONY = clean images

all: bin/quick_plot

bin/%: src/%.py
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

images: all $(image_files)

img/example_1.png: example/data_2d_1.txt
	bin/quick_plot $^ --mode scatter --markersize 3.0 --out_format png --out $@.tmp --title '2D scatter data from example/data_2d_1.txt' --xlabel 'The x-axis' --ylabel 'The y-axis' --no_legend
	mv $@.tmp.png $@

img/example_2.png: example/data_2d_1.txt example/data_2d_2.txt
	bin/quick_plot $^ --mode scatter --markersize 3.0 --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_3.png: example/data_2d_3.txt example/data_2d_4.txt
	bin/quick_plot $^ --mode line --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_4.png: example/data_2d_5.txt example/data_2d_6.txt example/data_2d_7.txt
	bin/quick_plot $^ --mode line --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_5.png: example/data_1d_1.txt example/data_1d_2.txt
	bin/quick_plot $^  --mode bar --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_6.png: example/data_1d_1.txt example/data_1d_2.txt
	bin/quick_plot $^ --mode tick --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_7.png: example/data_1d_1.txt example/data_1d_2.txt
	bin/quick_plot $^ --mode point --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_8.png: example/data_1d_1.txt example/data_1d_2.txt
	bin/quick_plot $^ --mode point --jitter --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_9.png: example/data_1d_3.txt example/data_1d_4.txt example/data_1d_5.txt
	bin/quick_plot $^  --mode hist --out_format png --out $@.tmp
	mv $@.tmp.png $@

clean:
	rm -rf bin/
