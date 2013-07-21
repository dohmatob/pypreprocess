"""
XXX only use nosetests command-line tool to run this test module!

"""

import numpy as np
import nibabel
import os
import inspect
import nose
import nose.tools

# import the APIs to be tested
from ..spm_slice_timing import (
    fMRISTC
    )
