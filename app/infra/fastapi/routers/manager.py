from fastapi import APIRouter, Depends

from app.core.facade import IManagerService
from app.core.report.report_model import ReportResponse, ReportType
from app.infra.fastapi.dependables import get_manager_service

manager_api = APIRouter()


@manager_api.get("/report/x")  # type: ignore
def generate_report_x(
    day: str,
    service: IManagerService = Depends(get_manager_service),
) -> ReportResponse:
    return service.generate_report(ReportType.X_REPORT, day)


# @manager_api.get("/report/z")
# def generate_report_y(
#     service: IManagerService = Depends(get_manager_service),
# ) -> ReportResponse:
#     return service.generate_report(ReportType.Y_REPORT)
