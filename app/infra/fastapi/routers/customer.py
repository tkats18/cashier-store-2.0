from app.core.facade import ICustomerService
from app.core.product.product_representation import ProductListResponse
from app.core.receipt.receipt_representation import ReceiptFullRepresentation
from app.infra.fastapi.dependables import get_customer_service
from fastapi import APIRouter
from fastapi.params import Depends

customer_api: APIRouter = APIRouter()


# @customer_api.get("/receipt/{receipt_id}/pay")
# def pay_receipt(
#     receipt_id: int,
#     payment: Payment,
#     service: ICustomerService = Depends(get_customer_service),
# ) -> None:
#     service.pay_receipt(receipt_id, payment)


@customer_api.get("/view/receipt/{receipt_id}")  # type: ignore
def pay_receipt(
    receipt_id: int,
    service: ICustomerService = Depends(get_customer_service),
) -> ReceiptFullRepresentation:
    return service.get_receipt(receipt_id)


@customer_api.get("/view/products")  # type: ignore
def get_products(
    service: ICustomerService = Depends(get_customer_service),
) -> ProductListResponse:
    return service.get_products()
