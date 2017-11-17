import numpy as np
import PypersPlots as pp
import extractor as ext
from matplotlib.offsetbox import AnchoredText
from matplotlib.patheffects import withStroke

NxM = [150, 150]
data = "sL_sR_T.dat"
fname = data.split(".")[0]
sL, sR, TFS = ext.dataExtract3col(data, NxM)
sL, sR, TRS = ext.dataExtract3col(data, NxM, cols=(0,1,3))
fig, axes = pp.initPlot(ncols=2,fscale=1.25)

for ax, T, title in zip(axes.flat, [TFS, TRS], ['FS', 'RS']):
    CM = pp.theGradient(ax, sL, sR, T, (1.0, 5e2),LNorm=True)
    at = AnchoredText(title, loc=4, prop=dict(size=12),
                      pad=0., borderpad=0.5,
                      frameon=False)
    at.txt._text.set_path_effects([withStroke(foreground="w", linewidth=2)])
    ax.add_artist(at)
CB = pp.setColorBar(CM,fig,axes[1],cblabel=r"$\mathcal{L}$", subs=[1.,3.,5.])
pp.decor(axes[0],xlabel=r"$\mathcal{X}$",ylabel=r"$\mathcal{Y}$")
pp.decor(axes[1],xlabel=r"$\mathcal{X}$",yticks=False)
axes[0].set_xticks(range(-5,3))
axes[1].set_xticks(range(-5,3))

pp.printer(fig,'sL_sR_T',savedir="tests/",printPNG=True)#,onscreen=True)#
