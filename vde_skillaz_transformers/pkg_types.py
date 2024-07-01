from typing import TypeVar, Generic, NamedTuple

ResponseType = TypeVar("ResponseType")
class WithError(Generic[ResponseType], NamedTuple):
    err: str | None
    res: ResponseType | None
