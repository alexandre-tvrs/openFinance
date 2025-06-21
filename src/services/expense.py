from uuid import uuid4
from fastapi import Query
from sqlmodel import select
from typing import Annotated
from models.expense import ExpenseModel
from core.database.setup import SessionDep
from schemas.expense import ExpenseSchema, ExpenseResponseSchema


async def get_expenses(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[ExpenseResponseSchema]:
    expenses = session.exec(select(ExpenseModel).offset(offset).limit(limit)).all()
    return [ExpenseResponseSchema(**expense.model_dump()) for expense in expenses]


async def create_expense(
    test: ExpenseSchema, session: SessionDep
) -> ExpenseResponseSchema:
    expense = ExpenseModel(**test.model_dump())
    expense.id = uuid4()
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return ExpenseResponseSchema(**expense.model_dump())
