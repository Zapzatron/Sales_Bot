from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    email: str
    phone: str
    source: str


class IntegrationCreate(BaseModel):
    name: str
    api_key: str
