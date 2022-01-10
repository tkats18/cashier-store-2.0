from typing import Any, List, Protocol


class InitializingStorage(Protocol):
    def initialize_with_items(self, items: List[Any]) -> None:
        pass
