import numpy as np
import h5py as h5
import PypersPlots as pp
import extractor as extr
import colorcet as cc
readdir = "/Users/jesus/lab/cSPEV/tables/CHAMBA_v2.2/"
errName = "I1Error500x500-newRMA.h5"
spTable = readdir + "spTable_ng256nc250-fit.h5"
plotname = 'harmonics'
dset = 'I1exact'
cblabel = r"$\tilde{I}_{1}$"
cbmin=1e-6
cbmax=1.0
v1label=r"$\log\, \gamma$"
v2label=r"$\log\, \mathcal{X}$"
theCmap = cc.cm['diverging_rainbow_bgymr_45_85_c67_r']
N = 150
chi, gamma = extr.hdf5Extract1D(errName, ['chi1D', 'gamma1D'])
I1 = extr.hdf5Extract2D(errName, 'I1exact')
fig, ax = pp.initPlot()
CM = pp.theGradient(ax,gamma,chi,I1.T, (1e-6, 1.),cmap=theCmap, LNorm=True, xylog=True)
CB = pp.setColorBar(CM,fig,ax,cblabel=r"$\mathcal{I}_{1}$",pad=0.05, borders=True, borcol=['w','k'])
pp.decor(ax,ylabel=r"$\mathcal{X}$",xlabel=r"$\mathcal{L}$")
pp.printer(fig,'gradient',onscreen=True)#,savedir="tests/",printPNG=True)#
