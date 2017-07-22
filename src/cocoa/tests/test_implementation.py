import os
from toga_dummy.test_utils import utils

BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'toga_cocoa'))

impl_tests = utils.create_impl_tests(BACKEND_ROOT)
# Add the implementations tests into the current namespace.
globals().update(impl_tests)
