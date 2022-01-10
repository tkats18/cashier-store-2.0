from fastapi import APIRouter, Depends

from app.core.facade import ICashierService
from app.core.model.store_response import StoreResponse
from app.core.receipt.receipt_models import FillReceipt
from app.infra.fastapi.dependables import get_cashier_service

cashier_api = APIRouter()


@cashier_api.get("/receipt/open")  # type: ignore
def open_receipt(
    service: ICashierService = Depends(get_cashier_service),
) -> StoreResponse:
    return service.open_receipt()


@cashier_api.post("/receipt/fill")  # type: ignore
def fill_receipt(
    request: FillReceipt, service: ICashierService = Depends(get_cashier_service)
) -> StoreResponse:
    return service.fill_receipt(request)


@cashier_api.post("/receipt/{receipt_id}/close")  # type: ignore
def close_receipt(
    receipt_id: int, service: ICashierService = Depends(get_cashier_service)
) -> StoreResponse:
    return service.close_receipt(receipt_id)
