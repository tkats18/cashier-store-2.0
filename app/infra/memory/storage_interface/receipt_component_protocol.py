from typing import List, Protocol


class IReceiptComponentDb(Protocol):
    def add_receipt_component(self, receipt_id: int, product_ids: List[int]) -> None:
        pass

    def get_receipt_component(self, receipt_id: int) -> List[int]:
        pass
