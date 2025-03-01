from typing import Optional, List

from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    species: str
    image:Optional[str] = None
    types:Optional[List[str]] = None
    qualities:Optional[List[str]] = None