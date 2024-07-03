from typing import Mapping, TypeVar

K = TypeVar('K')
V = TypeVar('V')

def strip_dict(data: dict[K, V]) -> dict[K, V]:
    stripped_dict = {}
    for k, v in data.items():
        if isinstance(v, str):
            stripped_dict[k] = v.strip()
        else:
            stripped_dict[k] = v
    return stripped_dict
