try:
    # Try to import js from the PyScript namespace.
    import js
except ModuleNotFoundError:
    # To ensure the code can be imported, provide a js symbol
    # as a fallback
    js = None
