This is a library intended to produce publishable and not so heavy contour and gradient plots.

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
import PypersPlots as pp
pp.latexify()
import numpy as np
x = np.linspace(0.0, 2.0*np.pi, 50)
p1 = pp.PypersSingle()
pp.plotxy(p1.fig,p1.ax,x,np.sin(x))
pp.decor(p1.fig,p1.ax,xlim=(0.0,2.0*np.pi),ylim=(-1.0,1.0))
pp.printer(p1.fig,p1.ax,'some example',onscreen=True)
```

## Log-log plot ##
```python
import Pypersplots as pp
import numpy as np
x = np.linspace(0.0, 2.0*np.pi, 50)
pp.latexify()
fig,ax = pp.initPlot()
pp.plotxy(fig,ax,x,np.sin(x),log=True)
pp.printer(fig,ax,'some example',onscreen=True)
```

## Contours plot ##

## Gradient plot ##

## Gradient and contours plot ##

## Multiple plots ##
