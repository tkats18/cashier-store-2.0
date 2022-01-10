from dataclasses import dataclass

from app.core.model.store_exception import StoreException
from app.core.product.product_interactor import ProductInteractor
from app.core.receipt.receipt_models import FillReceipt
from app.core.receipt.receipt_representation import (
    ReceiptDataPartialListRepresentation,
    ReceiptDataPartialRepresentation,
    ReceiptFullRepresentation,
)
from app.infra.memory.storage_interface.receipt_component_protocol import (
    IReceiptComponentDb,
)
from app.infra.memory.storage_interface.receipt_protocol import IReceiptDb


@dataclass
class ReceiptInteractor:
    receipt_db: IReceiptDb
    receipt_component_db: IReceiptComponentDb
    product_interactor: ProductInteractor

    def open_receipt(self) -> ReceiptDataPartialRepresentation:
        return ReceiptDataPartialRepresentation(self.receipt_db.open_receipt())

    def add_items_to_receipt(self, request: FillReceipt) -> None:
        receipt = self.receipt_db.get_receipt(request.receipt_id)

        if receipt.closed:
            raise StoreException(
                "Receipt with id " + str(request.receipt_id) + " is closed"
            )

        self.product_interactor.get_products_by_ids_in(request.products)
        self.receipt_component_db.add_receipt_component(
            request.receipt_id, request.products
        )

    def close_receipt(self, receipt_id: int) -> None:
        receipt = self.receipt_db.get_receipt(receipt_id)
        if receipt.closed:
            raise StoreException(
                "Receipt with id " + str(receipt_id) + " already closed"
            )
        self.receipt_db.close_receipt(receipt_id)

    def get_receipts_of_day(
        self, report_day: str
    ) -> ReceiptDataPartialListRepresentation:
        return self.receipt_db.find_receipts_on_day(report_day)

    def get_receipt(self, receipt_id: int) -> ReceiptFullRepresentation:
        receipt = self.receipt_db.get_receipt(receipt_id)
        receipt_product_ids = self.receipt_component_db.get_receipt_component(
            receipt_id
        )

        products = self.product_interactor.get_products_by_ids_in(receipt_product_ids)
        return ReceiptFullRepresentation(
            receipt, products.get_products(), products.calculate_total_price()
        )

    # def pay_receipt(self, receipt_id: int, payment: Payment) -> None:

    #     receipt = self.get_receipt(receipt_id)
    #     if receipt.total > payment.amount:
    #         raise RuntimeError()
    #
    #     self.receipt_db.mark_as_payed()
