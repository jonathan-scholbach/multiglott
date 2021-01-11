from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Optional, TypeVar

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from middleware.auth import get_verified_user_or_none
from models.db_model import DBModel
from privileges import AccessConstricted


privilege_routes = APIRouter(prefix="/privileges")


@privilege_routes.post("/", response_model=List["Privilege"])
def user_privileges(
    entity_type: str = Body(...),
    entity_key: str = Body(...),
    entity_value: Any = Body(...),
    user: Optional["User"] = Depends(get_verified_user_or_none),
    db: "Session" = Depends(get_db),
):
    try:
        entity_class = next(
            klass
            for klass in AccessConstricted.SUBCLASSES
            if klass.__name__ == entity_type
        )
    except StopIteration:
        raise HTTPException(
            status_code=422,
            detail="Invalid entity_type `{entity_type}` in privilege request.",
        )

    return entity_class.get(
        db=db, key=entity_key, value=entity_value
    ).access_privileges(db=db, user=user)
