from pydantic import BaseModel, Field


class PasswordRequest(BaseModel):
    password: str = Field(min_length=1, max_length=128)


class ComparePasswordsRequest(BaseModel):
    first_password: str = Field(min_length=1, max_length=128)
    second_password: str = Field(min_length=1, max_length=128)
