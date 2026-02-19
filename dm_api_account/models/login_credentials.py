from pydantic import BaseModel, Field, ConfigDict


class LoginCredentials(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

    login: str = Field(
        ...,
        min_length=1,
        description="Login name"
    )

    password: str = Field(
        ...,
        min_length=1,
        description="Password"
    )

    remember_me: bool = Field(
        default=False,
        description="Remember me flag",
        serialization_alias="rememberMe"
    )

    # remember_me: bool = Field(..., description="Remember me", serialization_alias="rememberMe")