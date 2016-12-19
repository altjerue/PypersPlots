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

def dataExtract3col(filename, N, cols=(0,1,2)):
    '''contourExtract4(filename, N, cols=(0,1,2))

    Four columns extraction routine. Getting data ready for contour
    plotting.

    filename: string
    Name of the file with at least four columns.

    N: int
    Size of the temporal arrays to generate the grid.
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


def hdf5Extract():

    return

def theContours(fig, v1, v2, t, numl=7, log=True, fmt='%1.0f', levs=[0], labelpos=[0], rasterd=True):
    ''' Setting the contour lines.
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    plt.figure(fig.number)
    if len(levs) == 1 and levs[0] == 0:
        if log:
            levs = np.logspace(np.log10(t.min()), np.log10(t.max()), num=numl)
        else:
            levs = np.linspace(t.min(), t.max(), num=numl)

    CS = plt.contour(v1, v2, t, levels=levs, colors='k', linestyle = 'dotted', lw=2.0, rasterized=rasterd)
    if len(labelpos) == 1 and labelpos[0] == 0:
        plt.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=False, rasterized=rasterd)
    else:
        plt.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=labelpos, rasterized=rasterd)
    return CS

def theGradient(v1, v2, t, cbmin, cbmax, v1label=r"$x$", v2label="$y$", tlabel="$z$", LNorm=True, cmap='Accent', xlim=(0.0,3.0), ylim=(0.0,3.0), subs=[1.0], rasterd=True):
    '''Setting the contour gradient plot.
    '''
    mpl.use('pgf')

    import matplotlib.pyplot as plt
    import matplotlib.colors as col
    import numpy as np

    fig = plt.gcf()
    ax = fig.add_subplot(111)

    ticksize = 14
    axfont = {'family' : 'sans-serif',
              'weight' : 'normal'
              }

    if LNorm:
        import matplotlib.ticker as ticker
        CM = plt.pcolormesh(v1, v2, t, cmap=cmap,
                            norm=col.LogNorm(vmin=cbmin, vmax=cbmax),
                            rasterized=rasterd)

        cbticks = ticker.LogLocator(base=10.0, subs=subs)
        CB = plt.colorbar(CM, ax=ax, pad=0.0, extendrect=True, extend='both', extendfrac=0.01, ticks=cbticks, format=ticker.LogFormatter(base=10.0,labelOnlyBase=False))
    else:
        CM = plt.pcolormesh(v1, v2, t, cmap=cmap,
                            norm=col.Normalize(vmin=cbmin, vmax=cbmax),
                            rasterized=rasterd)
        CB = plt.colorbar(CM, ax=ax, extendrect=True, extend='both')

    CB.ax.tick_params(which='major', length=0, width=1.5, labelsize=ticksize)
    CB.set_label(tlabel, labelpad=10, size=20, **axfont)
    CB.outline.set_linewidth(1.5)
    CB.cmap.set_under(color='w')
    CB.cmap.set_over()
    CB.ax.set_rasterized(rasterd)

    ax.minorticks_on()
    ax.tick_params(which='minor', length=3, width=1.5, )
    ax.tick_params(which='major', length=6, width=1.5, labelsize=ticksize)
    ax.ticklabel_format(axis='both', **axfont)
    ax.set_xlabel(v1label, labelpad=15, size=20)
    ax.set_ylabel(v2label, labelpad=10, size=20)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.5)
        ax.spines[axis].set_color('black')

    plt.xlim(xlim)
    plt.ylim(ylim)

    ax.set_rasterized(rasterd)
    plt.subplots_adjust(left=0.10, bottom=0.13, right=0.95, top=0.95)

    return fig

def printer(fig, name, onscreen=False, rasterd=True):
    import matplotlib.pyplot as plt
    plt.figure(fig.number)

    if onscreen:
        #plt.title(name)
        plt.draw()
    else:
        plt.savefig(name + '.pdf', format='pdf', dpi=300, rasterized=rasterd)
        plt.savefig(name + '.png', format='png', dpi=300, rasterized=rasterd)
        plt.savefig(name + '.pgf')
    plt.clf()
    return

#    plt.show()
#    CS = theContours(v1, v2, t, numl=nl)

###### EXPONENT SEARCHER   ################
#        expmax = np.ceil(np.log10(np.abs(cbmax))).astype(int)
#        expmin = np.floor(np.log10(np.abs(cbmax))).astype(int)
#        cbticks = np.outer(np.power(10.,range(-1,3)),np.arange(1.,10.)).flatten()
