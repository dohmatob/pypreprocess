import os
import glob
from nilearn.image.image import check_niimg_4d
from nilearn.decomposition.canica import CanICA
import nibabel

# Fetch data
z_maps = sorted(glob.glob("/storage/workspace/elvis/openfmri/ds001/*/z_maps/*_minus_*.nii.gz"))

# Fit CanICA
canica = CanICA(
    n_components=20, n_jobs=1, memory_level=5, verbose=10, random_state=0,
    memory="/storage/workspace/elvis/openfmri/nilearn_cache")
canica.fit(z_maps)

# Retrieve the independent components in brain space
components_img = canica.masker_.inverse_transform(canica.components_)
# components_img is a Nifti Image object, and can be saved to a file with
# the following line:
components_img.to_filename(
    '/storage/workspace/elvis/openfmri/canica_resting_state.nii.gz')
