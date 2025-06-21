from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field


class ExpenseModel(SQLModel, table=True):
    __tablename__ = "Expense"
    id: UUID = Field(default=uuid4(), primary_key=True)
    name: str = Field(index=True)
    value: float = Field()
    in_installments: bool = Field()
