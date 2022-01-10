from typing import List

from app.infra.memory.storage_interface.initializing_storage import InitializingStorage


class IReceiptComponentDb(InitializingStorage):  # type: ignore
    def add_receipt_component(self, receipt_id: int, product_ids: List[int]) -> None:
        pass

    def get_receipt_component(self, receipt_id: int) -> List[int]:
        pass
