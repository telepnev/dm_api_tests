from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, ConfigDict


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSICPALE = "ClassicPale"
    NIGHT = "Night"


class BbParseMode(str, Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class InfoBbText(BaseModel):
    value: Optional[str] = None
    parse_mode: Optional[BbParseMode] = Field(
        default=None,
        alias="parseMode"
    )


class PagingSettings(BaseModel):
    posts_per_page: Optional[int] = Field(None, alias="postsPerPage")
    comments_per_page: Optional[int] = Field(None, alias="commentsPerPage")
    topics_per_page: Optional[int] = Field(None, alias="topicsPerPage")
    messages_per_page: Optional[int] = Field(None, alias="messagesPerPage")
    entities_per_page: Optional[int] = Field(None, alias="entitiesPerPage")


class UserSettings(BaseModel):
    color_schema: Optional[ColorSchema] = Field(
        default=None,
        alias="colorSchema"
    )
    nanny_greetings_message: Optional[str] = Field(
        default=None,
        alias="nannyGreetingsMessage"
    )
    paging: PagingSettings


class Resource(BaseModel):
    login: str
    roles: List[UserRole]
    rating: Rating

    online: Optional[datetime] = None
    registration: Optional[datetime] = None

    medium_picture_url: Optional[str] = Field(None, alias="mediumPictureUrl")
    small_picture_url: Optional[str] = Field(None, alias="smallPictureUrl")
    original_picture_url: Optional[str] = Field(None, alias="originalPictureUrl")

    status: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    icq: Optional[str] = None
    skype: Optional[str] = None

    info: Optional[Union[InfoBbText, str]] = None

    settings: UserSettings


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # строгая проверка контракта
        populate_by_name=True  # поддержка alias
    )

    resource: Optional[Resource] = None
    metadata: Optional[str] = None
