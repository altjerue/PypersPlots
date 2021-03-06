# -*- coding: utf-8 -*-
"""This is the docstring for PypersPlots."""
from __future__ import division


def figsize(scale, landscape=True, ratio=None, txtwidth=None):
    """Control figure size."""
    import numpy as np
    if txtwidth is None:          # Get this from LaTeX using \the\textwidth
        fig_width_pt = 469.755
    else:
        fig_width_pt = txtwidth
    inches_per_pt = 1.0 / 72.27     # Convert pt to inch
    if ratio is None:
        # Aesthetic ratio (you could change this)
        golden_mean = 2.0 / (np.sqrt(5.0) - 1.0)
        ratio = golden_mean
    if landscape:
        # width in inches
        fig_width = fig_width_pt * inches_per_pt * scale
        # height in inches
        fig_height = fig_width / ratio
    else:
        # width in inches
        fig_width = fig_width_pt * inches_per_pt * scale
        # height in inches
        fig_height = fig_width * ratio
    fig_size = [fig_width, fig_height]
    return fig_size


#
#  #              #######        #     #
#  #         ##      #    ######  #   #  # ###### #   #
#  #        #  #     #    #        # #   # #       # #
#  #       #    #    #    #####     #    # #####    #
#  #       ######    #    #        # #   # #        #
#  #       #    #    #    #       #   #  # #        #
#  ####### #    #    #    ###### #     # # #        #
def latexify(fscale=1.0, ratio=None, landscape=True, txtwdth=None, edgecol='k',
             lw=1.0, tklen=6.0, interact=False):
    """Define the matplotlib preamble.

    The default LaTeX preamble here corresponds to the preamble in MNRAS class.
    It can be modified to whatever LaTeX preable needed.

    Args:
        fscale: The size of the plot in terms of its size and height.
            Default is 1.0.
        ratio: Aspect ratio of the figure.
            The default is the golden ratio.
        landscape: Orientation is landscape if True, portrait if False.
        twtwdth: Width of the plot in pts.
            The default is the text width of a standard LaTeX report. To know
            the text width in latex just write the textwidth (or the
            columnwidth for article class) to get this value.
        edgecol: Color of the borders and ticks. Default is black ('k'). For
            dark backgrounds use 'w' for white borders.
    """
    import matplotlib as mpl

    pream = [
        r"\usepackage{amssymb}",
        r"\usepackage{amsmath}",
        r"\usepackage{txfonts}",
        r"\usepackage{txgreeks}",
    ]

    rc_mnras_preamble = {
        "text.usetex": True,        # use LaTeX to write all text
        "text.latex.preamble": pream,
        "text.color": edgecol,
        "axes.linewidth": 1.25 * lw,
        "axes.labelcolor": edgecol,
        # "axes.labelsize": 'medium',  # fontsize for x and y labels (was 10)
        "axes.unicode_minus": False,
        "axes.edgecolor": edgecol,
        # "legend.framealpha": 0.2,
        "legend.facecolor": 'inherit',
        "legend.edgecolor": 'inherit',
        "legend.borderpad": 0.4,
        "legend.labelspacing": 0.2,
        "legend.handletextpad": 0.3,
        "legend.handlelength": 1.5,
        "legend.borderaxespad": 0.7,
        "legend.fancybox": False,
        "figure.figsize": figsize(fscale,
                                  landscape=landscape,
                                  ratio=ratio,
                                  txtwidth=txtwdth),
        "lines.linewidth": lw,
        "xtick.direction": 'in',
        "xtick.top": True,
        "xtick.minor.visible": True,
        "xtick.color": edgecol,
        "ytick.direction": 'in',
        "ytick.right": True,
        "ytick.minor.visible": True,
        "ytick.color": edgecol,
        "savefig.transparent": True,
        "savefig.dpi": 300,
        "savefig.bbox": 'tight',
        "savefig.pad_inches": 0.05
    }
    mpl.rcParams.update(rc_mnras_preamble)

    if interact:
        mpl.use('Qt5Agg')
        import matplotlib.pyplot as plt
        plt.ion()


def inserTeXpreamble(preamble):
    """Insert dictionary with LaTeX preamble."""
    import matplotlib as mpl
    for p in preamble:
        mpl.rcParams["pgf.preamble"].append(p)
    mpl.rcParams.update()


def initPlot(nrows=1, ncols=1, redraw=True, shareY=False, shareX=False,
             gskw=None):
    """Initialize plot.

    Return:

    * fig: Figure class.

    """
    # from matplotlib import figure
    import matplotlib.pyplot as plt

    if redraw:
        plt.close('all')

    if gskw is None:
        gskw = {}
    if shareY:
        gskw.update({'wspace': 0.0})
    if shareX:
        gskw.update({'hspace': 0.0})
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharey=shareY,
                           sharex=shareX, gridspec_kw=gskw)

    return fig, ax


#
#  #####  ######  ####   ####  #####
#  #    # #      #    # #    # #    #
#  #    # #####  #      #    # #    #
#  #    # #      #      #    # #####
#  #    # #      #    # #    # #   #
#  #####  ######  ####   ####  #    #
def decor(ax, xlim=None, ylim=None, xlabel=None, ylabel=None, labels_kw=None,
          ticks_kw=None,  minticks_off=False, gridon=False):
    """Decorate the plot you have produced."""
    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    if labels_kw is not None:
        if xlabel is not None:
            ax.set_xlabel(xlabel, **labels_kw)
        if ylabel is not None:
            ax.set_ylabel(ylabel, **labels_kw)
    else:
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
        # labels_kw = {}

    if ticks_kw is None:
        ticks_kw = {}
    else:
        ax.tick_params(axis='both', which='major', **ticks_kw)

    if minticks_off:
        ax.minorticks_off()
    else:
        ax.minorticks_on()

    # for axis in ax.spines.keys():
    #     ax.spines[axis].set_linewidth(lw)

    if gridon:
        ax.grid(which='both', zorder=-100)


#
#  #####  #####  # #    # ##### ###### #####
#  #    # #    # # ##   #   #   #      #    #
#  #    # #    # # # #  #   #   #####  #    #
#  #####  #####  # #  # #   #   #      #####
#  #      #   #  # #   ##   #   #      #   #
#  #      #    # # #    #   #   ###### #    #
def printer(fig, fname, savedir=None, pgfdir=None, onscreen=False,
            rasterd=False, printPNG=False, printPDF=True, printEPS=False,
            printPGF=False, delPNG=True, PNG2EPS=True, tight=True):
    """Print on screen or to a file the plot generated."""
    if onscreen:
        if tight:
            fig.tight_layout()
        fig.suptitle(fname)
        fig.show()
    else:
        import os
        if tight:
            fig.tight_layout()
        if savedir is None:
            savedir = os.getcwd() + '/'
        if pgfdir is None:
            pgfdir = savedir
        fullname = savedir + fname
        if printPNG:
            fig.savefig(fullname + '.png', format='png', rasterized=True,
                        transparent=False)
        if printPDF:
            fig.savefig(fullname + '.pdf', format='pdf', rasterized=rasterd)
        if printEPS:
            fig.savefig(fullname + '.eps', format='eps', rasterized=rasterd)

        if printPGF:
            fig.savefig(fullname + '.pgf', format='pgf', rasterized=True)

    print('  Printing ' + fname + ': DONE')


# The contour plots
def theContours(ax, v1, v2, t, clim=None, numl=None, clabels=False,
                logsep=False, fmt='%1.0f', levs=None, labelpos=None,
                rasterd=False, colors='k'):
    """Set contour lines."""
    import numpy as np
    if numl is None:
        if levs is None:
            CS = ax.contour(v1, v2, t, colors=colors, lw=1.0,
                            rasterized=rasterd)
        else:
            CS = ax.contour(v1, v2, t, levels=levs, colors=colors, lw=1.0,
                            rasterized=rasterd)
    else:
        if clim is None:
            clim = (t.min(), t.max())
        if logsep:
            levs = np.logspace(np.log10(clim[0]), np.log10(clim[1]), num=numl)
        else:
            levs = np.linspace(clim[0], clim[1], numl)
        CS = ax.contour(v1, v2, t, levels=levs, colors=colors, lw=1.0,
                        rasterized=rasterd)

    if clabels:
        if labelpos is None or labelpos is False:
            ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=False)
        elif labelpos:
            ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=labelpos)
        else:
            ax.clabel(CS, fontsize=10, inline=True, fmt=fmt, manual=labelpos)
    return CS


def theGradient(ax, v1, v2, t, cmlim, LNorm=False, cmap=None, rasterd=False):
    """Set the contour gradient plot."""
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

    return CM


def setColorBar(TT, fig, lax, blw=1.0, cblabel=r"$z$", subs=[1.0], pad=0.01,
                borders=True, borcol=[], width=1.0, size=1.0, loc='right',
                fmt=None, label_kw=None, ticks_kw=None):
    """Produce a color bar for gradient plots."""
    import matplotlib.colors as col
    import matplotlib.colorbar as colbar
    import matplotlib.ticker as ticker
    if label_kw is None:
        label_kw = {}

    if ticks_kw is None:
        ticks_kw = {}

    cax_kw = {'shrink': size,
              'aspect': 20.0 / width,
              'pad': pad}

    col_kw = {}
    if borders is True:
        col_kw.update({'extendfrac': 0.01,
                       'extend': 'both',
                       'extendrect': True})
    else:
        col_kw.update({'extend': 'neither'})

    if type(TT.norm) == col.LogNorm:
        cbticks = ticker.LogLocator(base=10.0, subs=subs)
        col_kw.update({'ticks': cbticks})

    try:
        list(lax)
        cax, ckw = colbar.make_axes_gridspec([ax for ax in lax.flat], **cax_kw)
    except TypeError:
        cax, ckw = colbar.make_axes_gridspec(lax, **cax_kw)

    col_kw.update(ckw)
    CB = fig.colorbar(TT, cax=cax, use_gridspec=True, format=fmt, **col_kw)

    CB.set_label(cblabel, **label_kw)
    CB.ax.tick_params(which='both', length=0.0, **ticks_kw)
    CB.outline.set_linewidth(blw)
    if borders is True:
        if len(borcol) == 0:
            CB.cmap.set_under(color='k')
            CB.cmap.set_over(color='w')
        else:
            CB.cmap.set_under(color=borcol[0])
            CB.cmap.set_over(color=borcol[1])

    CB.outline.set_figure(fig)
    return CB


def addInset(fig, anchor, wscale=0.05, hscale=0.05):
    """Produce an inset."""
    w, h = fig.get_size_inches()
    rect = anchor[0], anchor[1], w * wscale, h * hscale
    inax = fig.add_axes(rect)
    return inax
