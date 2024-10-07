from pydantic import BaseModel


class UserInput(BaseModel):
    name: str
    email: str
    hashed_password: str


class UserOutput(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
