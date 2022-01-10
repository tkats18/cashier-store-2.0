from typing import Dict

from app.core.receipt.receipt_interactor import ReceiptInteractor
from app.core.report.report_model import ReportResponse, ReportType
from app.core.report.report_strategy import IReportStrategy


class ReportInteractor:
    def __init__(
        self,
        receipt_interactor: ReceiptInteractor,
        report_engines: Dict[ReportType, IReportStrategy],
    ):
        self.receipt_interactor = receipt_interactor
        self.report_engines = report_engines

    def generate_report(self, report: ReportType, day: str) -> ReportResponse:
        respo = self.receipt_interactor.get_receipts_of_day(day)
        data = []

        for i in respo.receipt_ids:
            data.append(self.receipt_interactor.get_receipt(i.receipt_id))

        if not self.report_engines.__contains__(report):
            print("error")
        #     TODO theow error

        return ReportResponse(self.report_engines[report].report(data))
