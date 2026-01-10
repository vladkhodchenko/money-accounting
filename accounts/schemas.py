from pydantic import BaseModel
from typing import List


class SPortfolio(BaseModel):
    deposits: List[str]
