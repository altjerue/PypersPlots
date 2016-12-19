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
import Pypersplots as pp
import numpy as np
x = np.linspace(0.0, 2.0*np.pi, 50)
pp.latexify()
fig,ax = pp.initPlot()
pp.plotxy(fig,ax,x,np.sin(x))
pp.printer(fig,ax,'some example',onscreen=True)
```

## Log-log plot ##

## Contours plot ##

## Gradient plot ##

## Gradient and contours plot ##

## Multiple plots ##
