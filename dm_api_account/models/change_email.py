from pydantic import BaseModel, ConfigDict, Field


class ChangeEmail(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )
    login: str = Field(
        ...,
        description="Login name"
    )

    password: str = Field(
        ...,
        description="Password"
    )

    email: str = Field(
        ...,
        description="New user email"
    )