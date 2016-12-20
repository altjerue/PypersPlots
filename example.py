import numpy as np
import PypersPlots as pp
pp.latexify(1.2)
x = np.linspace(0.0, 2.0*np.pi, 50)
fig,ax = pp.initPlot()
ax.plot(x,np.sin(x))
ax = pp.decor(ax,xlim=(0.0,2.0*np.pi),ylim=(-1.0,1.0),ylabel=r"$\mathcal{L}$",xlabel=r"$\mathcal{X}$")
pp.printer(fig,ax,'some example')#,onscreen=True)

# Generate random data file

# Read random data file

#pp.dataExtract3col()

# define matplotlib preamble
#pp.latexify()

# print plots (onscreen ON/OFF)
