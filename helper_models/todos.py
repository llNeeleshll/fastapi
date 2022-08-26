from typing import Optional
from pydantic import BaseModel, Field

class Todo(BaseModel):
    title: str = Field()
    description: Optional[str] = Field()
    priority: int = Field(gt=0,lt=6)
    complete: bool = Field(default=False)