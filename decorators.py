from typing import Callable

from endpoints import ENDPOINTS


def assert_endpoint_exists(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        if not (endpoint := kwargs.get('endpoint')):
            raise TypeError(f"Endpoint not provided.")
        if endpoint not in ENDPOINTS.values():
            raise ValueError(f"Unknown API {endpoint=}.")
        return func(*args, **kwargs)

    return wrapper
