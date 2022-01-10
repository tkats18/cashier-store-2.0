from dataclasses import dataclass
from http import HTTPStatus

from app.core.model.store_exception import StoreException
from app.core.model.store_response import StoreResponse
from app.core.receipt.receipt_models import FillReceipt
from app.core.report.report_model import ReportType
from app.core.store.store import StoreService


class ICashierService:
    def open_receipt(self) -> StoreResponse:
        pass

    def fill_receipt(self, request: FillReceipt) -> StoreResponse:
        pass

    def close_receipt(self, receipt_id: int) -> StoreResponse:
        pass


class ICustomerService:
    # def pay_receipt(self, receipt_id: int, payment: Payment) -> None:
    #     pass

    def get_receipt(self, receipt_id: int) -> StoreResponse:
        pass

    def get_products(self) -> StoreResponse:
        pass


class IManagerService:
    def generate_report(self, report: ReportType, day: str) -> StoreResponse:
        pass


@dataclass
class StoreAdapter:
    store: StoreService

    def open_receipt(self) -> StoreResponse:
        try:
            return StoreResponse(HTTPStatus.OK, None, self.store.open_receipt())
        except StoreException as ex:
            return StoreResponse(HTTPStatus.INTERNAL_SERVER_ERROR, ex.description, None)

    def fill_receipt(self, request: FillReceipt) -> StoreResponse:
        try:
            return StoreResponse(HTTPStatus.OK, None, self.store.fill_receipt(request))
        except StoreException as ex:
            return StoreResponse(HTTPStatus.INTERNAL_SERVER_ERROR, ex.description, None)

    def close_receipt(self, receipt_id: int) -> StoreResponse:
        try:
            return StoreResponse(
                HTTPStatus.OK,
                None,
                self.store.close_receipt(receipt_id),
            )
        except StoreException as ex:
            return StoreResponse(HTTPStatus.INTERNAL_SERVER_ERROR, ex.description, None)

    # def pay_receipt(self, receipt_id: int, payment: Payment) -> None:
    #     pass

    def get_receipt(self, receipt_id: int) -> StoreResponse:
        try:
            return StoreResponse(
                HTTPStatus.OK,
                None,
                self.store.get_receipt(receipt_id),
            )
        except StoreException as ex:
            return StoreResponse(HTTPStatus.INTERNAL_SERVER_ERROR, ex.description, None)

    def get_products(self) -> StoreResponse:
        try:
            return StoreResponse(HTTPStatus.OK, None, self.store.get_products())
        except StoreException as ex:
            return StoreResponse(HTTPStatus.INTERNAL_SERVER_ERROR, ex.description, None)

    def generate_report(self, report: ReportType, day: str) -> StoreResponse:
        try:
            return StoreResponse(
                HTTPStatus.OK,
                None,
                self.store.generate_report(report, day),
            )
        except StoreException as ex:
            return StoreResponse(HTTPStatus.INTERNAL_SERVER_ERROR, ex.description, None)
