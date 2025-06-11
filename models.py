from abc import ABC, abstractmethod
from datetime import date
from dateutil.relativedelta import relativedelta

from dataclasses import dataclass
from typing import List, Union, Dict
from consts import Capitalization


class InterestCalculator(ABC):
    @abstractmethod
    def calculate_profit(self, deposit: 'DepositBase', months: int) -> float:
        pass


class MonthlyInterestCalculator(InterestCalculator):
    def calculate_profit(self, deposit: 'DepositBase', months: int) -> float:
        effective_months = min(months, deposit.term_months)
        monthly_rate = deposit.interest_rate / 100 / 12
        return deposit.initial_amount * monthly_rate * effective_months


class DailyInterestCalculator(InterestCalculator):
    def calculate_profit(self, deposit: 'DepositBase', months: int) -> float:
        effective_months = min(months, deposit.term_months)
        days = effective_months * 30  # Упрощённо, 30 дней в месяце
        daily_rate = deposit.interest_rate / 100 / 365
        return deposit.initial_amount * daily_rate * days


class EndTermInterestCalculator(InterestCalculator):
    def calculate_profit(self, deposit: 'DepositBase', months: int) -> float:
        if months < deposit.term_months:
            return 0
        return deposit.initial_amount * \
            (deposit.interest_rate / 100) * (deposit.term_months / 12)


CALCULATORS = {
    "monthly": MonthlyInterestCalculator(),
    "daily": DailyInterestCalculator(),
    "end": EndTermInterestCalculator()
}


@dataclass
class DepositBase:
    name: str
    initial_amount: float
    interest_rate: float
    term_months: int
    date_from: date
    capitalization: Capitalization = Capitalization.MONTHLY

    @property
    def date_to(self):
        return self.date_from + relativedelta(months=self.term_months)


class Deposit(DepositBase):
    def calculate_profit(self, months: int) -> float:
        calculator = CALCULATORS[self.capitalization.value]
        return round(calculator.calculate_profit(self, months), 2)

    def calculate_amount(self, months: int) -> float:
        profit = self.calculate_profit(months)
        return round(self.initial_amount + profit, 2)


class Portfolio:
    def __init__(self):
        self._deposits: List[Deposit] = []

    def add_deposit(self, *deposits: Deposit):
        self._deposits.extend(deposits)

    def get_deposit_names(self) -> List[str]:
        return [deposit.name for deposit in self._deposits]

    def get_deposits(self) -> List[Deposit]:
        return self._deposits.copy()

    def get_deposit_by_name(self, name: str) -> Union[Deposit, None]:
        return next((d for d in self._deposits if d.name == name), None)

    def calculate_total(self, target_months: int) -> float:
        total = 0.0
        for deposit in self._deposits:
            # Учитываем только действующие вклады
            if target_months <= deposit.term_months:
                total += deposit.calculate_amount(target_months)
        return total

    def forecast(self, periods: List[int]) -> dict:
        return {months: self.calculate_total(months) for months in periods}


portfolio_service = Portfolio()
