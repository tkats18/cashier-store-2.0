from dataclasses import dataclass

from app.core.product.product_interactor import ProductInteractor
from app.core.product.product_representation import ProductListResponse
from app.core.receipt.receipt_interactor import ReceiptInteractor
from app.core.receipt.receipt_models import FillReceipt
from app.core.receipt.receipt_representation import (
    ReceiptDataPartialRepresentation,
    ReceiptFullRepresentation,
)
from app.core.report.report_interactor import ReportInteractor
from app.core.report.report_model import ReportResponse, ReportType
from app.core.report.report_strategy import XReportStrategy
from app.infra.memory.storage_interface.product_protocol import IProductDb
from app.infra.memory.storage_interface.receipt_component_protocol import (
    IReceiptComponentDb,
)
from app.infra.memory.storage_interface.receipt_protocol import IReceiptDb


@dataclass
class StoreService:
    receipt_interactor: ReceiptInteractor
    product_interactor: ProductInteractor
    report_interactor: ReportInteractor

    @classmethod
    def create(
        cls,
        receipt_db: IReceiptDb,
        product_db: IProductDb,
        receipt_component_db: IReceiptComponentDb,
    ) -> "StoreService":
        report_engines = dict({ReportType.X_REPORT: XReportStrategy()})

        product_interactor = ProductInteractor(product_db)
        receipt_interactor = ReceiptInteractor(
            receipt_db, receipt_component_db, product_interactor
        )
        report_interactor = ReportInteractor(receipt_interactor, report_engines)

        return cls(
            product_interactor=product_interactor,
            receipt_interactor=receipt_interactor,
            report_interactor=report_interactor,
        )

    def get_products(self) -> ProductListResponse:
        return self.product_interactor.get_products_by_ids_in().get_products()

    def open_receipt(self) -> ReceiptDataPartialRepresentation:
        return self.receipt_interactor.open_receipt()

    def fill_receipt(self, request: FillReceipt) -> None:
        self.receipt_interactor.add_items_to_receipt(request)

    def close_receipt(self, receipt_id: int) -> None:
        self.receipt_interactor.close_receipt(receipt_id)

    # def pay_receipt(self, receipt_id: int, payment: Payment) -> None:
    #     self.receipt_interactor.pay_receipt(receipt_id, payment)

    def generate_report(self, report: ReportType, day: str) -> ReportResponse:
        return self.report_interactor.generate_report(report, day)

    def get_receipt(self, receipt_id: int) -> ReceiptFullRepresentation:
        return self.receipt_interactor.get_receipt(receipt_id)
