from app.core.facade import ICashierService, ICustomerService, IManagerService
from starlette.requests import Request


def get_manager_service(request: Request) -> IManagerService:
    return request.app.state.core


def get_customer_service(request: Request) -> ICustomerService:
    return request.app.state.core


def get_cashier_service(request: Request) -> ICashierService:
    return request.app.state.core
