from __future__ import division

def figsize(scale, landscape=True, ratio=None, txtwidth=None):
    import numpy as np
    if txtwidth is None:          # Get this from LaTeX using \the\textwidth
        fig_width_pt = 469.755
    else:
        fig_width_pt = txtwidth
    inches_per_pt = 1.0/72.27     # Convert pt to inch
    if ratio is None:
        golden_mean = 2.0/(np.sqrt(5.0)-1.0)  # Aesthetic ratio (you could change this)
        ratio = golden_mean
    if landscape:
        fig_width = fig_width_pt*inches_per_pt*scale   # width in inches
        fig_height = fig_width/ratio                   # height in inches
    else:
        fig_height = fig_width_pt*inches_per_pt*scale  # height in inches
        fig_width = fig_height/ratio                   # width in inches
    fig_size = [fig_width,fig_height]
    return fig_size

def latexify(fscale=1.0, ratio=None, landscape=True, txtwdth=None, edgecol='k'):
    """Define the matplotlib preamble.

    The LaTeX preamble here corresponds to the preamble in MNRAS class. It
    can be modified to whatever LaTeX preable needed.

    PARAMETERS:

    fscale
    ------
    The size of the plot in terms of its size and height. Default is 1.0.

    ratio
    -----
    Aspect ratio of the figure. The default is the golden ratio.

    landscape
    ---------
    Landscape if True. Portrait if False.

    twtwdth
    -------
    Width of the plot in pts. The default is the text width of a standard
    LaTeX report. To know the text width in latex just write \the\textwidth
    (or \the\columnwidth for article class) to get this value.

    edgecol
    -------
    Color of the borders and ticks. Default is black ('k'). For dark
    backgrounds use 'w' for white borders.
    """
    import matplotlib as mpl
    from matplotlib.backends.backend_pgf import FigureCanvasPgf
    #mpl.use('pgf')

    #mpl.backend_bases.register_backend('pdf', FigureCanvasPgf)
    #mpl.backend_bases.register_backend('png', FigureCanvasPgf)
    mpl.backend_bases.register_backend('pgf', FigureCanvasPgf)

    pream = [
        r"\let\mit=\mathnormal",
        r"\DeclareRobustCommand\cal{\@fontswitch{\relax}{\mathcal}}",
        r"\SetSymbolFont{symbols}{bold}{OMS}{cmsy}{b}{n}",
        r"\DeclareSymbolFont{UPM}{U}{eur}{m}{n}",
        r"\SetSymbolFont{UPM}{bold}{U}{eur}{b}{n}",
        r"\DeclareSymbolFont{AMSa}{U}{msa}{m}{n}",
        r"\usepackage{amsmath}",
        r"\usepackage{txfonts}",
    ]

    rc_mnras_preamble = {
        "text.usetex": True,        # use LaTeX to write all text
        "text.dvipnghack": True,
        "text.latex.preamble": pream,
        "text.latex.unicode": False,
        "text.latex.preamble": pream,
        "axes.labelsize": 'x-large',  # fontsize for x and y labels (was 10)
        "axes.unicode_minus": False,
        "axes.edgecolor": edgecol,
        "legend.labelspacing": 0.2,
        "legend.fancybox": False,
        "legend.framealpha": 1.0,
        "legend.edgecolor": edgecol,
        "legend.borderpad": 0.4,
        "legend.handletextpad": 0.3,
        "legend.handlelength": 1.5,
        "legend.borderaxespad": 0.7,
        "figure.figsize": figsize(fscale,
                                  landscape=landscape,
                                  ratio=ratio,
                                  txtwidth=txtwdth),
        "lines.linewidth": 1.0,
        "xtick.major.width": 1.0,
        "xtick.minor.width": 1.0,
        "xtick.major.size": 6.0,
        "xtick.minor.size": 3.0,
        "xtick.direction": 'in',
        "xtick.top": True,
        "xtick.minor.visible": True,
        "xtick.labelsize": 'medium',
        "xtick.color": edgecol,
        "ytick.major.width": 1.0,
        "ytick.minor.width": 1.0,
        "ytick.major.size": 6.0,
        "ytick.minor.size": 3.0,
        "ytick.direction": 'in',
        "ytick.right": True,
        "ytick.minor.visible": True,
        "ytick.labelsize": 'medium',
        "ytick.color": edgecol,
        "savefig.transparent": True,
        "savefig.dpi": 300,
        "savefig.bbox": 'tight',
        "savefig.pad_inches": 0.05,
        "pgf.texsystem": "pdflatex",
        #"pgf.rcfonts": False,
        #"pgf.preamble": pream
    }
    mpl.rcParams.update(rc_mnras_preamble)

def inserTeXpreamble(preamble):
    import matplotlib as mpl
    for p in preamble:
        mpl.rcParams["pgf.preamble"].append(p)
    mpl.rcParams.update()

def initPlot(nrows=1, ncols=1, redraw=True, shareY=False, shareX=False, polar=False):
    """Initializing plot.

    Return:

    * fig: Figure class.

    """
    from matplotlib import figure
    import matplotlib.pyplot as plt

    if redraw:
        plt.close('all')

    gskw = {}
    if shareY:
        gskw.update({'hspace' : 0.0})
    if shareX:
        gskw.update({'wspace' : 0.0})

    if polar:
        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, subplot_kw={'projection' : 'polar'}, sharey=shareY, sharex=shareX, gridspec_kw=gskw)
    else:
        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharey=shareY, sharex=shareX, gridspec_kw=gskw)

    return fig,ax

def decor(ax, xlim=None, ylim=None, xlabel=None, ylabel=None, xticks=True, yticks=True, xlog=False, ylog=False, labels_kw=None, ticks_kw=None, minticks_off=False, gridon=False, lw=1.0):
    from matplotlib.ticker import LogLocator
    if labels_kw is None:
        labels_kw = {}

    if ticks_kw is None:
        ticks_kw = {
            "width" : lw
        }

    if xticks:
        ax.tick_params(axis='x', which='major', **ticks_kw)
    else:
        ax.set_xticklabels([])

    if yticks:
        ax.tick_params(axis='y', which='major', **ticks_kw)
    else:
        ax.set_yticklabels([])

    if xlog:
        ax.set_xscale('log')
        ax.xaxis.set_major_locator(LogLocator(base=10.0))
        ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=range(2,10)))
    if ylog:
        ax.set_yscale('log')
        ax.yaxis.set_major_locator(LogLocator(base=10.0))
        ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=range(2,10)))

    if minticks_off:
        ax.minorticks_off()

    if xlabel is not None:
        ax.set_xlabel(xlabel, **labels_kw)
    if ylabel is not None:
        ax.set_ylabel(ylabel, **labels_kw)

    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    for axis in ax.spines.keys():
        ax.spines[axis].set_linewidth(lw)

    if gridon:
        ax.grid(which='both')

def printer(fig, fname, savedir=None, onscreen=False, rasterd=True, printPNG=False, printPDF=True, printEPS=False, delPNG=True, PNG2EPS=True):
    if onscreen:
        fig.suptitle(fname)
        fig.show()
    else:
        import subprocess as sp
        import os
        if savedir is None:
            savedir = os.getcwd() + '/'
        fullname = savedir + fname
        if  printPNG:
            fig.savefig(fullname + '.png', format='png', rasterized=rasterd, frameon=False, transparent=False)
        if printPDF:
            fig.savefig(fullname + '.pdf', format='pdf', rasterized=rasterd, frameon=False)
        if printEPS:
            fig.savefig(fullname + '.eps', format='eps', rasterized=rasterd, frameon=False)
        fig.savefig(fullname + '.pgf', format='pgf', rasterized=True, frameon=False)
        
        if PNG2EPS:

            counter = 0

            for item in os.listdir(savedir):
                img_name = "-img%d" % (counter)
                if item.endswith(img_name + ".png") and item.startswith(fname):
                    im = sp.Popen(['imgtops', '-3', '-e', fullname + img_name + ".png"], stdout=sp.PIPE)
                    imEPS, imerr = im.communicate()
                    imEPSf = open(fullname + img_name + ".eps", 'w')
                    imEPSf.write(imEPS)
                    imEPSf.close()
                    if delPNG:
                        sp.call(['rm', '-f', fullname + img_name + '.png'])
                    counter += 1

            # MODIF PGF FILE (PNG -> EPS & LOC -> FULL LOC)
            replacements = {'png':'eps', fname: savedir + fname}
            lines = []
            with open(fullname + '.pgf') as infile:
                for line in infile:
                    for src, target in replacements.iteritems():
                        line = line.replace(src, target)
                    lines.append(line)
            with open(fullname + '.pgf', 'w') as outfile:
                for line in lines:
                    outfile.write(line)

            # if printEPS:
            #     import matplotlib as mpl
            #     from pgf2eps import pgf2eps
            #     pream = mpl.rcParams["pgf.preamble"]
            #     pgf2eps(fullname, pream)

        else:

            replacements = {fname: savedir + fname}
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

def theGradient(ax, v1, v2, t, cmlim, LNorm=False, cmap=None, rasterd=True):
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

    return CM

def setColorBar(TT, fig, lax, blw=1.0, cblabel=r"$z$", subs=[1.0], pad=0.01, borders=True, borcol=[], width=1.0, size=1.0, loc='right', label_kw=None, ticks_kw=None):
    import matplotlib.colors as col
    import matplotlib.colorbar as colbar
    import matplotlib.ticker as ticker
    if label_kw is None:
        label_kw = {}
        
    if ticks_kw is None:
        ticks_kw = {}
        
    cax_kw = { 'shrink' : size,
               'aspect' : 20.0/width,
               'pad' : pad,
               'anchor': 'C'
    }

    col_kw = {}
    if borders is True:
        col_kw.update({ 'extendfrac' : 0.01,
                        'extend' : 'both',
                        'extendrect' : True
        })
    else:
        col_kw.update({'extend': 'neither'})    
        
    if type(TT.norm) == col.LogNorm:
        cbticks = ticker.LogLocator(base=10.0, subs=subs)
        col_kw.update({'ticks': cbticks})


    try:
        list(lax)
        cax,ckw = colbar.make_axes([ax for ax in lax.flat], **cax_kw)
    except TypeError:
        cax, ckw = colbar.make_axes(lax, **cax_kw)

    col_kw.update(ckw)
    CB = fig.colorbar(TT, cax=cax, use_gridspec=True, **col_kw)

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

    w, h = fig.get_size_inches()
    rect = anchor[0], anchor[1], w*wscale, h*hscale
    inax = fig.add_axes(rect)
    return inax
