from pydantic import BaseModel, Field, ConfigDict


class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid")  # конфигурация, проверка обязательных полей
    login: str = Field(..., description="Login name")
    password: str = Field(..., description="Password for login")
    email: str = Field(..., description="Email address")


