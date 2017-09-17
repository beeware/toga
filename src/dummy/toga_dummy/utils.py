def not_required_on(*args):
    """ This decorator function is used to mark methods or classes
    that they are not required on certain platforms.
    This is only used by the implementation checks creation mechanism.

    Args:
        *args (str): Takes arguments in form of strings.

    Notes:
        You should only use 'mobile' and 'desktop' as *args.

    Examples:
        >>> # Marks the function as only required on platforms that are not "mobile".
        >>> @not_required_on('mobile')
        >>> def open_window():
        >>>     self.window.open()

        >>> # Function is not required on "mobile" and "gtk" backends.
        >>> @not_required_on('mobile', 'gtk')
        >>> def open_window():
        >>>     self.window.open()

    Returns:
        Not important but it is a ``callable``.
    """
    return callable