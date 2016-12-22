This is a library intended to produce ready to publish (and not so heavy) plots.

# Prerequisites #

  * Python 2.7
  * matplotlib
  * numpy
  * scipy
  * h5py (optional)
  * colorcet (optional

# Examples #

## Linear plot ##

```python
import numpy as np
import PypersPlots as pp
pp.latexify()
x = np.linspace(0.0, 2.0*np.pi, 50)
fig,ax = pp.initPlot()
ax.plot(x,np.sin(x))
ax = pp.decor(ax,xlim=(0.0,2.0*np.pi),ylim=(-1.0,1.0),ylabel=r"$\mathcal{L}$",xlabel=r"$\mathcal{X}$")
pp.printer(fig,ax,'some example',onscreen=True)
```

## Log-log plot ##
```python
import numpy as np
import Pypersplots as pp
x = np.logspace(-1,1,50)
pp.latexify()
fig,ax = pp.initPlot()
ax.loglog(x,np.exp(x))
ax = pp.decor(ax,ylabel=r"$\mathcal{L}$",xlabel=r"$\mathcal{X}$")
pp.printer(fig,ax,'some example',onscreen=True)
```

## Contours plot ##

``` python
import numpy as np
import Pypers as pp
x, y = np.meshgrid(*(np.linspace(-1,1,500),)*2)
z = np.sin(20*x**2)*np.cos(30*y)
fig,ax = initPlot()
pp.theContours(ax,x,y,z,colors=['r','b'])
```

## Gradient plot ##

## Gradient and contours plot ##

## A more elaborate example ##

``` python
import numpy as np
import colorcet as cc
import PypersPlots as pp

pp.latexify(1.5)

fig,ax = pp.initPlot(ncols=2)

### Here we plot the electric potential and field ###
a=0.2
x, y = np.meshgrid(np.linspace(-0.2,0.4,100),np.linspace(-0.3,0.3,100))
phi = (1.0 / np.sqrt(x**2 + y**2)) - (1.0 / np.sqrt((x - a)**2 + y**2))
r1 = np.sqrt((x**2) + (y**2))
r2 = np.sqrt(((x - a)**2) + (y**2))
phi = np.ma.masked_where((r1<=0.03)|(r2<=0.03), phi)
lines = np.linspace(np.abs(phi).min()*40,np.abs(phi).max()/2, 7)
lines = np.append(lines,-lines)
lines.sort()
pp.theContours(ax[0],x,y,phi,levs=lines)

x, y = np.meshgrid(np.linspace(-0.2,0.4,15),np.linspace(-0.3,0.3,15))
r1 = np.sqrt((x**2) + (y**2))
r2 = np.sqrt(((x - a)**2) + (y**2))
Ex = -x / (x**2 + y**2) + (x - a) / ((x - a)**2 + y**2)
Ey = -y * ( 1.0 / (x**2 + y**2) - 1.0 / ((x - a)**2 + y**2) )
EE = np.sqrt(Ex**2 + Ey**2)
Ex = np.ma.masked_where((r1<=0.03)|(r2<=0.03), Ex)
Ey = np.ma.masked_where((r1<=0.03)|(r2<=0.03), Ey)
EE = np.ma.masked_where((r1<=0.03)|(r2<=0.03), EE)
EQ = ax[0].quiver(x,y,Ex/EE,Ey/EE,EE,units='xy',pivot='mid',scale_units='width',cmap='terrain')
EQcb = pp.setColorBar(EQ,fig,EQ.ax,cblabel=r'$|\mathbf{E}|$')

pp.decor(ax[0],xlabel=r'$\mathcal{X}$', ylabel=r'$\mathcal{Y}$')

### Stream lines of a flow of an incompressible fluid past a cylinder ###
Uinf = 1.
a = 1.
x,y = np.meshgrid(*(np.linspace(-3.,3.,500),)*2)
rad = np.sqrt((x**2) + (y**2))
psi = Uinf * x * (1.0 + a / (x**2 + y**2)**2)
Ux = Uinf * ( 1.0 + (a * (y**2 - x**2) / (x**2 + y**2)**2) )
Uy = - 2.0 * a * Uinf * x * y / (x**2 + y**2)**2
UU = np.sqrt(Ux**2 + Uy**2)
psi = np.ma.masked_where(rad<1.0, psi)
Ux = np.ma.masked_where(rad<1.0, Ux)
Uy = np.ma.masked_where(rad<1.0, Uy)
UU = np.ma.masked_where(rad<1.0, UU)
lines = np.linspace(0.1, 3., 10)
lines = np.append(lines,-lines)
lines.sort()
pp.theContours(ax[1],x,y,psi,levs=lines,colors='r')
stream = ax[1].streamplot(x,y,Ux/UU,Uy/UU,color=UU,linewidth=2,cmap=cc.cm['kbc'])
streamCB = pp.setColorBar(stream.lines,fig,ax[1],cblabel='speed')
pp.decor(ax[1],ylabel=r"$\mathcal{Y}$",xlabel=r"$\mathcal{X}$")

lines = np.linspace(np.abs(phi).min()*40,np.abs(phi).max()/2, 7)
lines = np.append(lines,-lines)
lines.sort()
pp.theContours(ax[0],x,y,psi,levs=lines)

pp.printer(fig,'fields and streams',onscreen=True)

```

![Output](README_figs/fields_and_streams.png)

To produce this plot it is straigh

# Recomendations and observations #

For a good interactive plotting I suggest using IPython. Once inside call
the magic command `%%matplotlib osx`, if you are using macOS:

``` jupyter-notebook
%%matplotlib osx
```

Something that must be pointed out is that the PNG image will not have the
correct characters. However the PDF and PGF will.

This module is under development. Any issue, comment and upgrades are most welcome.
