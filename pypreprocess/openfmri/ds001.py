import os
import sys
import shutil

# local imports
from utils import apply_preproc, load_preproc, load_glm_params

# pypreprocess imports
from pypreprocess.external.nilearn.datasets import fetch_nyu_rest
from pypreprocess.datasets_extras import unzip_nii_gz
import pypreprocess.nipype_preproc_spm_utils as nipype_preproc_spm_utils
from pypreprocess.external.nilearn.datasets import fetch_openfmri

FULL_ID = 'ds000001'
SHORT_ID = 'ds001'
NAME = 'Balloon Analog Risk-taking Task'
DESCRIPTION = """
Subjects perform the Balloon Analog Risk-taking Task in an event-related
design. Get full description <a href="https://openfmri.org/dataset/ds000001">\
here</a>.

<b>Note</b>: The original highres image for sub004 was not \
available, so the skull-stripped version is included as highres001.nii.gz
"""

MODEL_ID = 'model001'

ignore_list = []


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print ("Usage: python %s <data_root_dir> "
        "<preproc_root_dir> <glm_root_dir>" % sys.argv[0])
        print ("Example:\r\npython %s ~/datasets/raw"
               " ~/datasets/preproc ~/datasets/glm") % sys.argv[0]
        sys.exit(1)

    root_dir, preproc_dir, glm_dir = sys.argv[1:]

    # download data
    data_dir = fetch_openfmri(FULL_ID, root_dir)

    # alternative task_contrasts (errors in original file?)
    contrasts_file = '%s_task_contrasts.txt' % SHORT_ID
    assert os.path.isfile(contrasts_file), \
        "BUG: No contrasts file in code repo: %s" % contrasts_file
    dest = os.path.join(data_dir, SHORT_ID,
                        'models', MODEL_ID, 'task_contrasts.txt')

    if not os.path.isfile(dest):
        os.symlink(contrasts_file, dest)

    # apply SPM preprocessing
    apply_preproc(SHORT_ID, data_dir, preproc_dir, ignore_list,
                  dataset_description=DESCRIPTION)

    # prepare GLM (get data and design)
    preproc_data, motion_params = load_preproc(SHORT_ID, preproc_dir)

    glm_params = load_glm_params(SHORT_ID, data_dir, MODEL_ID,
                                 subject_ids=preproc_data.keys(),
                                 motion_params=motion_params)

    apply_glm(SHORT_ID, glm_dir, preproc_data,
              glm_params, resample=True, n_jobs=-1)
