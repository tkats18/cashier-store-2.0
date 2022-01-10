from dataclasses import dataclass
from typing import List

from app.core.product.product_representation import ProductListResponse


@dataclass
class ReceiptDataPartialRepresentation:
    receipt_id: int


@dataclass
class ReceiptRepresentation:
    receipt_id: int
    closed: bool
    create_time: str


@dataclass
class ReceiptFullRepresentation:
    receipt: ReceiptRepresentation
    items: ProductListResponse
    total: float


@dataclass
class ReceiptDataPartialListRepresentation:
    receipt_ids: List[ReceiptDataPartialRepresentation]
