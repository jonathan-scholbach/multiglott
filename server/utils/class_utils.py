from typing import List


def _own_properties(cls: type) -> List[str]:
    return [
        key
        for key, value in cls.__dict__.items()
        if isinstance(value, property)
    ]


def properties(cls: type) -> List[str]:
    props = []
    for kls in cls.mro():
        props += _own_properties(kls)

    return props
