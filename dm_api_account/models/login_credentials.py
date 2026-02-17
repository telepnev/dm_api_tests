from pydantic import BaseModel, Field, ConfigDict


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Login name")
    password: str = Field(..., description="Password")
    remember_me: bool = Field(..., description="Remember me", serialization_alias="rememberMe")