from enum import Enum

class Capitalization(str, Enum):
    MONTHLY = "monthly"
    DAILY = "daily"
    END = "end"