from functools import wraps

__all__ = ["cache"]


def cache(user_function):
    sentinel = object()
    kwd_mark = (object(),)
    cache = {}

    @wraps(user_function)
    def wrapper(*args, **kwds):
        key = args
        if kwds:
            key += kwd_mark
            for item in kwds.items():
                key += item

        result = cache.get(key, sentinel)
        if result is not sentinel:
            return result
        result = user_function(*args, **kwds)
        cache[key] = result
        return result

    return wrapper
