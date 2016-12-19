#!/usr/bin/env python -tt
from __future__ import (absolute_import, division, print_function)

def latexify():
    '''Define the matplotlib preamble.

    The PGF preamble corresponds to the latex preamble in MNRAS class. It
    can be modified to whatever LaTeX preamble needed.
    '''
    import matplotlib as mpl
    mpl.use('pgf')
    from matplotlib.backends.backend_pgf import FigureCanvasPgf
    mpl.backend_bases.register_backend('pdf', FigureCanvasPgf)

    rc_custom_preamble = {
        "savefig.transparent": True,
        "savefig.dpi": 300,
        "pgf.rcfonts": False,
        "pgf.preamble": [
            r"\let\mit=\mathnormal"
            r"\DeclareRobustCommand\cal{\@fontswitch{\relax}{\mathcal}}",
            r"\SetSymbolFont{symbols}{bold}{OMS}{cmsy}{b}{n}",
            r"\DeclareSymbolFont{UPM}{U}{eur}{m}{n}",
            r"\SetSymbolFont{UPM}{bold}{U}{eur}{b}{n}",
            r"\DeclareSymbolFont{AMSa}{U}{msa}{m}{n}",
            r"\usepackage{amsmath}",
            r"\usepackage{txfonts}"
        ],
    }
    mpl.rcParams.update(rc_custom_preamble)
    return

def dataExtract3col(filename, N, cols=(0,1,2)):
    '''contourExtract4(filename, N, cols=(0,1,2))

    Four columns extraction routine. Getting data ready for contour
    plotting.

    filename: string
    Name of the file with at least four columns.

    N: int
    Size of the temporal arrays to generate the grid.

    cols: tuple
    Tuple of three int referring to the columns to be read.
    '''
    import numpy as np
    import scipy.interpolate
    v1, v2, tt = np.loadtxt(filename, usecols=cols, unpack=True)
    v1i = np.linspace(v1.min(), v1.max(), N)
    v2i = np.linspace(v2.min(), v2.max(), N)
    ti = scipy.interpolate.griddata((v1, v2), tt,
                                    (v1i[None,:], v2i[:,None]),
                                    method='cubic', rescale=True
    )
    return v1i, v2i, ti

def hdf5Extract3D(h5file, ds1, ds2, ds3):
    ''' hdf5Extraxt(h5file)

    Extract data from an HDF5 data file.

    h5file: string
    File name.

    ds1,ds2: strings
    1D data set names

    ds3:
    2D  data set names
    '''
    import h5py as h5

    h5f = h5.File(h5file, 'r')
    v1 = emissTable[ds1][:]
    v2 = emissTable[ds2][:]
    v3 = emissTable[ds3][:,:]

    return v1,v2,v3

def initPlot():
    '''Initializing single plot.
    '''
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    return fig,ax

def initmPlot(nrows=1,ncols=2,cbloc="right",cbmode="single",landscape=True):
    '''Initializing multiple plots.


    Return:
    * fig: Figure instance.

    * grid:

    '''
    import matplotlib.pyplot as plt
    from matplotlib import figure
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
                    cbar_mode="single"
    )

    return fig,grid

def plotxy(fig,ax,x,y,log=True):
    import matplotlib.pyplot as plt
    plt.figure(fig.number)
    if log:
        ax.loglog(x,y)
    else:
        ax.plot(x,y)
    return

def theContours(fig, ax, v1, v2, t, numl=7, log=True, fmt='%1.0f', levs=[1], labelpos=[0], rasterd=True):
    ''' Setting the contour lines.
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    plt.figure(fig.number)
    if len(levs) == 1 and levs[0] == 1:
        CS = ax.contour(v1, v2, t, colors='k', lw=1.0, rasterized=rasterd)
    else:
        if log:
            levs = np.logspace(np.log10(t.min()), np.log10(t.max()), num=numl)
        else:
            levs = np.linspace(t.min(), t.max(), num=numl)
        CS = ax.contour(v1, v2, t, levels=levs, colors='k', lw=1.0, rasterized=rasterd)


    if len(labelpos) == 1 and labelpos[0] == 0:
        ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=False, rasterized=rasterd)
    else:
        ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=labelpos, rasterized=rasterd)
    return CS

def theGradient(fig, ax, v1, v2, t, cbmin, cbmax, v1label=r"$x$", v2label="$y$", tlabel="$z$", LNorm=True, cmap='Accent', xlim=(0.0,3.0), ylim=(0.0,3.0), subs=[1.0], rasterd=True):
    '''Setting the contour gradient plot.
    '''
    import matplotlib.pyplot as plt
    import matplotlib.colors as col
    import matplotlib.ticker as ticker
    import numpy as np

    plt.figure(fig.number)

    if LNorm:
        CM = ax.pcolormesh(v1, v2, t,
                           cmap=cmap,
                           norm=col.LogNorm(vmin=cbmin, vmax=cbmax),
                           rasterized=rasterd
        )
        cbticks = ticker.LogLocator(base=10.0, subs=subs)
        CB = fig.colorbar(CM, ax=ax,
                          pad=0.0,
                          extendrect=True,
                          extend='both',
                          extendfrac=0.01,
                          ticks=cbticks,
                          format=ticker.LogFormatter(base=10.0, labelOnlyBase=False)
        )
    else:
        CM = ax.pcolormesh(v1, v2, t,
                           cmap=cmap,
                           norm=col.Normalize(vmin=cbmin, vmax=cbmax),
                           rasterized=rasterd
        )
        CB = fig.colorbar(CM, ax=ax,
                          pad=0.0,
                          extendrect=True,
                          extend='both',
                          extendfrac=0.01
        )

    CB.ax.tick_params(which='major', length=0, width=1.5, labelsize=16)
    CB.set_label(tlabel, size=20)
    CB.outline.set_linewidth(1.5)
    CB.cmap.set_under(color='k')
    CB.cmap.set_over(color='w')

    ax.minorticks_on()
    ax.tick_params(axis='both', which='minor', length=3, width=1.5)
    ax.tick_params(axis='both', which='major', length=6, width=1.5, labelsize=16)
    ax.set_xlabel(v1label, size=20)
    ax.set_ylabel(v2label, size=20)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    return CM,CB

def printer(fig, ax, fname, savedir, pgfsavedir, onscreen=False, rasterd=True, printPNG=False, printPDF=True):
    import matplotlib.pyplot as plt
    plt.figure(fig.number)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.5)
        ax.spines[axis].set_color('black')
    plt.subplots_adjust(left=0.10, bottom=0.13, right=0.95, top=0.95)

    fullname = savedir + fname
    if onscreen:
        plt.title(fname)
        plt.show()
        plt.clf()
    else:
        if  printPNG:
            fig.savefig(fullname + '.png', format='png', dpi=300, rasterized=rasterd)
        if printPDF:
            fig.savefig(fullname + '.pdf', format='pdf', dpi=300, rasterized=rasterd)
        fig.savefig(fullname + '.pgf')
        im = sp.Popen(['imgtops', '-3', '-e', fullname + '-img0.png'], stdout=sp.PIPE)
        imEPS, imerr = im.communicate()
        imEPSf = open(fullname + '-img0.eps', 'w')
        imEPSf.write(imEPS)
        imEPSf.close()
        im = sp.Popen(['imgtops', '-3', '-e', fullname + '-img1.png'], stdout=sp.PIPE)
        imEPS, imerr = im.communicate()
        imEPSf = open(fullname + '-img1.eps', 'w')
        imEPSf.write(imEPS)
        imEPSf.close()

        # MODIF PGF FILE (PNG -> EPS & LOC -> FULL LOC)
        replacements = {'png':'eps', fname:pgfdir + fname}
        lines = []
        with open(fullname + '.pgf') as infile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                lines.append(line)
        with open(fullname + '.pgf', 'w') as outfile:
            for line in lines:
                outfile.write(line)

        if delPNGs:
            for pngIM in ['-img0', '-img1']:
                sp.call(['rm', '-f', fullname + pngIM + '.png'])
    print('  Printing: done')

    return
