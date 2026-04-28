from pydantic import BaseModel, Field


class PasswordRequest(BaseModel):
    # PL: Limit 128 znakow zabezpiecza API przed zbyt duzym inputem.
    # EN: The 128-character limit keeps the API input reasonably small.
    password: str = Field(min_length=1, max_length=128)


class ComparePasswordsRequest(BaseModel):
    # PL: Ten sam limit stosujemy dla obu hasel, zeby porownanie bylo spojne.
    # EN: Both passwords use the same limit so comparison validation is consistent.
    first_password: str = Field(min_length=1, max_length=128)
    second_password: str = Field(min_length=1, max_length=128)
