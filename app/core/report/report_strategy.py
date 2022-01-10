from dataclasses import dataclass
from typing import List, Any, Dict

from app.core.product.product_representation import ProductFullRepresentation
from app.core.receipt.receipt_representation import ReceiptFullRepresentation


@dataclass
class ReportModel:
    item: ProductFullRepresentation
    sold: int


# Generic enough i think :ddd
class IReportStrategy:
    def report(self, data: List[ReceiptFullRepresentation]) -> Dict[str, Any]:
        pass


class XReportStrategy(IReportStrategy):
    def report(self, data: List[ReceiptFullRepresentation]) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()

        num_closed_receipts = 0
        revenue = 0.0
        items_sold: List[ReportModel] = list()

        all_items: Dict[str, ProductFullRepresentation] = dict()
        sold_number: Dict[str, int] = dict()

        for i in data:
            if i.receipt.closed:
                num_closed_receipts += 1

        for k in data:
            revenue += k.total

        for it in data:
            for prod in it.items.response:
                key = self._prod_key(prod)
                if sold_number.__contains__(key):
                    sold_number[key] += 1
                else:
                    sold_number[key] = 1
                    all_items[key] = prod

        for r in sold_number:
            items_sold.append(ReportModel(all_items[r], sold_number[r]))

        result["revenue"] = revenue
        result["closed"] = num_closed_receipts
        result["items_sold"] = items_sold

        return result

    @staticmethod
    def _prod_key(prod: ProductFullRepresentation) -> str:
        return str(prod.name + "-" + str(prod.units))
