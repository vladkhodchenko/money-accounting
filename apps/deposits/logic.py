from abc import ABC, abstractmethod
from datetime import date
from dateutil.relativedelta import relativedelta

from dataclasses import dataclass
from apps.deposits.consts import Capitalization, TypeBankAccount


class InterestCalculator(ABC):
    @abstractmethod
    def calculate_profit(self, deposit: "DepositBase", months: int) -> float:
        pass


class MonthlyInterestCalculator(InterestCalculator):
    def calculate_profit(self, deposit: "DepositBase", months: int) -> float:
        effective_months = min(months, deposit.term_months)
        monthly_rate = deposit.interest_rate / 100 / 12
        return deposit.initial_amount * monthly_rate * effective_months


class DailyInterestCalculator(InterestCalculator):
    def calculate_profit(self, deposit: "DepositBase", months: int) -> float:
        effective_months = min(months, deposit.term_months)
        days = effective_months * 30  # Упрощённо, 30 дней в месяце
        daily_rate = deposit.interest_rate / 100 / 365
        return deposit.initial_amount * daily_rate * days


class EndTermInterestCalculator(InterestCalculator):
    def calculate_profit(self, deposit: "DepositBase", months: int) -> float:
        if months < deposit.term_months:
            return 0
        return (
            deposit.initial_amount
            * (deposit.interest_rate / 100)
            * (deposit.term_months / 12)
        )


CALCULATORS = {
    "monthly": MonthlyInterestCalculator(),
    "daily": DailyInterestCalculator(),
    "end": EndTermInterestCalculator(),
}


@dataclass
class DepositBase:
    name_bank: str
    name: str
    initial_amount: float
    interest_rate: float
    term_months: int
    date_from: date
    capitalization_id: Capitalization = Capitalization.MONTHLY
    deposit_type_id: TypeBankAccount = TypeBankAccount.DEPOSIT

    @property
    def date_to(self):
        return self.date_from + relativedelta(months=self.term_months)


class Deposit(DepositBase):
    def calculate_profit(self, months: int) -> float:
        calculator = CALCULATORS[self.capitalization_id.value]
        return round(calculator.calculate_profit(self, months), 2)

    def calculate_amount(self, months: int) -> float:
        profit = self.calculate_profit(months)
        return round(self.initial_amount + profit, 2)
