from pydantic import BaseModel
from typing import Annotated
from pydantic import constr


class UserCreate(BaseModel):
    username: str
    email: str
    password: Annotated[str, constr(max_length=72)]

class UserRead(BaseModel):
    id: int
    username: str
    email: str

    model_config = {
        "from_attributes": True  # v2 equivalent of orm_mode
    }

class UserLogin(BaseModel):
    email: str
    password: str