from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class StoreResponse(Generic[T]):
    def __init__(
        self,
        status: int,
        error: Optional[str] = None,
        data: Optional[T] = None,
    ):
        self.status = status
        self.error = error
        self.data = data
