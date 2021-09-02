from pydantic import BaseModel


class Session(BaseModel):
    name: str


class SessionId(BaseModel):
    id: str
