# quick_plot

**quick_plot** is a python script that uses matplotlib to create simple visualizations of data from the command line.

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
    usage: quick_plot file1 file2 file3... [options]

    quick_plot is a tool to produce quick plots. col1 of input file is x value col2 is y
    value. If the --mode is column/bar/hist then only col1 is used.

    positional arguments:
      files                 files to plot

    optional arguments:
      -h, --help            show this help message and exit
      --out OUT             path/filename where figure will be created. No extension
                            needed. default=my_plot
      --mode MODE           plotting mode. may be in (line, scatter, column, bar, hist,
                            tick, barcode, point, contour, density) default=line
      --colors COLORS       color palatte mode. may be in (bostock, brewer, mono,
                            hcl_ggplot2) default=brewer
      --alpha ALPHA         alpha value for markers in --mode scatter
      --dot_size MARKERSIZE, --markersize MARKERSIZE
                            value for markers in --mode scatter
      --linewidth LINEWIDTH
                            Line width for the plot. default=2.0
      --logy                Put the y-axis into log. default=False
      --logx                Put the x-axis into log. default=False
      --title TITLE         Plot title.
      --xlabel XLABEL       X-axis label.
      --ylabel YLABEL       Y-axis label.
      --xmin USER_XMIN      xmin value.
      --xmax USER_XMAX      xmax value.
      --ymin USER_YMIN      ymin value.
      --ymax USER_YMAX      ymax value.
      --height HEIGHT       height of image, in inches. default=4.0
      --width WIDTH         width of image, in inches. default=9.0
      --dpi DPI             dots per inch of raster outputs, i.e. if --outFormat is all or
                            png. default=300
      --out_format OUT_FORMAT
                            output format [pdf|png|eps|all]. default=pdf
      --no_legend           Turns off the filename / color legend. Helpful for large
                            numbers of files.
      --regression          turn on a simple linear regression line
      --jitter              turn on jitter for certain plotting modes
      --aspect_equal        Turn on equal aspect ratio for the plot

    contour:
      --contour_bin CONTOUR_BIN
                            Bin size of the contour plot. Smaller integers lead to
                            smoother curves.
      --contour_logspace    Switch the contour lines from linear spacing to log spacing
      --contour_num_levels CONTOUR_NUM_LEVELS
                            The number of levels in the contour plot, default=6

    density:
      --density_covariance DENSITY_COVARIANCE
                            Gaussian kernel density estimate covariance, raising the value
                            leads to smoother curves. This roughly corresponds to
                            bandwidth in R. Default is to discover the value
                            automatically.
      --density_num_bins DENSITY_NUM_BINS
                            Number of "bins" for the density curve. default=200


## Examples
### Plotting 2D scatter data, one file, no legend.

    bin/quick_plot example/data_2d_1.txt --mode scatter --markersize 7.0 --out_format png --out img/example_01.png --title '2D scatter data from example/data_2d_1.txt' --xlabel 'The x-axis' --ylabel 'The y-axis' --no_legend

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_01.png)

### Plotting 2D scatter data, two files.

    bin/quick_plot example/data_2d_1.txt example/data_2d_2.txt --mode scatter --markersize 7.0 --out_format png --out img/example_02.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_02.png)

### Plotting 2D line data, two files.

    bin/quick_plot example/data_2d_3.txt example/data_2d_4.txt --mode line --out_format png --out img/example_03.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_03.png)

### Plotting 2D line data, three files.

    bin/quick_plot example/data_2d_5.txt example/data_2d_6.txt example/data_2d_7.txt --mode line --out_format png --out img/example_04.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_04.png)

### Plotting 1D data as bars, two files.

    bin/quick_plot example/data_1d_1.txt example/data_1d_2.txt --mode bar --out_format png --out img/example_05.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_05.png)

### Plotting 1D data as tick marks, two files.

    bin/quick_plot example/data_1d_1.txt example/data_1d_2.txt --mode tick --out_format png --out img/example_06.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_06.png)

### Plotting 1D data as point marks, two files.

    bin/quick_plot example/data_1d_1.txt example/data_1d_2.txt --mode point --out_format png --out img/example_07.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_07.png)

### Plotting 1D data as point clouds (using jitter), two files.

    bin/quick_plot example/data_1d_1.txt example/data_1d_2.txt --mode point --jitter --out_format png --out img/example_08.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_08.png)

### Plotting 1D data as histogram, three files.

    bin/quick_plot example/data_1d_3.txt example/data_1d_4.txt example/data_1d_5.txt --mode hist --out_format png --out img/example_09.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_09.png)

### Plotting 2D data as scatter plot, one file.

    bin/quick_plot example/data_2d_8.txt --mode scatter --markersize 5.0 --out_format png --out img/example_10.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_10.png)

### Plotting 2D data as scatter plot with alpha transparency, one file.

    bin/quick_plot example/data_2d_8.txt --mode scatter --markersize 5.0 --alpha 0.1 --out_format png --out img/example_11.png

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_11.png)

### Plotting 2D data as scatter plot with alpha transparency, fixing the aspect ratio, one file.

    bin/quick_plot example/data_2d_8.txt --mode scatter --markersize 5.0 --alpha 0.1 --out_format png --out img/example_11_a.png --aspect_equal

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_11_a.png)

### Plotting 1D data as density curve, one file.

    bin/quick_plot example/data_1d_7.txt --mode density --out_format png --out img/example_12.png --title 'data_2d_8.txt x marginal'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_12.png)

### Plotting 1D data as density curve, one file.

    bin/quick_plot example/data_1d_8.txt --mode density --out_format png --out img/example_13.png --title 'data_2d_8.txt y marginal'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_13.png)

### Plotting 2D data as contour plot, one file.

    bin/quick_plot example/data_2d_8.txt --mode contour --out_format png --out img/example_14.png --title 'A hard example for a contour plot'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_14.png)

### Plotting 2D data as contour plot, one file.

    bin/quick_plot example/data_2d_9.txt --mode contour --out_format png --out img/example_15.png --title 'An easier example for a contour plot'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_15.png)
