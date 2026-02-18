from pydantic import BaseModel, Field, ConfigDict, EmailStr


class Registration(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    login: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Login name"
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password for login"
    )

    email: EmailStr = Field(
        ...,
        description="Valid email address"
    )

    """
    Ограничения на длину берем из OpenAPI спецификации или backend-кода.
    Если в контракте API указаны minLength/maxLength, отражаем их в Pydantic модели.
    Если ограничений нет, не добавляем их самостоятельно, чтобы не сделать модель строже backend-а.
    В случае отсутствия документации уточнить у разработчиков или проверить через негативные тесты.
    """
