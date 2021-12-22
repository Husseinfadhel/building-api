from fastapi import APIRouter
from models import *
import datetime
from tortoise.transactions import in_transaction

fast_router = APIRouter()


# GET `/main-admin` - Get all offices, total expenses, yearly expenses, total income, yearly income, total amount,
# yearly amount from the database. - Request Arguments: None - Returns: number of total offices, total expenses,
# yearly expenses, total income, yearly income, total amount, yearly amount. Example Response `{ "offices_number":
# 10, "total_expenses": 4325, "yearly_expenses": 4325, "total_income": 234, "yearly_income": 234, "total_amount":
# 5464, "yearly_amount": 3456, "success": true, }`
@fast_router.get('/main-admin')
async def main_admin():
    total_exp = await Expenses.all()
    total_office = await OfficeDetails.all()
    year = datetime.datetime.now().year
    am = 0.0
    ym = 0.0
    for exp in total_exp:
        am += exp.amount
        date = str(exp.date)
        date = date.split('-')
        if year == int(date[0]):
            ym += exp.amount
    t_amount = 0.0
    y_amount = 0.0
    for off in total_office:
        t_amount += off.amount
        date = str(off.date_of_receipt)
        date = date.split('-')
        if year == int(date[0]):
            y_amount += off.amount
    t_income = t_amount - am
    y_income = y_amount - ym
    return {
        "offices_number": await Offices.all().count(),
        "total_expenses": am,
        "yearly_expenses": ym,
        "total_amount": t_amount,
        "yearly_amount": y_amount,
        "total_income": t_income,
        "yearly_income": y_income,
        "success": True

    }


# GET `/offices`
# - Get info about offices from the database.
# - Request Arguments: None
# - Returns: id and name.
#
# Example Response `{
#     "offices": [
#         {
#             "id": 1,
#             "name": "1"
#         }
#     ],
#     "success": true
# }`
@fast_router.get('/offices')
async def get_offices():
    return {
        "offices": await Offices.all(),
        "success": True
    }


# POST `/offices`
#
# - Add an office to the database.
# - Request Body: Name.
# - Returns: name of office.
#
# Example Request Payload `{
#     "name": "1"
# }`
#
# Example Response `{
#     "name": "1"
#     "success": true
# }`
@fast_router.post('/offices')
async def post_office(name: str):
    async with in_transaction() as conn:
        new = Offices(name=name)
        await new.save(using_db=conn)
    return {
        "name": new.name,
        "success": True
    }
