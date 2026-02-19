from pydantic import BaseModel, ConfigDict, Field


class ResetPassword(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

    login: str = Field(
        ...,
        min_length=1,
        description="Login name"
    )
    email: str = Field(
        ...,
        description="New user email"
    )
