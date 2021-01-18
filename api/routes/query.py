from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database import get_db
from middleware.auth import get_verified_user_or_none
from privileges import AccessConstricted, Privilege


query_route = APIRouter(
    prefix="/query",
)


def get_entity(entity_type: str, key: str, value: Any, db: Session):
    entity_class = AccessConstricted.get_subclass(subclass_name=entity_type)
    print(entity_type)
    if not entity_class:
        raise HTTPException(
            status_code=400,
            detail=f"entity_type {entity_type} is not accessible.",
        )

    entity = entity_class.get(db=db, value=value, key=key)
    if not entity:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot find {entity_class.__name__} with {key} = {value}.",
        )
    
    return entity

@query_route.post("/")
def find_entity(
    entity_type: str = Body(...),
    key: str = Body(...),
    value: Any = Body(...),
    related_models: List[str] = Body(...),
    user: Optional["User"] = Depends(get_verified_user_or_none),
    db: Session = Depends(get_db),
):
    entity = get_entity(entity_type=entity_type, key=key, value=value, db=db)
    serialized_entity = jsonable_encoder(entity)
    serialized_related_models = {
        related_model: getattr(entity, related_model)
        for related_model in related_models
    }
    serialized_entity.update(serialized_related_models)

    privileges = {
        "privileges": [
            privilege.value
            for privilege in entity.access_privileges(db=db, user=user)
        ]
    }
    serialized_entity.update(privileges)

    return serialized_entity


@query_route.put("/")
def update_entity(
    entity_type: str = Body(...),
    key: str = Body(...),
    value: Any = Body(...),
    data: dict = Body(...),
    user: Optional["User"] = Depends(get_verified_user_or_none),
    db: Session = Depends(get_db),
):
    print("HERE")
    entity = get_entity(entity_type=entity_type, key=key, value=value, db=db)
    print(entity)
    if not Privilege.CAN_EDIT in entity.access_privileges(db=db, user=user):
        raise HTTPException(
            status_code=401,
            detail="User lacks privilege to edit this entity."
        )

    for updated_key, updated_value in data.items():
        setattr(entity, updated_key, updated_value)
    
    db.add(entity)
    db.commit()


    return entity