import os

from toga_dummy import test_implementation

globals().update(
    test_implementation.create_impl_tests(
        os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'toga_cocoa')
        )
    )
)
