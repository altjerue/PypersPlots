from __future__ import division

def interpol(v1, v2, tt, NxM, logscale=False, rescale=False):
    import numpy as np
    import scipy.interpolate
    N = NxM[0]
    M = NxM[1]
    if logscale is True:
        v1i = np.logspace(np.log10(v1.min()), np.log10(v1.max()), N)
        v2i = np.logspace(np.log10(v2.min()), np.log10(v2.max()), M)
    else:
        v1i = np.linspace(v1.min(), v1.max(), N)
        v2i = np.linspace(v2.min(), v2.max(), M)
    ti = scipy.interpolate.griddata((v1, v2), tt,
                                    (v1i[None,:], v2i[:,None]),
                                    method='cubic',
                                    rescale=rescale
    )
    return v1i,v2i,ti

def dataExtract3col(filename, NxM, cols=(0,1,2),rescale=False):
    """dataExtract3col(filename, NxM, cols=(0,1,2))

    Four columns extraction routine. Getting data ready for contour
    plotting.

    filename: string
    Name of the file with at least four columns.

    N: int
    Size of the temporal arrays to generate the grid.

    cols: tuple
    Tuple of three int referring to the columns to be read.
    """
    import numpy as np
    import scipy.interpolate
    v1, v2, tt = np.loadtxt(filename, usecols=cols, unpack=True)
    return interpol(v1,v2,tt,NxM)

def dataExtract2col(filename, cols=(0,1)):
    """dataExtract3col(filename, N, cols=(0,1,2))

    Four columns extraction routine. Getting data ready for contour
    plotting.

    filename: string
    Name of the file with at least four columns.

    cols: tuple
    Tuple of two int referring to the columns to be read.
    """
    import numpy as np
    return np.loadtxt(filename, usecols=cols, unpack=True)

def hdf5ExtractScalar(h5file, dsets, group=None):
    """Extract data from an HDF5 data file.

    h5file: string
    File name.

    dsets: strings
    scalar datasets names
    """
    import numpy as np
    import h5py as h5
    h5f = h5.File(h5file, 'r')
    if group is None:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[dsets[i]][0])
            v = np.array(v)
            v = v.squeeze()
        else:
            v = h5f[dsets][0]
    else:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[group][dsets[i]][0])
            v = np.array(v)
            v = v.squeeze()
        else:
            v = h5f[group][dsets][0]
    h5f.close()
    return v

def hdf5Extract1D(h5file, dsets, group=None):
    """Extract data from an HDF5 data file.

    h5file: string
    File name.

    ds1,ds2: strings
    1D data set names
    """
    import numpy as np
    import h5py as h5
    h5f = h5.File(h5file, 'r')
    if group is None:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[dsets[i]][:])
            v = np.array(v)
            v = v.squeeze()
        else:
            v = h5f[dsets][:]
    else:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[group][dsets[i]][:])
            v = np.array(v)
            v = v.squeeze()
        else:
            v = h5f[group][dsets][:]
    h5f.close()
    return v

def hdf5Extract2D(h5file, dsets, group=None):
    """Extract data from an HDF5 data file.

    h5file: string
    File name.

    dsets: string or array of strings
    2D data set names
    """
    import numpy as np
    import h5py as h5
    h5f = h5.File(h5file, 'r')
    if group is None:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[dsets[i]][:,:])
            v = np.array(v)
            v = v.squeeze()
        else:
            v = h5f[dsets][:,:]
    else:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[group][dsets[i]][:,:])
            v = np.array(v)
            v = v.squeeze()
        else:
            v = h5f[group][dsets][:,:]
    h5f.close()
    return v

def hdf5Extract3D(h5file, dsets, group=None):
    """Extract data from an HDF5 data file.

    h5file: string
    File name.

    dsets: strings or array of strings
    3D data set names
    """
    import numpy as np
    import h5py as h5
    h5f = h5.File(h5file, 'r')
    if group is None:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[dsets[i]][:,:,:])
        else:
            v = h5f[dsets][:,:,:]
    else:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[group][dsets[i]][:,:,:])
        else:
            v = h5f[group][dsets][:,:,:]
    h5f.close()
    return v

def hdf5Extract4D(h5file, dsets, group=None):
    """Extract data from an HDF5 data file.

    h5file: string
    File name.

    dsets: strings or array of strings
    3D data set names
    """
    import numpy as np
    import h5py as h5
    h5f = h5.File(h5file, 'r')
    if group is None:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[dsets[i]][:,:,:,:])
        else:
            v = h5f[dsets][:,:,:,:]
    else:
        if type(dsets) is list:
            v = []
            for i in range(0, len(dsets)):
                v.append(h5f[group][dsets[i]][:,:,:,:])
        else:
            v = h5f[group][dsets][:,:,:,:]
    h5f.close()
    return v
