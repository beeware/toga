def encode_value(v) -> str:
    # Encode a Python value or proxy-ish object.
    # Supported:
    #   - proxies (via .js_ref)
    #   - primitives (str/int/float/bool/None)
    #   - list/tuple (recursive)
    #   - dict with primitive keys (recursive on values)
    if hasattr(v, "js_ref"):  # any proxy
        return v.js_ref

    if isinstance(v, (str, int, float, bool)) or v is None:
        return repr(v)

    if isinstance(v, list):
        inner = ", ".join(encode_value(x) for x in v)
        return f"[{inner}]"

    if isinstance(v, tuple):
        inner = ", ".join(encode_value(x) for x in v)
        if len(v) == 1:
            inner += ","
        return f"({inner})"

    if isinstance(v, dict):
        items = ", ".join(f"{repr(k)}: {encode_value(val)}" for k, val in v.items())
        return f"{{{items}}}"

    try:
        return repr(str(v))

    except Exception as e:
        raise TypeError(
            f"Cannot encode {type(v).__name__}; pass a proxy (.js_ref), "
            f"primitive, list/tuple, dict, or an object with a valid __str__()."
        ) from e
