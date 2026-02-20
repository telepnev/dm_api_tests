from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="ignore")

    type: Optional[str] = None
    title: str
    status: int
    traceId: Optional[str] = None
    errors: Optional[Dict[str, List[str]]] = None