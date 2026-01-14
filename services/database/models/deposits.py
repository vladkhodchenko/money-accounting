from utils.clients.database.base_model import Base
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    TIMESTAMP,
)
from sqlalchemy.orm import Mapped, mapped_column

from utils.clients.database.mixin_model import MixinModel


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


# тип капитализации: ежемесячно/в конце срока/ежедневно
class CapitalizationTypeModel(Base):
    __tablename__ = "capitalization_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


# вклад/сберегательный счет
class DepositTypeModel(Base):
    __tablename__ = "deposit_types"

    id = Column(Integer, primary_key=True)
    deposit_type = Column(String(50), unique=True, nullable=False)


class DepositsModel(MixinModel):
    __tablename__ = "deposits"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    name = Column(String(100), unique=True, nullable=False)
    name_bank = Column(String(100), unique=True, nullable=False)

    initial_amount = Column(Float, nullable=False)
    final_amount = Column(Float, nullable=False)
    earned_amount = Column(Float, nullable=False)

    interest_rate = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)

    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)

    capitalization_id = Column(Integer, ForeignKey("capitalization_types.id"))
    deposit_type_id = Column(Integer, ForeignKey("deposit_types.id"))
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

