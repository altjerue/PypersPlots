This is a library intended to produce ready to publish (and not so heavy) plots.

# Prerequisites #

  * Python 2.7
  * matplotlib
  * numpy
  * scipy
  * h5py
  * [colorcet](https://bokeh.github.io/colorcet/) (optional)
  * [imgtops](http://imgtops.sourceforge.net/)

# Examples #

## Linear plot ##

```python
import numpy as np
import PypersPlots as pp
pp.latexify()
x = np.linspace(0.0, 2.0*np.pi, 50)
fig,ax = pp.initPlot()
ax.plot(x,np.sin(x))
ax.plot(x,np.cos(x))
pp.decor(ax,xlim=(0.0,2.0*np.pi),ylim=(-1.0,1.0),ylabel=r"$\mathcal{L}$",xlabel=r"$\mathcal{X}$")
pp.printer(fig,'sin')
```
![](README_figs/sin.png)

## Contours plot ##

``` python
import numpy as np
import Pypers as pp
x, y = np.meshgrid(*(np.linspace(-1,1,500),)*2)
z = np.sin(20*x**2)*np.cos(30*y)
fig,ax = initPlot()
pp.theContours(ax,x,y,z,colors=['r','b'])
```
![](README_figs/contours.png)

## Gradient plot ##

## More elaborate example examples ##

### Streams and fields ###
![](README_figs/fields_and_streams.png)

### Temperature profiles from internal shocks simulations ###

![](README_figs/gradient.png)

### Magnetobremsstrahlung ###
![](README_figs/mbs.png)

To see how these examples were produced go to the wiki. I will be placing more elaborated stuff there.

# Recomendations and observations #

## Interacting with Python ##
For a good interactive plotting I suggest using IPython. Once inside call
the magic command `%%matplotlib osx`, if you are using macOS:

``` jupyter-notebook
%%matplotlib osx
```

## About the output ##
Something that must be pointed out is that the PNG image will not have the
correct characters. However the PDF and PGF will.

##  ##

This module is under development. Any issue, comment and upgrades are most welcome.
