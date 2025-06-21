from fastapi import Query
from typing import Annotated
from fastapi.routing import APIRouter
from services import expense as service
from core.database.setup import SessionDep
from schemas.expense import ExpenseSchema, ExpenseResponseSchema


router = APIRouter()


@router.get(
    "/",
    response_model=list[ExpenseResponseSchema],
    name="Get all expenses for a user",
    status_code=200,
)
async def get_expenses(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    """
    Get all expenses for the authenticated user
    """
    return await service.get_expenses(session, offset, limit)


@router.post(
    "/",
    response_model=ExpenseResponseSchema,
    name="Create a new expense",
    status_code=200,
)
async def create_expense(expense: ExpenseSchema, session: SessionDep):
    """
    Create a new expense for the authenticated user
    """
    return await service.create_expense(expense, session)
