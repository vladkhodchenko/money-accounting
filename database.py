import sqlalchemy

from deposits.models import Deposit
from sqlalchemy.orm import sessionmaker
from datetime import date

DIR = "/mnt/c/Users/sidyu/Documents/code/development/onlycash"

engine=sqlalchemy.create_engine(f'sqlite:///{DIR}/onlycash.db')

session = sessionmaker(bind=engine)


# session = Session()

# session.add_all(
#     [
#         Deposit(
#             name="ВТБ - вклад1",
#             # name_bank = "VTB",
#             initial_amount=100000.0,
#             interest_rate=5.5,
#             term_months=12,
#             date_from=date(2023, 1, 1),
#             date_to=date(2024, 1, 1),
#             capitalization_id=1,  # MONTHLY
#         )
#     ]
# )

# session.commit()

# session.close()

# print("База данных успешно создана и заполнена тестовыми данными!")