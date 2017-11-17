import numpy as np
import PypersPlots as pp
x = np.linspace(0.0, 2.0*np.pi, 50)
pp.latexify()
fig,ax = pp.initPlot()
ax.plot(x,np.sin(x))
ax.plot(x,np.cos(x))
pp.decor(ax,
         xlim=(0.0,2.0*np.pi),
         ylim=(-1.0,1.0),
         ylabel=r"$\mathcal{L}$",
         xlabel=r"$\mathcal{X}$")
pp.printer(fig,'sin',tight=True,printPNG=True)
