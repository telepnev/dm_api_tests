from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, HttpUrl


# ==========================
# MAIN RESOURCE
# ==========================

class UserDetails(BaseModel):
    login: Optional[str] = None
    roles: Optional[List[UserRole]] = None

    mediumPictureUrl: Optional[HttpUrl] = None
    smallPictureUrl: Optional[HttpUrl] = None
    originalPictureUrl: Optional[HttpUrl] = None

    status: Optional[str] = None
    rating: Optional[Rating] = None

    online: Optional[datetime] = None
    registration: Optional[datetime] = None

    name: Optional[str] = None
    location: Optional[str] = None

    icq: Optional[str] = None
    skype: Optional[str] = None

    info: Optional[InfoBbText] = None
    settings: Optional[UserSettings] = None

class BbParseMode(str, Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"

class UserRole(BaseModel):
    name: Optional[str] = None


class Rating(BaseModel):
    value: Optional[int] = None


class InfoBbText(BaseModel):
    value: Optional[str] = None
    parseMode: Optional[BbParseMode] = None


class PagingSettings(BaseModel):
    postsPerPage: Optional[int] = None
    commentsPerPage: Optional[int] = None
    topicsPerPage: Optional[int] = None
    messagesPerPage: Optional[int] = None
    entitiesPerPage: Optional[int] = None


class UserSettings(BaseModel):
    colorSchema: Optional[ColorSchema] = None
    nannyGreetingsMessage: Optional[str] = None
    paging: Optional[PagingSettings] = None


class UserDetailsEnvelope(BaseModel):
    resource: UserDetails
    metadata: Optional[Dict[str, Any]] = None
