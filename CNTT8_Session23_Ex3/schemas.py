from pydantic import BaseModel, ConfigDict, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ResourceCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str
    url: str
    is_published: bool = False


class ResourcePublishUpdate(BaseModel):
    is_published: bool


class ResourceResponse(BaseModel):
    id: int
    title: str
    description: str
    url: str
    is_published: bool
    created_by: str

    model_config = ConfigDict(from_attributes=True)