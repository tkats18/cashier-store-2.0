from dataclasses import dataclass


@dataclass
class StoreException(RuntimeError):
    description: str
