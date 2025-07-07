from enum import Enum
from mmap import ACCESS_COPY


class Capitalization(str, Enum):
    MONTHLY = "monthly"
    DAILY = "daily"
    END = "end"


class TypeBankAccount(str, Enum):
    ACCUMULATION = "accumulation"  # накопительный счет
    DEPOSIT = "deposit"  # вклад


class Bank(str, Enum):
    TINKOFF = "Tinkoff" or "T-Bank"
    VTB = "VTB"
    ALFABANK = "Alfabank"
    GAZPROMBANK = "Gazprombank"
    DOMRF = "Dom RF"
