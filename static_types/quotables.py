from enum import Enum

class LOADABLE(Enum):
    STOCK = "stock"
    CURRENCY = "currency"
    EXCHANGE = "exchange"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_
    
    def __str__(self):
        return self.value

    def __contains__(cls, item):
        return item in cls._value2member_map_

    __contains__ = classmethod(__contains__)
