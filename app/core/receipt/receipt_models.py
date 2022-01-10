from dataclasses import dataclass
from typing import List


@dataclass
class FillReceipt:
    receipt_id: int
    products: List[int]


@dataclass
class Payment:
    amount: int
    payment_method: str
