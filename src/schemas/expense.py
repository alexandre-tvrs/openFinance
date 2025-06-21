from uuid import UUID
from pydantic import BaseModel


class ExpenseSchema(BaseModel):
    name: str
    value: float
    in_installments: bool


class ExpenseResponseSchema(ExpenseSchema):
    id: UUID
    ...
