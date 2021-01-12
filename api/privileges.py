from enum import Enum
from typing import Any, List, Optional, Type, TypeVar


class Privilege(Enum):
    CAN_CREATE = "CAN_CREATE"
    CAN_READ = "CAN_READ"
    CAN_EDIT = "CAN_EDIT"
    CAN_DELETE = "CAN_DELETE"


class AccessConstricted:
    """Interface for Classes who provide access based on user's privilege."""

    ABSTRACT_METHODS = ["access_privileges", "get"]

    SUBCLASSES = []

    def __init_subclass__(cls):
        for method_name in AccessConstricted.ABSTRACT_METHODS:
            method = getattr(cls, method_name, None)
            if not method or not callable(method):
                raise TypeError(
                    f"Can't initialize abstract class {cls.__name__} with "
                    f"abstract methods {method_name}."
                )

        AccessConstricted.SUBCLASSES.append(cls)

    @classmethod
    def get_subclass(cls, subclass_name: str) -> Optional[Type["AccessConstricted"]]:
        try:
            return next(
                subclass
                for subclass in AccessConstricted.SUBCLASSES
                if subclass.__name__ == subclass_name
            )

        except StopIteration:
            return None
