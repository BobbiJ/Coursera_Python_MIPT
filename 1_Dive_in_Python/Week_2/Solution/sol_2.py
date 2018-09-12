import json
import functools


def to_json(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = json.dumps(func(*args, **kwargs))
        return result
    return wrapper




