from typing import List, Optional

from pydantic import BaseModel


class VocabSchema(BaseModel):
    id: int
    hint: Optional[str]
    source: List[str]
    target: List[str]

    class Config:
        orm_mode = True
