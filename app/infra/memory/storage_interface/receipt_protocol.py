from app.core.receipt.receipt_representation import (
    ReceiptDataPartialListRepresentation,
    ReceiptRepresentation,
)
from app.infra.memory.storage_interface.initializing_storage import InitializingStorage


class IReceiptDb(InitializingStorage):  # type: ignore
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
