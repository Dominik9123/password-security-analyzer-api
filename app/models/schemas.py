from pydantic import BaseModel, Field


class PasswordRequest(BaseModel):
    # Keep password inputs within a small, predictable size.
    password: str = Field(min_length=1, max_length=128)


class ComparePasswordsRequest(BaseModel):
    # Apply the same validation limits to both compared passwords.
    first_password: str = Field(min_length=1, max_length=128)
    second_password: str = Field(min_length=1, max_length=128)
