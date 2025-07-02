# Название
- onlycash (deprecated)
- catinbag

# Цель:
- мотивация - мативация
- копить/откладывать
- ставить финансовые цели/идти к ним и отслеживать прогресс

# TODO


## Backend 

### Базовый функционал
- [x] учитывать БАНК, и тип вклада
- [ ] Хранить информацию о вкладах/накопительных счетах
- [ ] авторизация аутентификация

### API
- GET на получение всех вкладов
- GET на получение одного вклада
- GET на получение вложенной суммы

- POST на создание
- PATCH на редактирование вклада
- DELETE на удаление


### Карта продукта, будущие фичи
- [ ] возможная отложенная сумма - при текущем накоплениие сумма составит столько-то
- [ ] возможная заработанная сумма - при текущем доходе сумма составит столько-то


- итоговый доход - отложенная сумма
- итоговые сбережения - суммы на вкладах + 
- учитывать разницу между вкладами с капитализацией и без неё
- 10 * процент - вклад без капитализации
- умножается сумма полученная каждый месяц на процент


## Frontend
-[] нужно считать примерный доход в месяц по типу как делает тинькоф -> доход в месяц
-[] желаемо отлаживаемый доход
- калькулятор сравнения: вклад под 19 с ежедневной капитализацией vs вклад под 20 с процентами только в конце


## Перспектива:
- мы можем отложить
- мы реально откладываем

```shell
желаемо
10к 10к 10к
|   |   |
10к 20к 30к
суммарно
```


# Пример использования
# if __name__ == "__main__":
#     # Создаем портфель сбережений
#     portfolio = Portfolio()

#     deposit_tinkof = Deposit(
#         name="deposit_tinkof",
#         initial_amount=10000,
#         interest_rate=19.0,
#         term_months=3,
#         date_from=date.today(),
#         capitalization='monthly'
#     )

#     deposit_alfa = Deposit(
#         name="deposit_alfa",
#         initial_amount=100000,
#         interest_rate=20.03,
#         term_months=3,
#         date_from=date.today(),
#         capitalization='monthly'
#     )

#     print("deposit_tinkof", deposit_tinkof.calculate_amount(months=2))
#     print("deposit_tinkof", deposit_tinkof.calculate_profit(months=2))

#     portfolio.add_deposit(
#         deposit_tinkof,
#         deposit_alfa
#     )
#     # print(portfolio.get_deposit_names())
#     # print("forecast=", forecast)
#     # Делаем прогноз на разные периоды
#     forecast = portfolio.forecast([3, 6, 12])
