def raises(exc_type, fn, *args, **kwargs):
    """Return True if fn(*args, **kwargs) raises exc_type. Fail loudly otherwise."""
    try:
        fn(*args, **kwargs)
    except exc_type:
        return True
    except Exception as other:
        raise AssertionError(f"expected {exc_type.__name__}, got {type(other).__name__}: {other}")
    raise AssertionError(f"expected {exc_type.__name__}, but nothing was raised")