### Load nyu_rest dataset #####################################################

import glob
import numpy as np
from nilearn import input_data
from nilearn.plotting import plot_roi, plot_epi, show

n_clusters = 50

# This is resting-state data: the background has not been removed yet,
# thus we need to use mask_strategy='epi' to compute the mask from the
# EPI images
nifti_masker = input_data.NiftiMasker(memory='nilearn_cache',
                                      mask_strategy='epi', memory_level=1,
                                      standardize=False)
func_filename = sorted(glob.glob("/storage/workspace/elvis/openfmri/ds001/*/z_maps/*_minus_*.nii.gz"))
fmri_masked = nifti_masker.fit_transform(func_filename)
mask = nifti_masker.mask_img_.get_data().astype(np.bool)

### Ward ######################################################################

# Compute connectivity matrix: which voxel is connected to which
from sklearn.feature_extraction import image
shape = mask.shape
connectivity = image.grid_to_graph(n_x=shape[0], n_y=shape[1],
                                   n_z=shape[2], mask=mask)

# Computing the ward for the first time, this is long...
from sklearn.cluster import FeatureAgglomeration
# If you have scikit-learn older than 0.14, you need to import
# WardAgglomeration instead of FeatureAgglomeration
import time

# Compute the ward with more clusters, should be faster as we are using
# the caching mechanism
start = time.time()
ward = FeatureAgglomeration(n_clusters=n_clusters, connectivity=connectivity,
                            linkage='ward', memory='nilearn_cache')
ward.fit(fmri_masked)
print("Ward agglomeration %i clusters: %.2fs" % (n_clusters,
                                                 time.time() - start))

### Show result ###############################################################

# Unmask data
# Avoid 0 label
labels = ward.labels_ + 1
labels_img = nifti_masker.inverse_transform(labels)

from nilearn.image import mean_img
mean_func_img = mean_img(func_filename)

# common cut coordinates for all plots

first_plot = plot_roi(labels_img, title="Ward parcellation",
                      display_mode='ortho', black_bg=True)
# labels_img is a Nifti1Image object, it can be saved to file with the
# following code:
labels_img.to_filename('parcellation.nii')


# # Display the original data
# plot_epi(nifti_masker.inverse_transform(fmri_masked[0]),
#          cut_coords=first_plot.cut_coords,
#          title='Original (%i voxels)' % fmri_masked.shape[1],
#          display_mode='xz')

# # A reduced data can be create by taking the parcel-level average:
# # Note that, as many objects in the scikit-learn, the ward object exposes
# # a transform method that modifies input features. Here it reduces their
# # dimension
# fmri_reduced = ward.transform(fmri_masked)

# # Display the corresponding data compressed using the parcellation
# fmri_compressed = ward.inverse_transform(fmri_reduced)
# compressed_img = nifti_masker.inverse_transform(fmri_compressed[0])

# plot_epi(compressed_img, cut_coords=first_plot.cut_coords,
#          title='Compressed representation (%s parcels)' % n_clusters,
#          display_mode='xz')

show()
