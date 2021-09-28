from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class MenuCreate(BaseModel):
    name: str
    description: str
    created : Optional[datetime]
    updated : Optional[datetime]
    class Config:
        orm_mode = True

class Dish(BaseModel):
    name: str
    description: str
    owner_id : str
    time_to_get_ready : int
    price : float
    is_vgetarian : bool
    created : Optional[datetime]
    updated : Optional[datetime]
    class Config:
        orm_mode = True

class Menu(MenuCreate):
    dishes: List[Dish] = []
    class Config:
        orm_mode = True
