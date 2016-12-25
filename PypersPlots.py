#!/usr/bin/env python -tt

def figsize(scale,landscape=True,ratio=None):
    import numpy as np
    fig_width_pt = 469.755                          # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    if ratio is None:
        golden_mean = 2.0/(np.sqrt(5.0)-1.0)        # Aesthetic ratio (you could change this)
        ratio = golden_mean
    if landscape:
        fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
        fig_height = fig_width/ratio              # height in inches
    else:
        fig_height = fig_width_pt*inches_per_pt*scale    # width in inches
        fig_width = fig_height/ratio              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

def latexify(fscale=1.0,ratio=None,landscape=True):
    """Define the matplotlib preamble.

    The PGF preamble corresponds to the latex preamble in MNRAS class. It
    can be modified to whatever LaTeX preable needed.
    """
    import matplotlib as mpl
    from matplotlib.backends.backend_pgf import FigureCanvasPgf
    mpl.backend_bases.register_backend('pdf', FigureCanvasPgf)
    mpl.backend_bases.register_backend('png', FigureCanvasPgf)
    mpl.backend_bases.register_backend('pgf', FigureCanvasPgf)
    rc_mnras_preamble = {
        "text.usetex": False,        # use LaTeX to write all text
        "axes.labelsize": 12,        # fontsize for x and y labels (was 10)
        "legend.fontsize": 10,       # was 10
        "figure.figsize": figsize(fscale,landscape=landscape, ratio=ratio),
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

def initPlot(nrows=1,ncols=1,landscape=True,fscale=1.0,ratio=None):
    """Initializing plot.

    Return:

    * fig: Figure class.

    """
    latexify(fscale=fscale,ratio=ratio,landscape=landscape)
    from matplotlib import figure
    import matplotlib.pyplot as plt

    wh = plt.rcParams['figure.figsize']
    plt.close('all')
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols)
    fig.set_size_inches(wh[0],wh[1])

    return fig,ax

def initGrid(nrows=1,ncols=1,cbloc="right",cbmode="each",landscape=True,fscale=1.0,ratio=None):
    """
    Function that generates the grid of plots.

    Parameters
    ----------
    nrows : int
    ncols : int
    cbloc : str
            right, top
    cbmode : str
    landscape : bool

    Returns
    -------
    fig: Figure
    ax : array_like
    """
    latexify(fscale=fscale,ratio=ratio,landscape=landscape)
    import matplotlib.pyplot as plt
    from matplotlib import figure
    from mpl_toolkits.axes_grid1 import AxesGrid

    wh = plt.rcParams['figure.figsize']
    plt.close('all')

    fig = plt.figure(figsize=(wh[0],wh[1]))
    grid = AxesGrid(fig, 111,
                    nrows_ncols=(nrows, ncols),
                    add_all=True,
                    axes_pad=0.,
                    share_all=True,
                    label_mode="L",
                    cbar_location=cbloc,
                    cbar_mode=cbmode,
    )
    return fig, grid

def decor(ax,xlim=None,ylim=None,xlabel=r"$x$",ylabel=r"$y$",lw=1.0,tlabelsize=10,minticks_on=True,gridon=False):
    if minticks_on:
        ax.minorticks_on()
        ax.tick_params(axis='both', which='minor', length=3, width=lw)
    ax.tick_params(axis='both', which='major', length=6, width=lw, labelsize=tlabelsize)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(lw)
        ax.spines[axis].set_color('black')

    if gridon:
        ax.grid()

def printer(fig,fname, savedir="./", onscreen=False, rasterd=True, printPNG=False, printPDF=True, delPNG=True):
    if onscreen:
        #import matplotlib.pyplot as plt
        fig.suptitle(fname)
        fig.set_tight_layout({'pad':0.1})
        fig.show()
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

## The contour plots
def theContours(ax, v1, v2, t, clim=None, numl=None, clabels=False, logsep=False, fmt='%1.0f', levs=None, labelpos=None, rasterd=True, colors='k'):
    """ Setting the contour lines.
    """
    import numpy as np
    if numl is None:
        if levs is None:
            CS = ax.contour(v1, v2, t, colors=colors, lw=1.0, rasterized=rasterd)
        else:
            CS = ax.contour(v1, v2, t, levels=levs, colors=colors, lw=1.0, rasterized=rasterd)
    else:
        if clim is None:
            clim = (t.min(), t.max())
        if logsep:
            levs = np.logspace(np.log10(clim[0]), np.log10(clim[1]), num=numl)
        else:
            levs = np.linspace(clim[0], clim[1], numl)
        CS = ax.contour(v1, v2, t, levels=levs, colors=colors, lw=1.0, rasterized=rasterd)

    if clabels:
        if labelpos is None or labelpos is False:
            ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=False)
        elif labelpos:
            ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=labelpos)
        else:
            ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=labelpos)
    return CS

def theGradient(ax, v1, v2, t, cmlim, v1label=r"$x$", v2label="$y$", tlabel="$z$", LNorm=False, cmap=None, xlim=(0.0,3.0), ylim=(0.0,3.0), rasterd=True, xlog=False, ylog=False, xylog=False):
    """Setting the contour gradient plot.
    """
    import matplotlib.colors as col

    if cmap is None:
        import colorcet as cc
        cmap = cc.cm['bgy']

    cm_min = cmlim[0]
    cm_max = cmlim[1]

    if LNorm:
        CM = ax.pcolormesh(v1, v2, t,
                           cmap=cmap,
                           norm=col.LogNorm(vmin=cm_min, vmax=cm_max),
                           rasterized=rasterd
        )
    else:
        CM = ax.pcolormesh(v1, v2, t,
                           cmap=cmap,
                           norm=col.Normalize(vmin=cm_min, vmax=cm_max),
                           rasterized=rasterd
        )

    if xylog:
        xlog = ax.set_xscale('log')
        ylog = ax.set_yscale('log')
    elif xlog:
        ax.set_xscale('log')
    elif ylog:
        ax.set_yscale('log')

    return CM

def setColorBar(TT,fig,cbax,log=False,blw=1.0,cblabel=r"$z$",subs=[1.0],pad=0.1,borders=True, borcol=[]):
    import matplotlib.colors as col
    import matplotlib.ticker as ticker
    from mpl_toolkits.axes_grid1.axes_grid import CbarAxes

    kw = { 'extendfrac' : 0.01,
           'extend' : 'both'
    }

    if type(cbax) == CbarAxes:
        ax = None
        cax = cbax
    else:
        ax = cbax
        cax = None
        kw.update({'pad': pad})

    if log:
        cbticks = ticker.LogLocator(base=10.0, subs=subs)
        CB = fig.colorbar(TT, cax=cax, ax=ax,
                          extendrect = True,
                          ticks = cbticks,
                          format = ticker.LogFormatter(base=10.0, labelOnlyBase=False),
                          **kw
        )
    else:
        CB = fig.colorbar(TT, cax=cax, ax=ax,
                          extendrect=True,
                          **kw
        )
    CB.set_label(cblabel)
    CB.ax.tick_params(which='major', length=0)
    CB.outline.set_linewidth(blw)
    if borders is True:
        if len(borcol) == 0:
            CB.cmap.set_under(color='k')
            CB.cmap.set_over(color='w')
        else:
            CB.cmap.set_under(color=borcol[0])
            CB.cmap.set_over(color=borcol[1])
    return CB
