#!/usr/bin/env python -tt

def figsize(scale,landscape=True):
    import numpy as np
    fig_width_pt = 469.755                          # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    if landscape:
        fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
        fig_height = fig_width*golden_mean              # height in inches
    else:
        fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
        fig_height = fig_width/golden_mean              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

def latexify(fscale=1.0):
    """Define the matplotlib preamble.

    The PGF preamble corresponds to the latex preamble in MNRAS class. It
    can be modified to whatever LaTeX preable needed.
    """
    import matplotlib as mpl
    mpl.use('pgf')
    from matplotlib.backends.backend_pgf import FigureCanvasPgf
    mpl.backend_bases.register_backend('pdf', FigureCanvasPgf)
    mpl.backend_bases.register_backend('png', FigureCanvasPgf)
    rc_mnras_preamble = {
        #"backend": "pgf"
        "text.usetex": False,        # use LaTeX to write all text
        "axes.labelsize": 16,        # fontsize for x and y labels (was 10)
        "legend.fontsize": 10,       # was 10
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.figsize": figsize(fscale),     # default fig size of 0.9 textwidth
        "figure.autolayout": True,
        "savefig.transparent": True,
        "savefig.dpi": 300,
        "pgf.texsystem": "lualatex",        # change this if using xelatex or lualatex
        "pgf.rcfonts": False,
        "pgf.preamble": [
            r"\let\mit=\mathnormal",
            r"\DeclareRobustCommand\cal{\@fontswitch{\relax}{\mathcal}}",
            r"\SetSymbolFont{symbols}{bold}{OMS}{cmsy}{b}{n}",
            r"\DeclareSymbolFont{UPM}{U}{eur}{m}{n}",
            r"\SetSymbolFont{UPM}{bold}{U}{eur}{b}{n}",
            r"\DeclareSymbolFont{AMSa}{U}{msa}{m}{n}",
            r"\usepackage{amsmath}",
            r"\usepackage{txfonts}",
        ]
    }
    mpl.rcParams.update(rc_mnras_preamble)

def initPlot(nrows=1,ncols=1,landscape=True):
    """Initializing plot.

    Return:

    * fig: Figure class.

    """
    import matplotlib.pyplot as plt
    from matplotlib import figure

    if landscape:
        w,h = figure.figaspect(2.0/3.0)
    else:
        w,h = figure.figaspect(1.5)
    plt.clf()
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols)
    fig.set_size_inches(w, h)

    return fig,ax

def initGrid(nrows=1,ncols=1,cbloc="right",cbmode="each",landscape=True):
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import AxesGrid

    if landscape:
        w,h = figure.figaspect(2.0/3.0)
    else:
        w,h = figure.figaspect(1.5)
    fig = plt.figure(figsize=(w, h))

    grid = AxesGrid(fig, 111,
                    nrows_ncols=(nrows, ncols),
                    axes_pad=0.0,
                    share_all=True,
                    label_mode="L",
                    cbar_location=cbloc,
                    cbar_mode=cbmode
    )
    return grid

def decor(ax,xlim=None,ylim=None,xlabel=r"$x$",ylabel=r"$y$",lw=1.0,tlabelsize=10,minticks_on=True,gridon=False):
    if minticks_on:
        ax.minorticks_on()
        ax.tick_params(axis='both', which='minor', length=3, width=lw)
    ax.tick_params(axis='both', which='major', length=6, width=lw, labelsize=tlabelsize)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if xlim == None:
        xlim = ax.get_xlim()
    if ylim == None:
        ylim = ax.get_ylim()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(lw)
        ax.spines[axis].set_color('black')

    if gridon:
        ax.grid()

def printer(fig,fname, savedir="./", onscreen=False, rasterd=True, printPNG=False, printPDF=True, delPNG=True):
    import matplotlib.pyplot as plt
    if onscreen:
        fig.suptitle(fname)
        plt.show()
    else:
        import subprocess as sp
        import os
        fullname = savedir + fname
        if  printPNG:
            fig.savefig(fullname + '.png', format='png', rasterized=rasterd)
        if printPDF:
            fig.savefig(fullname + '.pdf', format='pdf', rasterized=rasterd)

        fig.savefig(fullname + '.pgf', format='pgf', rasterized=True)
        counter = 0
        for lsitem in os.listdir(savedir):
            img_name = "-img%d" % (counter)
            if lsitem.endswith(img_name + ".png"):
                im = sp.Popen(['imgtops', '-3', '-e', fullname + img_name + ".png"], stdout=sp.PIPE)
                imEPS, imerr = im.communicate()
                imEPSf = open(fullname + img_name + ".eps", 'w')
                imEPSf.write(imEPS)
                imEPSf.close()
                if delPNG:
                    sp.call(['rm', '-f', fullname + img_name + '.png'])
                counter += 1

        # MODIF PGF FILE (PNG -> EPS & LOC -> FULL LOC)
        replacements = {'png':'eps', fname:savedir + fname}
        lines = []
        with open(fullname + '.pgf') as infile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                lines.append(line)
        with open(fullname + '.pgf', 'w') as outfile:
            for line in lines:
                outfile.write(line)

    print('  Printing: done')

def theContours(ax, v1, v2, t, numl=None, clabels=False, logsep=False, fmt='%1.0f', levs=[1], labelpos=[0], rasterd=True, colors='k'):
    """ Setting the contour lines.
    """
    import numpy as np
    if numl==None:
        if len(levs) == 1 and levs[0] == 1:
            CS = ax.contour(v1, v2, t, colors=colors, lw=1.0, rasterized=rasterd)
        else:
            CS = ax.contour(v1, v2, t, levels=levs, colors=colors, lw=1.0, rasterized=rasterd)
    else:
        if logsep:
            levs = np.logspace(np.log10(t.min()), np.log10(t.max()), num=numl)
        else:
            levs = np.linspace(t.min(), t.max(), numl)
        CS = ax.contour(v1, v2, t, levels=levs, colors=colors, lw=1.0, rasterized=rasterd)

    if clabels:
        if len(labelpos) == 1 and labelpos[0] == 0:
            ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=False)
        else:
            ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=labelpos)
    return CS

def theGradient(fig, ax, v1, v2, t, cbmin, cbmax, v1label=r"$x$", v2label="$y$", tlabel="$z$", LNorm=True, cmap=None, xlim=(0.0,3.0), ylim=(0.0,3.0), rasterd=True):
    """Setting the contour gradient plot.
    """
    if cmap == None:
        import colorcet as cc
        cmap = cc.cm['bgy']
    if LNorm:
        CM = ax.pcolormesh(v1, v2, t,
                           cmap=cmap,
                           norm=col.LogNorm(vmin=cbmin, vmax=cbmax),
                           rasterized=rasterd
        )
    else:
        CM = ax.pcolormesh(v1, v2, t,
                           cmap=cmap,
                           norm=col.Normalize(vmin=cbmin, vmax=cbmax),
                           rasterized=rasterd
        )
    return CM

def setColorBar(TT,fig,ax,log=False,blw=1.0,cblabel=r"$z$",subs=[1.0]):
    import matplotlib.colors as col
    import matplotlib.ticker as ticker

    if log:
        cbticks = ticker.LogLocator(base=10.0, subs=subs)
        CB = fig.colorbar(TT, ax=ax,
                          pad=0.0,
                          extendrect=True,
                          extend='both',
                          extendfrac=0.01,
                          ticks=cbticks,
                          format=ticker.LogFormatter(base=10.0, labelOnlyBase=False)
        )
    else:
        CB = fig.colorbar(TT, ax=ax,
                          pad=0.0,
                          extendrect=True,
                          extend='both',
                          extendfrac=0.01
        )
    CB.ax.tick_params(which='major', length=0)
    CB.set_label(cblabel)
    CB.outline.set_linewidth(blw)
    CB.cmap.set_under(color='k')
    CB.cmap.set_over(color='w')
    return CB

############################################################################
#           EXTRACTING DATA
############################################################################

def dataExtract3col(filename, N, cols=(0,1,2)):
    """contourExtract4(filename, N, cols=(0,1,2))

    Four columns extraction routine. Getting data ready for contour
    plotting.

    filename: string
    Name of the file with at least four columns.

    N: int
    Size of the temporal arrays to generate the grid.

    cols: tuple
    Tuple of three int referring to the columns to be read.
    """
    #import numpy as np
    import scipy.interpolate
    v1, v2, tt = np.loadtxt(filename, usecols=cols, unpack=True)
    v1i = np.linspace(v1.min(), v1.max(), N)
    v2i = np.linspace(v2.min(), v2.max(), N)
    ti = scipy.interpolate.griddata((v1, v2), tt,
                                    (v1i[None,:], v2i[:,None]),
                                    method='cubic', rescale=True
    )
    return v1i, v2i, ti

def hdf5Extract2D(h5file, ds1, ds2):
    """ hdf5Extraxt(h5file)

    Extract data from an HDF5 data file.

    h5file: string
    File name.

    ds1,ds2: strings
    1D data set names

    """
    import h5py as h5

    h5f = h5.File(h5file, 'r')
    v1 = emissTable[ds1][:]
    v2 = emissTable[ds2][:]

    return v1,v2

def hdf5Extract3D(h5file, ds1, ds2, ds3):
    """ hdf5Extraxt(h5file)

    Extract data from an HDF5 data file.

    h5file: string
    File name.

    ds1,ds2: strings
    1D data set names

    ds3:
    2D  data set names
    """
    import h5py as h5

    h5f = h5.File(h5file, 'r')
    v1 = emissTable[ds1][:]
    v2 = emissTable[ds2][:]
    v3 = emissTable[ds3][:,:]

    return v1,v2,v3
