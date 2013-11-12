SHELL:=/bin/bash -e
export SHELLOPTS=pipefail
image_files = $(foreach i, 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15, img/example_$(i).png)

.PHONY = clean images

all: bin/quick_plot

bin/%: src/%.py
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

images: all $(image_files)

img/example_01.png: example/data_2d_1.txt
	bin/quick_plot $^ --mode scatter --markersize 7.0 --out_format png --out $@.tmp --title '2D scatter data from example/data_2d_1.txt' --xlabel 'The x-axis' --ylabel 'The y-axis' --no_legend
	mv $@.tmp.png $@

img/example_02.png: example/data_2d_1.txt example/data_2d_2.txt
	bin/quick_plot $^ --mode scatter --markersize 7.0 --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_03.png: example/data_2d_3.txt example/data_2d_4.txt
	bin/quick_plot $^ --mode line --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_04.png: example/data_2d_5.txt example/data_2d_6.txt example/data_2d_7.txt
	bin/quick_plot $^ --mode line --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_05.png: example/data_1d_1.txt example/data_1d_2.txt
	bin/quick_plot $^ --mode bar --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_06.png: example/data_1d_1.txt example/data_1d_2.txt
	bin/quick_plot $^ --mode tick --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_07.png: example/data_1d_1.txt example/data_1d_2.txt
	bin/quick_plot $^ --mode point --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_08.png: example/data_1d_1.txt example/data_1d_2.txt
	bin/quick_plot $^ --mode point --jitter --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_09.png: example/data_1d_3.txt example/data_1d_4.txt example/data_1d_5.txt
	bin/quick_plot $^ --mode hist --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_10.png: example/data_2d_8.txt
	bin/quick_plot $^ --mode scatter --markersize 5.0 --out_format png --out $@.tmp
	mv $@.tmp.png $@

img/example_11.png: example/data_2d_8.txt
	bin/quick_plot $^ --mode scatter --markersize 5.0 --out_format png --out $@.tmp --alpha 0.1
	mv $@.tmp.png $@

img/example_12.png: example/data_1d_7.txt
	bin/quick_plot $^ --mode density --out_format png --out $@.tmp --title 'data_2d_8.txt x marginal'
	mv $@.tmp.png $@

img/example_13.png: example/data_1d_8.txt
	bin/quick_plot $^ --mode density --out_format png --out $@.tmp --title 'data_2d_8.txt y marginal'
	mv $@.tmp.png $@

img/example_14.png: example/data_2d_8.txt
	bin/quick_plot $^ --mode contour --out_format png --out $@.tmp --title 'A hard example for a contour plot'
	mv $@.tmp.png $@

img/example_15.png: example/data_2d_9.txt
	bin/quick_plot $^ --mode contour --out_format png --out $@.tmp --title 'An easier example for a contour plot'
	mv $@.tmp.png $@

clean:
	rm -rf bin/
