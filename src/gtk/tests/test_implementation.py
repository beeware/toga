import os
from toga.utils import test as test_utils


globals().update(
    test_utils.create_impl_tests(
        os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'toga_gtk')
        )
    )
)
