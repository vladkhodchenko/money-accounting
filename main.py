from abc import ABC, abstractmethod
from datetime import date
from dateutil.relativedelta import relativedelta
from enum import Enum
from dataclasses import dataclass
from typing import List


class Capitalization(str, Enum):
    MONTHLY = "monthly"
    DAILY = "daily"
    END = "end"


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
        return deposit.initial_amount * (deposit.interest_rate / 100) * (deposit.term_months / 12)


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculator = self._create_calculator()

    def _create_calculator(self) -> InterestCalculator:
        calculators = {
            Capitalization.MONTHLY: MonthlyInterestCalculator(),
            Capitalization.DAILY: DailyInterestCalculator(),
            Capitalization.END: EndTermInterestCalculator()
        }
        return calculators[self.capitalization]

    def calculate_profit(self, months: int) -> float:
        return round(self.calculator.calculate_profit(self, months), 2)

    def calculate_amount(self, months: int) -> float:
        profit = self.calculate_profit(months)
        return round(self.initial_amount + profit, 2)


class Portfolio:
    def __init__(self):
        self.deposits: List[Deposit] = []

    def add_deposit(self, *deposits: Deposit):
        self.deposits.extend(deposits)

    def get_deposit_names(self) -> List[str]:
        return [deposit.name for deposit in self.deposits]

    def calculate_total(self, target_months: int) -> float:
        total = 0.0
        for deposit in self.deposits:
            # Учитываем только действующие вклады
            if target_months <= deposit.term_months:
                total += deposit.calculate_amount(target_months)
        return total

    def forecast(self, periods: List[int]) -> dict:
        return {months: self.calculate_total(months) for months in periods}


# Пример использования
if __name__ == "__main__":
    # Создаем портфель сбережений
    portfolio = Portfolio()

    deposit_tinkof = Deposit(
        name="deposit_tinkof",
        initial_amount=10000,
        interest_rate=19.0,
        term_months=3,
        date_from=date.today(),
        capitalization='monthly'
    )

    deposit_alfa = Deposit(
        name="deposit_alfa",
        initial_amount=100000,
        interest_rate=20.03,
        term_months=3,
        date_from=date.today(),
        capitalization='monthly'
    )

    print("deposit_tinkof", deposit_tinkof.calculate_amount(months=2))
    print("deposit_tinkof", deposit_tinkof.calculate_profit(months=2))

    portfolio.add_deposit(
        deposit_tinkof,
        deposit_alfa
    )
    # print(portfolio.get_deposit_names())
    # print("forecast=", forecast)
    # Делаем прогноз на разные периоды
    forecast = portfolio.forecast([3, 6, 12])


