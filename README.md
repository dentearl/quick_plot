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
      --out OUT             path/filename where figure will be created. No extension needed.
                            default=my_plot
      --mode MODE           plotting mode. may be in (line, scatter, column, bar, hist, tick, barcode,
                            point, contour, density, matrix) default=line
      --columns COLUMNS     two numbers, comma separated, can be reverse order, indicates x,y for
                            plotting. 1-based.
      --downsample DOWNSAMPLE
                            Randomly sample only n values from each input. Can help cutdown on runtime
                            and output size for pdfs.
      --colors COLORS       color palatte mode. may be in (bostock, brewer, mono, hcl_ggplot2)
                            default=brewer
      --color_index_offset COLOR_INDEX_OFFSET
                            index offset value to shift the starting point of the selected color map.
                            default=0
      --alpha ALPHA         alpha value for markers in --mode scatter
      --dot_size MARKERSIZE, --markersize MARKERSIZE
                            value for markers in --mode scatter
      --marker MARKER       Marker to use.
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
      --dpi DPI             dots per inch of raster outputs, i.e. if --outFormat is all or png.
                            default=300
      --out_format OUT_FORMAT
                            output format [pdf|png|eps|all]. default=pdf
      --no_legend           Turns off the filename / color legend. Helpful for large numbers of files.
      --regression          turn on a simple linear regression line
      --jitter              turn on jitter for certain plotting modes
      --random_seed RANDOM_SEED
                            Random seed for use with --jitter and --downsample flags.
      --aspect_equal        Turn on equal aspect ratio for the plot

    contour mode:
      --contour_bin CONTOUR_BIN
                            Bin size of the contour plot. Smaller integers lead to smoother curves.
      --contour_logspace    Switch the contour lines from linear spacing to log spacing
      --contour_num_levels CONTOUR_NUM_LEVELS
                            The number of levels in the contour plot, default=6

    density mode:
      --density_covariance DENSITY_COVARIANCE
                            Gaussian kernel density estimate covariance, raising the value leads to
                            smoother curves. This roughly corresponds to bandwidth in R. Default is to
                            discover the value automatically.
      --density_num_bins DENSITY_NUM_BINS
                            Number of "bins" for the density curve. default=200

    matrix mode:
      --matrix_matshow      Switches the drawing call from pcolor() to matshow(). matshow() uses rasters,
                            pcolor() uses vectors. For very large matrices matshow() may be desirable.
      --matrix_cmap MATRIX_CMAP
                            The colormap to be used. default=binary. Possible values: Spectral, summer,
                            coolwarm, Set1, Set2, Set3, Dark2, hot, RdPu, YlGnBu, RdYlBu, gist_stern,
                            cool, gray, GnBu, gist_ncar, gist_rainbow, bone, RdYlGn, spring, terrain,
                            PuBu, spectral, gist_yarg, BuGn, bwr, cubehelix, YlOrRd, Greens, PRGn,
                            gist_heat, Paired, hsv, Pastel2, Pastel1, BuPu, copper, OrRd, brg, gnuplot2,
                            jet, gist_earth, Oranges, PiYG, YlGn, Accent, gist_gray, flag, BrBG, Reds,
                            RdGy, PuRd, Blues, Greys, autumn, pink, binary, winter, gnuplot, RdBu, prism,
                            YlOrBr, rainbow, seismic, Purples, ocean, PuOr, PuBuGn, afmhot
      --matrix_no_colorbar  turn off the colorbar.
      --matrix_discritize_colormap MATRIX_DISCRITIZE_COLORMAP
                            number of bins to discritize colormap


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
(Remove the <code>--random_seed</code> for production use).

    bin/quick_plot example/data_1d_1.txt example/data_1d_2.txt --mode point --jitter --out_format png --out img/example_08.png --random_seed=127

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

### Plotting 2D data as scatter plot using downsampling to 1000 points, fixing the aspect ratio, one file.
(Remove the <code>--random_seed</code> for production use).

    bin/quick_plot example/data_2d_8.txt --mode scatter --markersize 5.0 --out_format png --out img/example_11_b.png --aspect_equal --random_seed=127 --downsample 1000 --title 'Downsampled to 1000 points'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_11_b.png)

### Plotting 2D data as scatter plot using downsampling to 100 points, fixing the aspect ratio, one file.
(Remove the <code>--random_seed</code> for production use).

    bin/quick_plot example/data_2d_8.txt --mode scatter --markersize 5.0 --alpha 0.1 --out_format png --out img/example_11_c.png --aspect_equal --random_seed=127 --downsample 100 --title 'Downsampled to 100 points'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_11_c.png)

### Plotting 1D data as density curve, one file.

    bin/quick_plot example/data_1d_7.txt --mode density --out_format png --out img/example_12.png --title 'data_2d_8.txt x marginal'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_12.png)

### Plotting 1D data as density curve, one file, selecting column to plot.

    bin/quick_plot example/data_2d_8.txt --mode density --out_format png --out img/example_12_a.png --title 'data_2d_8.txt x marginal' --columns 1

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_12_a.png)


### Plotting 1D data as density curve, one file.

    bin/quick_plot example/data_1d_8.txt --mode density --out_format png --out img/example_13.png --title 'data_2d_8.txt y marginal'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_13.png)

### Plotting 1D data as density curve, one file, selecting column to plot.

    bin/quick_plot example/data_1d_8.txt --mode density --out_format png --out img/example_13_a.png --title 'data_2d_8.txt y marginal' --columns 2

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_13_a.png)

### Plotting 2D data as contour plot, one file.

    bin/quick_plot example/data_2d_8.txt --mode contour --out_format png --out img/example_14.png --title 'A hard example for a contour plot'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_14.png)

### Plotting 2D data as contour plot, one file.

    bin/quick_plot example/data_2d_9.txt --mode contour --out_format png --out img/example_15.png --title 'An easier example for a contour plot'

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_15.png)

### Anscombe's quartet, plotting from a single file with many columns, mixing and matching columns

    bin/quick_plot example/anscombe.txt --mode scatter --out_format png --out img/example_16.png --title 'Anscombe_i' --regression  --markersize 5.0 --ymin 3 --ymax 13 --xmin 3 --xmax 20 --no_legend

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_16.png)

    bin/quick_plot example/anscombe.txt --mode scatter --out_format png --out img/example_17.png --title 'Anscombe_ii' --regression  --markersize 5.0 --ymin 3 --ymax 13 --xmin 3 --xmax 20 --no_legend --columns 3,4

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_17.png)

    bin/quick_plot example/anscombe.txt --mode scatter --out_format png --out img/example_18.png --title 'Anscombe_iii' --regression  --markersize 5.0 --ymin 3 --ymax 13 --xmin 3 --xmax 20 --no_legend --columns 5,6

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_18.png)

    bin/quick_plot example/anscombe.txt --mode scatter --out_format png --out img/example_19.png --title 'Anscombe_iiv' --regression  --markersize 5.0 --ymin 3 --ymax 13 --xmin 3 --xmax 20 --no_legend --columns 7,8

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_19.png)

### Matrix plot (heatmap) using a continuous colormap

    bin/quick_plot example/distance_matrix.txt --mode matrix --out_format png --out img/example_20.png --title 'Heatmap' --matrix_cmap Reds --width 6

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_20.png)

### Matrix plot (heatmap) using a continuous colormap, censoring colormap

    bin/quick_plot example/distance_matrix.txt --mode matrix --out_format png --out img/example_20_a.png --title 'Heatmap' --matrix_cmap Reds --width 6 --matrix_colormap_max 0.20

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_20_a.png)

### Heatmap using a discritized colormap

    bin/quick_plot example/distance_matrix_1.txt --mode matrix --out_format png --out img/example_21.png --title 'Heatmap 2' --width 6 --matrix_discritize_colormap 6

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_21.png)

### Heatmap using a discritized colormap without a colorbar

    bin/quick_plot example/distance_matrix_2.txt --mode matrix --out_format png --out img/example_22.png --title 'Heatmap 3' --matrix_cmap Oranges --width 6 --matrix_discritize_colormap 10 --matrix_no_colorbar

![Example image](https://github.com/dentearl/quick_plot/raw/master/img/example_22.png)
