from enum import  Enum

from typing import List

from dataclasses import dataclass

from datetime import date
from dateutil.relativedelta import relativedelta



class Capitalization(str, Enum):
    MONTHLY = "monthly" # ежемесячная - каждый месяц прибавляются проценты
    DAY = "day"         # ежедневная - каждый день прибавляются проценты (как в яндексе)
    END = "end"         # в конце срока прибавляются проценты (самое невыгодное)



@dataclass
class Deposit:
    name: str
    initial_amount: float
    interest_rate: float
    term_months: int
    date_from: date
    capitalization: str = "monthly"

    @property
    def date_to(self):
        return self.date_from + relativedelta(months=self.term_months)
        
    def calculate_profit_in_month(self) -> float:
        profit = self.initial_amount * (self.interest_rate / 100 / 12)
        return round(profit, 2)

    def calculate_profit(self) -> float:
        profit = self.calculate_profit_in_month() * self.term_months
        return round(profit, 2)

    def calculate_amount(self) -> float:
        amount = self.initial_amount + self.calculate_profit()
        return round(amount, 2)


class Portfolio:
    def __init__(self):
        self.deposits: List[Deposit] = []
    
    def add_deposit(self, *deposits: Deposit):
        for deposit in deposits:
            self.deposits.append(deposit)
    
    def get_deposits(self):
        list_name_deposits = []
        for deposit in self.deposits:
            list_name_deposits.append(deposit.name)
        return list_name_deposits
        

    def calculate_total(self, target_months: int) -> float:
        """Рассчитывает общую сумму через заданное количество месяцев"""
        total = 0.0
        
        for deposit in self.deposits:
            total += deposit.initial_amount + deposit.calculate_profit_in_month() * target_months
        
        return round(total, 2)
    
    def forecast(self, periods: List[int]) -> dict:
        """Возвращает прогноз для списка периодов (в месяцах)"""
        return {months: self.calculate_total(months) for months in periods}



# Пример использования
if __name__ == "__main__":
    # Создаем портфель сбережений
    portfolio = Portfolio()
    

    deposit_tinkof = Deposit(
        name = "deposit_tinkof",
        initial_amount=10000,
        interest_rate=19.0,
        term_months=3,
        date_from = date.today(),
        capitalization='monthly'
    )

    deposit_alfa = Deposit(
        name = "deposit_alfa",
        initial_amount=100000,
        interest_rate=20.03,
        term_months=3,
        date_from = date.today(),
        capitalization='monthly'
    )

    print("deposit_tinkof", deposit_tinkof.calculate_amount())
    print("deposit_tinkof", deposit_tinkof.calculate_profit())

    portfolio.add_deposit(
        deposit_tinkof,
        deposit_alfa
    )
    print(portfolio.get_deposits())
    # Делаем прогноз на разные периоды
    forecast = portfolio.forecast([3, 6, 12])

    print(f"forecast=", forecast)