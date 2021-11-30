from fastapi import APIRouter
from models import *

fast_router = APIRouter()


# GET `/main-admin`
# - Get all offices, total expenses, yearly expenses, total income, yearly income, total amount, yearly amount from the database.
# - Request Arguments: None
# - Returns: number of total offices, total expenses, yearly expenses, total income, yearly income, total amount, yearly amount.
# Example Response `{
#     "offices_number": 10,
#     "total_expenses": 4325,
#     "yearly_expenses": 4325,
#     "total_income": 234,
#     "yearly_income": 234,
#     "total_amount": 5464,
#     "yearly_amount": 3456,
#     "success": true,
# }`
@fast_router.get('/main-admin')
async def main_admin():
    return {
        "offices_number": await Offices.all().count(),
    }
