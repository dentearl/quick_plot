#!/usr/bin/env python
"""
quick_plot
9 Oct 2013
Dent Earl (dent.earl a gmail.com)

A quick plotting program for creating fast sketches of data.

"""
##############################
# Copyright (C) 2013 by
# Dent Earl (dearl@soe.ucsc.edu, dent.earl@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##############################
# plotting boilerplate / cargo cult
import matplotlib
matplotlib.use('Agg')
#####
# the param pdf.fonttype allows for text to be editable in Illustrator.
# Use either Output Type 3 (Type3) or Type 42 (TrueType)
matplotlib.rcParams['pdf.fonttype'] = 42
import matplotlib.backends.backend_pdf as pltBack
import matplotlib.lines as lines
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import numpy
##############################
from argparse import ArgumentParser
import os
from scipy.stats import scoreatpercentile, linregress, gaussian_kde
import sys


class BadInput(Exception):
  pass


class Data(object):
  """Class data holds data for plotting
  """
  def __init__(self):
    self.data = None  # this will be an n by 2 numpy array.
    self.label = ''


def InitArguments(parser):
  """Initialize arguments for the program.

  Args:
    parser: an argparse parser object
  """
  parser.add_argument('files', nargs='+', help='files to plot')
  parser.add_argument('--out', dest='out', default='my_plot',
                      type=str,
                      help=('path/filename where figure will be created. No '
                            'extension needed. default=%(default)s'))
  parser.add_argument('--mode', dest='mode', default='line', type=str,
                      help=('plotting mode. may be in (line, scatter, '
                            'column, bar, hist, tick, barcode, point, contour, '
                            'density) default=%(default)s'))
  parser.add_argument('--colors', dest='colors', default='brewer', type=str,
                      help=('color palatte mode. may be in (bostock, brewer, '
                            'mono, hcl_ggplot2) '
                            'default=%(default)s'))
  parser.add_argument('--color_index_offset', dest='color_index_offset',
                      type=int, default=0,
                      help=('index offset value to shift the starting point '
                            'of the selected color map. default=%(default)s'))
  parser.add_argument('--alpha', default=1.0, type=float,
                      help='alpha value for markers in --mode scatter')
  parser.add_argument('--dot_size', '--markersize', dest='markersize',
                      default=2.0, type=float,
                      help='value for markers in --mode scatter')
  parser.add_argument('--linewidth', dest='linewidth', default=2.0,
                      type=float,
                      help='Line width for the plot. default=%(default)s')
  parser.add_argument('--logy', dest='is_log_y', default=False,
                      action='store_true',
                      help='Put the y-axis into log. default=%(default)s')
  parser.add_argument('--logx', dest='is_log_x', default=False,
                      action='store_true',
                      help='Put the x-axis into log. default=%(default)s')
  parser.add_argument('--title', dest='title', type=str,
                      default='sentinel_value',
                      help='Plot title.')
  parser.add_argument('--xlabel', dest='xlabel', type=str,
                      default='sentinel_value',
                      help='X-axis label.')
  parser.add_argument('--ylabel', dest='ylabel', type=str,
                      default='sentinel_value',
                      help='Y-axis label.')
  parser.add_argument(
    '--xmin', dest='user_xmin', default=sys.maxint, type=float,
    help='xmin value.')
  parser.add_argument(
    '--xmax', dest='user_xmax', default=-sys.maxint, type=float,
    help='xmax value.')
  parser.add_argument(
    '--ymin', dest='user_ymin', default=sys.maxint, type=float,
    help='ymin value.')
  parser.add_argument(
    '--ymax', dest='user_ymax', default=-sys.maxint, type=float,
    help='ymax value.')
  parser.add_argument('--height', dest='height', default=4.0, type=float,
                      help='height of image, in inches. default=%(default)s')
  parser.add_argument('--width', dest='width', default=9.0, type=float,
                      help='width of image, in inches. default=%(default)s')
  parser.add_argument('--dpi', dest='dpi', default=300,
                      type=int,
                      help=('dots per inch of raster outputs, i.e. '
                            'if --outFormat is all or png. '
                            'default=%(default)s'))
  parser.add_argument('--out_format', dest='out_format', default='pdf',
                      type=str,
                      help=('output format [pdf|png|eps|all]. '
                            'default=%(default)s'))
  parser.add_argument('--no_legend', dest='is_legend', default=True,
                      action='store_false',
                      help=('Turns off the filename / color legend. '
                            'Helpful for large numbers of files.'))
  parser.add_argument('--regression', dest='regression', default=False,
                      action='store_true',
                      help='turn on a simple linear regression line')
  parser.add_argument('--jitter', dest='jitter', default=False,
                      action='store_true',
                      help='turn on jitter for certain plotting modes')
  parser.add_argument('--aspect_equal', dest='aspect_equal', default=False,
                      action='store_true',
                      help='Turn on equal aspect ratio for the plot')
  contour = parser.add_argument_group('contour')
  contour.add_argument('--contour_bin', dest='contour_bin', default=10,
                       type=int,
                       help=('Bin size of the contour plot. Smaller integers '
                             'lead to smoother curves.'))
  contour.add_argument('--contour_logspace', dest='contour_logspace',
                       default=False, action='store_true',
                       help=('Switch the contour lines from linear spacing '
                             'to log spacing'))
  contour.add_argument('--contour_num_levels', dest='contour_num_levels',
                       default=6, type=int,
                       help=('The number of levels in the contour plot, '
                             'default=%(default)s'))
  density = parser.add_argument_group('density')
  density.add_argument('--density_covariance', dest='density_covariance',
                       type=float,
                       help=('Gaussian kernel density estimate covariance, '
                             'raising the value leads to smoother curves. '
                             'This roughly corresponds to bandwidth in R. '
                             'Default is to discover the value automatically.'))
  density.add_argument('--density_num_bins', dest='density_num_bins', type=int,
                       default=200,
                       help=('Number of "bins" for the density curve. '
                             'default=%(default)s'))


def CheckArguments(args, parser):
  """Verify that input arguments are correct and sufficient.

  Args:
    args: an argparse arguments object
    parser: an argparse parser object
  """
  args.recognized_modes = ['line', 'scatter', 'bar', 'column', 'hist',
                           'tick', 'barcode', 'point', 'contour', 'density']
  if len(args.files) > 0:
    for f in args.files:
      if not os.path.exists(f):
        parser.error('File %s does not exist.\n' % f)
  else:
    parser.error('File paths must be passed in on command line!')
  if args.dpi < 72:
    parser.error('--dpi %d less than screen res, 72. Must be >= 72.'
                 % args.dpi)
  if args.out_format not in ('pdf', 'png', 'eps', 'all'):
    parser.error('Unrecognized --out_format %s. Choose one from: '
                 'pdf png eps all.' % args.out_format)
  if args.mode not in args.recognized_modes:
    parser.error('Unrecognized --mode %s. Choose one from: %s'
                 % (args.mode, str(args.recognized_mode)))
  if args.mode == 'contour':
    if len(args.files) > 1:
      parser.error('--mode=contour does not permit more than one file '
                   'to be plotted at a time.')
  if args.colors not in ('bostock', 'brewer', 'mono'):
    parser.error('Unrecognized --colors %s palette. Choose one from: '
                 'bostock brewer mono.' % args.colors)
  if (args.out.endswith('.png') or args.out.endswith('.pdf') or
      args.out.endswith('.eps')):
    args.out = args.out[:-4]
  args.xmax = -sys.maxint
  args.xmin = sys.maxint
  args.ymax = -sys.maxint
  args.ymin = sys.maxint
  if args.contour_bin < 3:
    parser.error('--contour_bin must be greater than 3.')
  DefineColors(args)


def DefineColors(args):
  """Based on --colors, define the set of colors to use in the plot.

  Args:
    args: an argparse arguments object
  """
  # TODO: allow for a way to override the color list
  if args.colors == 'bostock':
    args.colors_light = ['#aec7e8',  # l blue
                         '#ffbb78',  # l orange
                         '#98df8a',  # l green
                         '#ff9896',  # l red
                         '#c5b0d5',  # l purple
                         '#c49c94',  # l brown
                         '#f7b6d2',  # l lavender
                         '#c7c7c7',  # l gray
                         '#dbdb8d',  # l olive
                         '#9edae5',  # l aqua
                        ]
    args.colors_medium = ['#1f77b4',  # d blue
                          '#ff7f0e',  # d orange
                          '#2ca02c',  # d green
                          '#d62728',  # d red
                          '#9467bd',  # d purple
                          '#8c564b',  # d brown
                          '#e377c2',  # d lavender
                          '#7f7f7f',  # d gray
                          '#bcbd22',  # d olive
                          '#17becf',  # d aqua
                         ]
    args.colors_dark = []
  elif args.colors == 'brewer':
    args.colors_light = [(136, 189, 230),  # l blue
                         (251, 178,  88),  # l orange
                         (144, 205, 151),  # l green
                         (246, 170, 201),  # l red
                         (191, 165,  84),  # l brown
                         (188, 153, 199),  # l purple
                         (240, 126, 110),  # l magenta
                         (140, 140, 140),  # l grey
                         (237, 221,  70),  # l yellow
                        ]
    args.colors_medium = [( 93, 165, 218),  # m blue
                          (250, 164,  58),  # m orange
                          ( 96, 189, 104),  # m green
                          (241, 124, 167),  # m red
                          (178, 145,  47),  # m brown
                          (178, 118, 178),  # m purple
                          (241,  88,  84),  # m magenta
                          ( 77,  77,  77),  # m grey
                          (222, 207,  63),  # m yellow
                         ]
    args.colors_dark = [( 38,  93, 171),  # d blue
                        (223,  92,  36),  # d orange
                        (  5, 151,  72),  # d green
                        (229,  18, 111),  # d red
                        (157, 114,  42),  # d brown
                        (123,  58, 150),  # d purple
                        (203,  32,  39),  # d magenta
                        (  0,   0,   0),  # black
                        (199, 180,  46),  # d yellow
                       ]
    CorrectColorTuples(args)
  elif args.colors == 'mono':
    args.colors_light = [(140, 140, 140),  # l grey
                        ]
    args.colors_medium = [( 77,  77,  77),  # m grey
                         ]
    args.colors_dark = [(  0,   0,   0),  # black
                       ]
    CorrectColorTuples(args)
  elif args.colors == 'hcl_ggplot2':
    args.colors_light = [(158, 217, 255),  # l blue
                         (246, 209, 146),  # l mustard
                         ( 93, 237, 189),  # l green
                         (255, 189, 187),  # l pink
                         (182, 228, 149),  # l olive
                         ( 51, 235, 236),  # l teal
                         (241, 194, 255),  # l purple
                         (255, 179, 234),  # l magenta
                        ]
    args.colors_medium = [( 98, 162, 209),  # m blue
                          (190, 154,  87),  # m mustard
                          (223, 133, 131),  # m pink
                          (  0, 183, 134),  # m green
                          (126, 173,  90),  # m olive
                          (  0, 180, 181),  # m teal
                          (187, 134, 209),  # m purple
                          (225, 122, 179),  # m magenta
                         ]
    args.colors_dark = [(  0, 163, 255),  # d blue
                        (213, 151,   0),  # d mustard
                        (  0, 201, 106),  # d green
                        (254, 102,  97),  # d pink
                        ( 98, 183,   0),  # d olive
                        (  1, 196, 200),  # d teal
                        (219,  95, 255),  # d purple
                        (255,  40, 201),  # d magenta
                       ]
    CorrectColorTuples(args)


def CorrectColorTuples(args):
  """Corrects the 0-255 values in colors_light and colors_medium to 0.0-1.0

  Args:
    args: an argparse arguments object
  """
  for i in xrange(0, len(args.colors_light)):
    args.colors_light[i] = (args.colors_light[i][0] / 255.0,
                            args.colors_light[i][1] / 255.0,
                            args.colors_light[i][2] / 255.0,)
  for i in xrange(0, len(args.colors_medium)):
    args.colors_medium[i] = (args.colors_medium[i][0] / 255.0,
                             args.colors_medium[i][1] / 255.0,
                             args.colors_medium[i][2] / 255.0,)
  for i in xrange(0, len(args.colors_dark)):
    args.colors_dark[i] = (args.colors_dark[i][0] / 255.0,
                           args.colors_dark[i][1] / 255.0,
                           args.colors_dark[i][2] / 255.0,)


def InitImage(args):
  """Initialize a new image.

  Args:
    args: an argparse arguments object

  Returns:
    fig: a matplotlib figure object
    pdf: a matplotlib pdf drawing (backend) object
  """
  pdf = None
  if args.out_format == 'pdf' or args.out_format == 'all':
    pdf = pltBack.PdfPages(args.out + '.pdf')
  fig = plt.figure(figsize=(args.width, args.height),
                   dpi=args.dpi, facecolor='w')
  return (fig, pdf)


def EstablishAxes(fig, args):
  """Create a single axis on the figure object

  Args:
    fig: a matplotlib figure object
    args: an argparse arguments object

  Returns:
    ax: a matplotlib axis object
  Raises:
    ValueError: If an unknown spine location is passed.
  """
  args.axLeft = 0.11
  args.axWidth = 0.83
  args.axBottom = 0.17
  args.axHeight = 0.76
  ax = fig.add_axes([args.axLeft, args.axBottom,
                     args.axWidth, args.axHeight])
  ax.yaxis.set_major_locator(pylab.NullLocator())
  ax.xaxis.set_major_locator(pylab.NullLocator())
  for loc, spine in ax.spines.iteritems():
    if loc in ['left', 'bottom']:
      spine.set_position(('outward', 10))
    elif loc in ['right', 'top']:
      spine.set_color('none')
    else:
      raise ValueError('unknown spine location: %s' % loc)
  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.set_ticks_position('left')
  return ax


def WriteImage(fig, pdf, args):
  """Write the image to disk.

  Args:
    fig: a matplotlib figure object
    pdf: a matplotlib pdf drawing (backend) object
    args: an argparse arguments object
  """
  if args.out_format == 'pdf':
    fig.savefig(pdf, format = 'pdf')
    pdf.close()
  elif args.out_format == 'png':
    fig.savefig(args.out + '.png', format='png', dpi=args.dpi)
  elif args.out_format == 'all':
    fig.savefig(pdf, format='pdf')
    pdf.close()
    fig.savefig(args.out + '.png', format='png', dpi=args.dpi)
    fig.savefig(args.out + '.eps', format='eps')
  elif args.out_format == 'eps':
    fig.savefig(args.out + '.eps', format='eps')


def ColorPicker(i, args):
  """Returns a valid matplotlib color based on the index, plot mode and palette

  Args:
    i: index, integer
    args: an argparse arguments object

  Returns:
    color: a valid matplotlib color, or a list of colors if mode is hist
           or a name of a valid matplotlib colormap or a matplotlib color map
           if the mode is contour
  """
  i += args.color_index_offset
  if args.mode in ('column', 'bar'):
    return args.colors_light[i % len(args.colors_light)]
  elif args.mode in ('hist'):
    # hist requires a list of colors be returned
    colors = []
    for i in xrange(0, i):
      colors.append(args.colors_light[i % len(args.colors_light)])
    return colors
  elif args.mode in ('contour'):
    colors = 'k'
    return colors
  elif args.mode in ('line', 'scatter', 'tick', 'point', 'barcode', 'density'):
    return args.colors_medium[i % len(args.colors_medium)]


def PlotDensity(data_list, ax, args):
  """Plot one dimensional data as density curves.

  Args:
    data_list: a list of Data objects
    ax: a matplotlib axis object
    args: an argparse arguments object
  """
  # first create density list, then pass that to PlotLineScatter
  density_list = []
  for data in data_list:
    d = Data()
    d.label = data.label
    density = gaussian_kde(data.data[1])
    x_data = numpy.linspace(numpy.min(data.data[1]),
                            numpy.max(data.data[1]),
                            args.density_num_bins)
    if args.density_covariance is not None:
      density.covariance_factor = lambda : args.density_covariance
      density._compute_covariance()  # bad mojo calling privates like this
    d.data = numpy.array([x_data, density(x_data)])
    density_list.append(d)
  PlotLineScatter(density_list, ax, args)


def PlotTwoDimension(data_list, ax, args):
  """Plot two dimensional data.

  Args:
    data_list: a list of Data objects
    ax: a matplotlib axis object
    args: an argparse arguments object
  """
  if args.mode in ('scatter', 'line'):
    PlotLineScatter(data_list, ax, args)
  elif args.mode == 'contour':
    PlotContour(data_list, ax, args)
  elif args.mode == 'density':
    PlotDensity(data_list, ax, args)


def PlotContour(data_list, ax, args):
  """Plot two dimensional density contour.

  Args:
    data_list: a list of Data objects
    ax: a matplotlib axis object
    args: an argparse arguments object
  """
  data = data_list[0]
  x = data.data[0]
  y = data.data[1]
  H, xedges, yedges = numpy.histogram2d(
    x, y, range=[[min(x), max(x)], [min(y), max(y)]], bins=(args.contour_bin,
                                                            args.contour_bin))
  extent = [yedges[0], yedges[-1], xedges[0], xedges[-1]]
  c_max = max(map(max, H))
  c_min = min(map(min, H))
  nc_levels = args.contour_num_levels
  if args.contour_logspace:
    c_levels = numpy.logspace(c_min, c_max, nc_levels)
  else:
    c_levels = numpy.linspace(c_min, c_max, nc_levels)
  im = plt.imshow(H, interpolation='bilinear', origin='lower',
                  cmap=matplotlib.cm.binary, extent=extent)
  c_set = plt.contour(H, extent=extent, origin='lower',
                      levels=c_levels, colors=ColorPicker(0, args))
  plt.clabel(c_set, colors='red', inline=True, fmt='%1.0i',
             rightside_up=True)
  # for c in c_set.collections:
  #   c.set_linestyle('solid')
  print 'ha'


def PlotLineScatter(data_list, ax, args):
  """Plot two dimensional line or scatter data.

  Args:
    data_list: a list of Data objects
    ax: a matplotlib axis object
    args: an argparse arguments object
  """
  if args.mode == 'scatter':
    marker = 'o'
    args.linewidth = 0.0
    alpha = args.alpha
  else:
    marker = None
    alpha = 1.0
  args.xmin = min(map(min, map(lambda data: data.data[0], data_list)))
  args.xmax = max(map(max, map(lambda data: data.data[0], data_list)))
  args.ymin = min(map(min, map(lambda data: data.data[1], data_list)))
  args.ymax = max(map(max, map(lambda data: data.data[1], data_list)))
  for i, data in enumerate(data_list, 0):
    ax.add_line(
      lines.Line2D(xdata=data.data[0],
                   ydata=data.data[1],
                   color=ColorPicker(i, args),
                   marker=marker,
                   markersize=args.markersize,
                   markerfacecolor=ColorPicker(i, args),
                   markeredgecolor='None',
                   alpha=alpha,
                   linewidth=args.linewidth))
    if args.regression:
      data.data[0].sort()
      data.data[1].sort()
      rxlist = numpy.array(data.data[0])
      rylist = numpy.array(data.data[1])
      A = numpy.array([rxlist, numpy.ones(len(rxlist))])
      try:
        w = numpy.linalg.lstsq(A.T, rylist)[0]
      except ValueError:
        sys.stderr.write('Warning, unable to perform regression!')
        return
      fitline = (w[0] * rxlist) + w[1]
      ax.add_line(
        lines.Line2D(xdata=[rxlist[0], rxlist[-1]],
                     ydata=[fitline[0], fitline[-1]],
                     color='red',
                     linestyle='--'))
      slope, intercept, r, p, stderr = linregress(rxlist, rylist)
      ax.text(x=(rxlist[0] + rxlist[-1]) / 2.0,
              y=(fitline[0] + fitline[-1]) / 2.0,
              s=r'%f * x + %f, $r^2$=%f' % (w[0], w[1], r * r))


def ReadFiles(args):
  """Read and parse all input files.

  Args:
    args: an argparse arguments object

  Returns:
    data_list: a list of numpy arrays of dimension (n by 1) or (n by 2)
      depending on the --mode flag.
  """
  data_list = []
  for a_file in args.files:
    f = open(a_file, 'r')
    xlist = []
    ylist = []
    i = 0
    for line in f:
      line = line.strip()
      if line.startswith('#'):
        continue
      d = line.split()
      if d[0].lower() == 'nan':
        continue
      if len(d) > 1:
        # two values
        if d[0].lower() == 'nan' or d[1].lower() == 'nan':
          continue
        xlist.append(float(d[0]))
        ylist.append(float(d[1]))
        if args.xmin > xlist[-1]:
          args.xmin = xlist[-1]
        if args.xmax < xlist[-1]:
          args.xmax = xlist[-1]
      else:
        ylist.append(float(d[0]))
        if args.mode in ('scatter', 'line'):
          xlist.append(i)
          i += 1
      if args.ymin > ylist[-1]:
        args.ymin = ylist[-1]
      if args.ymax < ylist[-1]:
        args.ymax = ylist[-1]
    f.close()
    d = Data()
    d.label = os.path.basename(a_file)
    if ylist == []:
      d.data = numpy.array(xlist)
    else:
      d.data = numpy.array([xlist, ylist])
    data_list.append(d)
  return data_list


def PlotOneDimension(data_list, ax, args):
  """Plot one dimensional data.

  Args:
    data_list: a list of Data objects.
    ax: a matplotlib axis object.
    args: an argparse arguments object.
  """
  if args.mode == 'bar' or args.mode == 'column':
    PlotColumns(data_list, ax, args)
  elif args.mode == 'hist':
    PlotHistogram(data_list, ax, args)
  elif args.mode == 'tick' or args.mode == 'barcode':
    PlotTicks(data_list, ax, args)
  elif args.mode == 'point':
    PlotPoints(data_list, ax, args)


def PlotHistogram(data_list, ax, args):
  """Plot one dimensional data as histogram.

  Args:
    data_list: a list of Data objects.
    ax: a matplotlib axis object.
    args: an argparse arguments object.
  """
  width = 2.0 / 3.0 / len(data_list)
  datas = []
  for data in data_list:
    datas.append(data.data[1])
  n, bins, patch_groups = ax.hist(
    datas, color=ColorPicker(len(data_list), args), histtype='bar')
  for pg in patch_groups:
    if isinstance(pg, matplotlib.container.BarContainer):
      # if there are multiple files, pg will be a BarContainer
      for patch in pg.patches:
        patch.set_edgecolor('none')
    else:
      # if there is only one file to plot, pg is a Rectangle
      pg.set_edgecolor('white')


def PlotColumns(data_list, ax, args):
  """Plot one dimensional data as column / bar plot.

  Args:
    data_list: a list of Data objects.
    ax: a matplotlib axis object.
    args: an argparse arguments object.
  """
  width = 2.0 / 3.0 / len(data_list)
  data_min = min(map(numpy.min, map(lambda x: x.data[1], data_list)))
  data_max = max(map(numpy.max, map(lambda x: x.data[1], data_list)))
  args.xmin = 0
  args.xmax = max(map(len, map(lambda data: data.data[1], data_list)))
  for i, data in enumerate(data_list, 0):
    data.data[0] = range(0, len(data.data[1]))
    data.data[0] = numpy.add(data.data[0], width * i)  # offset
    rects = ax.bar(data.data[0],
                   data.data[1],
                   width,
                   color=ColorPicker(i, args),
                   linewidth=0.0,
                   alpha=1.0)
    ax.xaxis.set_ticklabels([])
  xmin, xmax, ymin, ymax = ax.axis()
  ymin, ymax = HandleLimits(min(0.0, data_min), ymax,
                            args.user_ymin, args.user_ymax)
  args.ymin = ymin
  args.ymax = ymax
  ax.set_ylim([ymin, ymax])


def GetTickYValues(i, args):
  """Produce the lower and upper y values for a Tick plot.

  Args:
    i: Integer offset of this set of values.
    args: an argparse arguments object.

  Returns:
    y0, y1: the lower and upper y values for a Tick Plot
  """
  if args.jitter:
    lo = numpy.random.uniform(low=0.0, high=0.3)
    return i + lo, i + lo + 0.1
  else:
    return i, i + 0.8


def HandleLimits(data_min, data_max, user_min, user_max):
  """Decides whether to use the data values or user supplied values.

  Args:
    data_min: minimum value from the data
    data_max: maximum value from the data
    user_min: possibly a user requested value for min
    user_max: possibly a user requested value for max

  Returns:
    a_min: the correct minimum
    a_max: the correct maximum
  """
  a_min, a_max = data_min, data_max
  if user_min != sys.maxint:
    a_min = user_min
  if user_max != -sys.maxint:
    a_max = user_max
  return a_min, a_max


def PlotTicks(data_list, ax, args):
  """Plot one dimensional data as tick marks on a line.

  Args:
    data_list: a list of Data objects
    ax: a matplotlib axis object
    args: an argparse arguments object
  """
  data_min = min(map(numpy.min, map(lambda x: x.data[1], data_list)))
  data_max = max(map(numpy.max, map(lambda x: x.data[1], data_list)))
  data_range = data_max - data_min
  if data_range == 0.0:
    data_min, data_max, data_range = -0.5, 0.5, 1.0
  data_min -= data_range * 0.1
  data_max += data_range * 0.1
  for i, data in enumerate(data_list, 0):
    for d in data.data[1]:
      y0, y1 = GetTickYValues(i, args)
      ax.add_line(
        lines.Line2D(xdata=[d, d],
                     ydata=[y0, y1],
                     color=ColorPicker(i, args),
                     marker=None,
                     markersize=args.markersize,
                     markerfacecolor=ColorPicker(i, args),
                     markeredgecolor='None',
                     alpha=args.alpha,
                     linewidth=args.linewidth))
  ymin, ymax = HandleLimits(0.0, len(data_list),
                            args.user_ymin, args.user_ymax)
  ax.set_ylim([ymin, ymax])
  xmin, xmax = HandleLimits(data_min, data_max,
                            args.user_xmin, args.user_xmax)
  ax.set_xlim([xmin, xmax])
  ax.yaxis.set_ticks_position('none')
  ax.yaxis.set_ticks([])


def GetPointYValues(n, i, args):
  """Produce the y values for a Point plot.

  Args:
    n: number of values to produce.
    i: Integer offset of this set of values.
    args: an argparse arguments object.

  Returns:
    y: a list of y values for a Point plot.
  """
  if args.jitter:
    return numpy.random.uniform(low=i, high=i + 0.5, size=n)
  else:
    return [i] * n


def PlotPoints(data_list, ax, args):
  """Plot one dimensional data as points on a line.

  Args:
    data_list: a list of Data objects
    ax: a matplotlib axis object
    args: an argparse arguments object
  """
  data_min = min(map(numpy.min, map(lambda x: x.data[1], data_list)))
  data_max = max(map(numpy.max, map(lambda x: x.data[1], data_list)))
  data_range = data_max - data_min
  if data_range == 0.0:
    data_min, data_max, data_range = -0.5, 0.5, 1.0
  data_min -= data_range * 0.1
  data_max += data_range * 0.1
  for i, data in enumerate(data_list, 0):
    data.data[0] = GetPointYValues(len(data.data[1]), i, args)
    ax.add_line(
      lines.Line2D(xdata=data.data[1],
                   ydata=data.data[0],
                   color=ColorPicker(i, args),
                   marker='o',
                   markersize=args.markersize,
                   markerfacecolor=ColorPicker(i, args),
                   markeredgecolor='None',
                   alpha=args.alpha,
                   linewidth=0.0))
  ymin, ymax = HandleLimits(-0.5, len(data_list),
                             args.user_ymin, args.user_ymax)
  ax.set_ylim([-0.5, len(data_list)])
  xmin, xmax = HandleLimits(data_min, data_max,
                            args.user_xmin, args.user_xmax)
  ax.set_xlim([data_min, data_max])
  ax.yaxis.set_ticks_position('none')
  ax.yaxis.set_ticks([])


def PlotData(data_list, ax, args):
  """Plot all of the data according to input arguments.

  Args:
    data_list: a list of Data objects.
    ax: a matplotlib axis object.
    args: an argparse argument object.
  """
  if args.mode in ('scatter', 'line', 'contour', 'density'):
    PlotTwoDimension(data_list, ax, args)
  elif args.mode in ('bar', 'column', 'hist', 'tick', 'barcode', 'point'):
    PlotOneDimension(data_list, ax, args)


def MakeProxyPlots(args):
  """Make some proxy plots for use with legends.

  Proxy plots are plots that are not actually drawn but whose
  colors are used for correctly populating a legend.

  Args:
    args: an argparse argument object.

  Returns:
    proxy_plots: A list of matplotlib plot objects.
  """
  if args.mode != 'hist':
    proxy_plots = []
    for i, afile in enumerate(args.files, 0):
      proxy_plots.append(
        plt.Rectangle(
          (0, 0), 1, 1,
          fc=ColorPicker(i, args),
          ec=ColorPicker(i, args)))
  else:
    proxy_plots = []
    for i, afile in enumerate(args.files, 0):
      proxy_plots.append(
        plt.Rectangle(
          (0, 0), 1, 1,
          fc=ColorPicker(len(args.files), args)[i],
          ec=ColorPicker(len(args.files), args)[i]))
  return proxy_plots


def MakeLegendLabels(args):
  """Make labels for use with legends.

  Args:
    args: an argparse argument object

  Returns:
    legend_labels: A list of strings.
  """
  legend_labels = []
  for afile in args.files:
    legend_labels.append(os.path.basename(afile))
  return legend_labels


def CleanAxis(ax, args):
  """Clean the axis up, apply scales, add legend.

  Args:
    ax: a matplotlib axis object
    args: an argparse argument object
  """
  # y axis
  if args.is_log_y:
    ax.set_yscale('log')
  else:
    if args.mode not in ('hist', 'tick', 'barcode', 'point', 'bar', 'column'):
      arange = args.ymax - args.ymin
      ymin, ymax = HandleLimits(args.ymin - arange * 0.05,
                                args.ymax + arange * 0.05,
                                args.user_ymin, args.user_ymax)
      ax.set_ylim([ymin, ymax])
  # x axis
  if args.is_log_x:
    ax.set_xscale('log')
  else:
    if args.mode not in ('hist', 'tick', 'barcode', 'point', 'bar', 'column'):
      arange = args.xmax - args.xmin
      xmin, xmax = HandleLimits(args.xmin - arange * 0.05,
                                args.xmax + arange * 0.05,
                                args.user_xmin, args.user_xmax)
      ax.set_xlim([xmin, xmax])
  # labels
  if args.xlabel != 'sentinel_value':
    ax.set_xlabel(args.xlabel)
  if args.ylabel != 'sentinel_value':
    if args.mode in ('tick', 'barcode', 'point'):
      sys.stderr.write(
        'Warning, --ylabel specified while '
        '--mode=(tick, barcode or point), ylabel not displayed\n')
    else:
      ax.set_ylabel(args.ylabel)
  if args.title != 'sentinel_value':
    ax.set_title(args.title)
  # legend
  if args.is_legend:
    if args.mode not in ('contour'):
      proxy_plots = MakeProxyPlots(args)
      legend_labels = MakeLegendLabels(args)
      leg = plt.legend(proxy_plots, legend_labels, 'upper right', numpoints=1)
      leg._drawFrame = False
  # aspect ratio
  if args.aspect_equal:
    ax.axis('equal')


def main():
  usage = '%(prog)s file1 file2 file3... [options]\n\n'
  description = ('%(prog)s is a tool to produce quick plots. col1 '
                 'of input file is x value col2 is y value. If '
                 'the --mode is column/bar/hist then only col1 is '
                 'used.')
  parser = ArgumentParser(usage=usage, description=description)
  InitArguments(parser)
  args = parser.parse_args()
  CheckArguments(args, parser)
  fig, pdf = InitImage(args)
  ax = EstablishAxes(fig, args)

  data_list = ReadFiles(args)
  PlotData(data_list, ax, args)

  CleanAxis(ax, args)
  WriteImage(fig, pdf, args)


if __name__ == '__main__':
    main()
