"""
Main VSNR functions
"""
import os
from ctypes import windll, POINTER, c_int, c_float
import numpy as np

PRECOMPILED_PATH = os.path.join(__file__, "..", "precompiled")


def get_vsnr2d():
    """ Load the 'cuda' function from the dedicated .dll library"""
    dll = windll.LoadLibrary(os.path.join(PRECOMPILED_PATH, "libvsnr2d.dll"))
    func = dll.VSNR_2D_FIJI_GPU
    func.argtypes = [POINTER(c_float), c_int, POINTER(c_float),
                     c_int, c_int, c_int,
                     c_float, POINTER(c_float), c_int, c_float]
    return func


def get_nblocks():
    """ Get the number of maximum threads per block library"""
    dll = windll.LoadLibrary(os.path.join(PRECOMPILED_PATH, "libvsnr2d.dll"))
    return dll.getMaxBlocks()


def vsnr2d(img, filters, nite=20, beta=10., nblocks='auto'):
    r"""
    Calculate the corrected image using the 2D-VSNR algorithm in libvsnr2d.dll

    .. note:
    To ease code comparison with the original onde, most of the variable names
    have been kept as nearly as possible during the code transcription.
    Accordingly, PEP8 formatting compatibility is not always respected.

    Parameters
    ----------
    img: numpy.ndarray((n0, n1))
        The image to process
    filters: list of dicts
        Dictionaries that contains filters definition.
        Example For a 'Dirac' filter:
        - filter={'name':'Dirac', 'noise_level':10}
        Example For a 'Gabor' filter:
        - filter={'name':'Gabor', 'noise_level':5, 'sigma':(3, 40), 'theta':45}
        For further informations, see :
        https://www.math.univ-toulouse.fr/~weiss/Codes/VSNR/Documentation_VSNR_V2_Fiji.pdf
    nite: int, optional
        Number of iterations in the denoising processing
    beta: float, optional
        Beta parameters
    nblocks: 'auto' or int, optional
        Number of threads per block to work with

    Returns
    -------
    img_corr: numpy.ndarray((n0, n1))
        The corrected image
    """
    length = len(filters)
    n0, n1 = img.shape

    # psis definition from filters
    psis = []
    for filt in filters:
        name = filt['name']
        noise_level = filt['noise_level']
        if name == 'Dirac':
            psis += [0, noise_level]
        elif name == 'Gabor':
            sigma = filt['sigma']
            theta = filt['theta']
            psis += [1, noise_level, sigma[0], sigma[1], theta]
        else:
            raise IOError(f"filter name '{name}' should be 'Dirac' or 'Gabor'")

    # flattened arrays and corresponding pointers definition
    psis = np.asarray(psis).flatten()
    u0 = img.flatten()
    u = np.zeros_like(u0)

    psis_ = (c_float * len(psis))(*psis)
    u0_ = (c_float * len(u0))(*u0)
    u_ = (c_float * len(u))(*u)

    # 'auto' nblocks definition
    nblocks_max = get_nblocks()
    if nblocks == 'auto':
        nblocks = nblocks_max
    else:
        nblocks = max(nblocks_max, nblocks)

    # calculation
    vmax = u0.max()
    try:
        get_vsnr2d()(psis_, length, u0_, n0, n1, nite, beta, u_, nblocks, vmax)
    except OSError:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        msg = '\n!!! Problem when running the cuda libvsnr2d.dll !!!\n'
        msg += 'You probably need to recompile the .dll\n'
        msg += f'See the README.txt for compilation instructions in {dir_path}'
        print(msg)

    # reshaping
    img_corr = np.array(u_).reshape(n0, n1).astype(float)

    return img_corr
