from enum import Enum
from mmap import ACCESS_COPY

class Capitalization(str, Enum):
    MONTHLY = "monthly"
    DAILY = "daily"
    END = "end"


class TypeBankAccount(str, Enum):
    ACCUMULATION = "accumulation" # накопительный счет
    DEPOSIT = "deposit" # вклад


class Bank(str, Enum):
    TINKOFF = "tinkoff"
    VTB = "VTB"
    ALFABANK = "alfabank"
    