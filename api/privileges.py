from enum import Enum
from typing import Any, List, Optional, TypeVar


class Privilege(Enum):
    CAN_CREATE = "can_create"
    CAN_READ = "can_read"
    CAN_EDIT = "can_edit"
    CAN_DELETE = "can_delete"


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
