from pydantic import BaseModel, ConfigDict, Field


class ChangePassword(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )

    login: str = Field(
        ...,
        min_length=1,
        description="Login name"
    )

    token: str = Field(
        ...,
        description="Password reset token"

    )
    old_password: str = Field(
        ...,
        description="Old password",
        serialization_alias="oldPassword"

    )
    new_password: str = Field(
        ...,
        description="New password",
        serialization_alias="newPassword"

    )
