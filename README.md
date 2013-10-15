# quick_plot

**quick_plot** is a Python script that uses matplotlib to create simple visualizations of data from the command line.

## Author
[Dent Earl](https://github.com/dentearl/)

## Dependencies
* Python 2.7
* [matplotlib](http://matplotlib.sourceforge.net/) 1.1.0

## Installation
1. Download the package.
2. <code>cd</code> into the directory.
3. Type <code>make</code>.

## Input file format
The input file may contain comment lines (lines that start with #). Files may contain one or more columns (white space delimited) of numbers

## Usage
    usage: quick_plot input_file1 input_file2 ... [options]

    positional arguments:
    files                 files to plot
    optional arguments:
    -h, --help            show this help message and exit
    --out OUT             path/filename where figure will be created. No extension needed.
                          default=my_plot
    --mode MODE           plotting mode. may be in (line, scatter, column, bar, hist, tick, point)
                          default=line
    --alpha ALPHA         alpha value for markers in --mode scatter
    --dot_size MARKERSIZE, --markersize MARKERSIZE
                          value for markers in --mode scatter
    --lineWidth LINEWIDTH
                          Line width for the plot. default=2.0
    --logy                Put the y-axis into log. default=False
    --logx                Put the x-axis into log. default=False
    --title TITLE         Plot title.
    --xlabel XLABEL       X-axis label.
    --ylabel YLABEL       Y-axis label.
    --height HEIGHT       height of image, in inches. default=4.0
    --width WIDTH         width of image, in inches. default=9.0
    --dpi DPI             dots per inch of raster outputs, i.e. if --outFormat is all or png.
                          default=300
    --out_format OUT_FORMAT
                          output format [pdf|png|eps|all]. default=pdf
    --no_legend           Turns off the filename / color legend. Helpful for large numbers of files.
    --regression          turn on a simple linear regression line
    --jitter              turn on jitter for certain plotting modes


## Examples
    bin/quick_plot example/metrics.txt --outFormat png --out img/example_1.png
![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_1.png)

