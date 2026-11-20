from pydantic import BaseModel
from typing import List
from pydantic import Field
from datetime import date

class Usuario(BaseModel):
    username: str
    vacaciones: List[date] = Field(default_factory=list)

