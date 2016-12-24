def dataExtract3col(filename, N, cols=(0,1,2),rescale=False):
    """contourExtract4(filename, N, cols=(0,1,2))

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
    v1i = np.linspace(v1.min(), v1.max(), N)
    v2i = np.linspace(v2.min(), v2.max(), N)
    ti = scipy.interpolate.griddata((v1, v2), tt,
                                    (v1i[None,:], v2i[:,None]),
                                    method='cubic',
                                    rescale=rescale
    )
    return v1i, v2i, ti

def hdf5Extract1D(h5file, dsets):
    """ hdf5Extraxt(h5file)

    Extract data from an HDF5 data file.

    h5file: string
    File name.

    ds1,ds2: strings
    1D data set names

    """
    import h5py as h5
    h5f = h5.File(h5file, 'r')
    if type(dsets) is list:
        v = []
        for i in range(0, len(dsets) + 1):
            v.append(h5f[dsets[i]][:])
    else:
        v = h5f[dsets[i]][:]
    h5f.close()

    return v

def hdf5Extract3D(h5file, ds1, ds2, ds3, xylog):
    """ hdf5Extraxt(h5file)

    Extract data from an HDF5 data file.

    h5file: string
    File name.

    ds1,ds2: strings
    1D data set names

    ds3:
    2D  data set names
    """
    import h5py as h5

    h5f = h5.File(h5file, 'r')
    v1 = emissTable[ds1][:]
    v2 = emissTable[ds2][:]
    tt = emissTable[ds3][:,:]
    h5f.close()
    if xylog:
        v1i = np.logspace(np.log10(v1.min()), np.log10(v1.max()), N)
        v2i = np.logspace(np.log10(v2.min()), np.log10(v2.max()), N)
    else:
        v1i = np.linspace(v1.min(), v1.max(), N)
        v2i = np.linspace(v2.min(), v2.max(), N)
    ti = scipy.interpolate.griddata((v1, v2), tt,
                                    (v1i[None,:], v2i[:,None]),
                                    method='cubic',
                                    rescale=rescale
    )

    return v1,v2,v3
