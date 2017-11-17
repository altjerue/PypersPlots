import numpy as np
import PypersPlots as pp
import extractor as ext
import colorcet as cc
N = 300
data = "/Users/jesus/RemoteRepos/GitHub/PypersPlots/temperature.dat"
thecmap = 'gist_ncar'
x, y, T = ext.dataExtract3col(data, (N,N))
pp.latexify(ratio=1.2)
fig, ax = pp.initPlot()
fig.canvas.draw_idle()
CM = pp.theGradient(ax, x, y, T, (0.0, 1.e2), cmap=thecmap)
pp.decor(ax,xlabel=r"$\mathcal{X}$",ylabel=r"$\mathcal{Y}$")
CB = pp.setColorBar(CM,fig,ax,cblabel=r"$\mathcal{L}$",pad=0.0)
pp.printer(fig, 'gradient2', onscreen=True)#savedir="tests/",printPNG=True)#
