from typing import Protocol

from app.core.receipt.receipt_representation import (
    ReceiptDataPartialListRepresentation,
    ReceiptRepresentation,
)


class IReceiptDb(Protocol):
    def open_receipt(self) -> int:
        pass

    def close_receipt(self, receipt_id: int) -> None:
        pass

    def get_receipt(self, receipt_id: int) -> ReceiptRepresentation:
        pass

    def find_receipts_on_day(
        self, date_time_obj: str
    ) -> ReceiptDataPartialListRepresentation:
        pass
