import numpy as np
import PypersPlots as pp
pp.latexify()
x, y = np.meshgrid(*(np.linspace(-0.6,0.6,500),)*2)
z = np.sin(20*x**2)*np.cos(30*y)
fig,ax = pp.initPlot()
CS = pp.theContours(ax,x,y,z)
pp.decor(ax,ylabel=r"$\mathcal{Y}$",xlabel=r"$\mathcal{X}$")

pp.printer(fig,'contours',onscreen=True)#,printPNG=True)
