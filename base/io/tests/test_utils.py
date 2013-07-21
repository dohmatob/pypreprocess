import numpy as np
import nibabel
import os
import inspect
import nose
import nose.tools

# import the APIIS to be tested
from ..utils import (
    _load_vol,
    _load_specific_vol)

# global setup
OUTPUT_DIR = "/tmp/test_spm_realign_data_dir"
IMAGE_EXTENSIONS = [".nii", ".nii.gz", ".img"]


def create_random_image(shape=None,
                        ndim=3,
                        n_scans=None,
                        affine=np.eye(4),
                        parent_class=nibabel.Nifti1Image):
    """
    Creates a random image of prescribed shape

    """

    if shape is None:
        shape = np.random.random_integers(20, size=ndim)

    ndim = len(shape)
    if not n_scans is None and ndim == 4:
        shape[-1] = n_scans

    return parent_class(np.random.randn(*shape), affine)


def test_load_vol():
    # setup
    output_dir = os.path.join(OUTPUT_DIR, inspect.stack()[0][3])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # creat a volume
    vol = create_random_image()

    # test loading vol from nibabel object
    _vol = _load_vol(vol)
    nose.tools.assert_true(isinstance(_vol, type(vol)))
    nose.tools.assert_equal(_vol.shape, vol.shape)
    np.testing.assert_array_equal(_vol.get_data(), vol.get_data())

    # test loading vol by filename
    for ext in IMAGE_EXTENSIONS:
        # save vol with extension ext
        vol_filename = os.path.join(output_dir, "vol%s" % ext)
        nibabel.save(vol, vol_filename)

        # note that .img loads as Nifti1Pair, not Nifti1Image
        vol_type = nibabel.Nifti1Pair if ext == '.img' else nibabel.Nifti1Image

        # load the vol by filename
        _vol = _load_vol(vol_filename)
        nose.tools.assert_true(isinstance(_vol, vol_type))
        nose.tools.assert_equal(_vol.shape, vol.shape)
        np.testing.assert_array_equal(_vol.get_data(), vol.get_data())


def test_load_specific_vol():
    # setup
    output_dir = os.path.join(OUTPUT_DIR, inspect.stack()[0][3])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    n_scans = 23

    # create 4D film
    film = create_random_image(ndim=4, n_scans=n_scans)

    # test loading vol from nibabel image object
    for t in xrange(n_scans):
        _vol, _n_scans = _load_specific_vol(film, t)
        nose.tools.assert_equal(_n_scans, n_scans)
        nose.tools.assert_true(isinstance(_vol, type(film)))
        nose.tools.assert_equal(_vol.shape, film.shape[:-1])
        np.testing.assert_array_equal(_vol.get_data(), film.get_data()[..., t])

    # test loading vol from a single 4D filename
    for ext in IMAGE_EXTENSIONS:
        for film_filename_type in ['str', 'list']:
            if film_filename_type == 'str':
                # save film as single filename with extension ext
                film_filename = os.path.join(output_dir, "4D%s" % ext)
                nibabel.save(film, film_filename)
            else:
                # save film as multiple filenames (3D vols), with ext extension
                vols = nibabel.four_to_three(film)
                film_filename = []
                for t, vol in zip(xrange(n_scans), vols):
                    vol_filename = os.path.join(output_dir,
                                                "vol_%i%s" % (t, ext))
                    nibabel.save(vol, vol_filename)
                    film_filename.append(vol_filename)

            # test loading proper
            for t in xrange(n_scans):
                # note that .img loads as Nifti1Pair, not Nifti1Image
                vol_type = nibabel.Nifti1Pair if ext == '.img' else \
                    nibabel.Nifti1Image

                # load specific 3D vol from 4D film by filename
                _vol, _n_scans = _load_specific_vol(film_filename, t)
                nose.tools.assert_equal(_n_scans, n_scans)
                nose.tools.assert_true(isinstance(_vol, vol_type))
                nose.tools.assert_equal(_vol.shape, film.shape[:-1])
                np.testing.assert_array_equal(_vol.get_data(),
                                              film.get_data()[..., t])
