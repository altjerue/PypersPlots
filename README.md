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

![](README_figs/fields_and_streams.png)

To produce these examples go to the wiki. I will be placing more elaborated stuff there.

# Recomendations and observations #

For a good interactive plotting I suggest using IPython. Once inside call
the magic command `%%matplotlib osx`, if you are using macOS:

``` jupyter-notebook
%%matplotlib osx
```

Something that must be pointed out is that the PNG image will not have the
correct characters. However the PDF and PGF will.

This module is under development. Any issue, comment and upgrades are most welcome.
