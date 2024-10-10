from typing import List
from typing import Optional
from schemas.base import BaseSchemaModel


class EventIntent(BaseSchemaModel):
    destinationName: str
    important: Optional[bool] = False
    bytes: Optional[int] = 0
    score: Optional[int] = 0


class EventSchema(BaseSchemaModel):
    payload: dict
    routingIntents: List[EventIntent]
    strategy: Optional[str] = None
