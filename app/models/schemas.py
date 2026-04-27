from pydantic import BaseModel, Field


class PasswordRequest(BaseModel):
    """PL: Model wejściowy dla analizy jednego hasła.
    EN: Request model for analyzing a single password.
    """

    # PL: Pydantic odrzuca puste hasła i zbyt długie wartości przed uruchomieniem logiki API.
    # EN: Pydantic rejects empty passwords and overly long values before API logic runs.
    password: str = Field(min_length=1, max_length=128)


class ComparePasswordsRequest(BaseModel):
    """PL: Model wejściowy dla porównania dwóch haseł.
    EN: Request model for comparing two passwords.
    """

    first_password: str = Field(min_length=1, max_length=128)
    second_password: str = Field(min_length=1, max_length=128)
