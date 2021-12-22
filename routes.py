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


# GET `/offices/<office_id>`
# - Get office details from the database.
# - Request Arguments: Page Number.
# - Returns: List of date of receipt, date of claiming, amount and notes.
# Example Response `{
#     "office_details": [
#         {
#             "id": 1,
#             "renter": "علي",
#             "date_of_receipt": "1",
#             "date_of_claiming": "1",
#             "amount": 1,
#             "notes": "1",
#         }
#     ],
#     "success": true
# }`
@fast_router.get('/offices/{office_id}')
async def office_details(office_id):
    off = await OfficeDetails.filter(office_id=office_id).all()
    all_offices = []
    for f in off:
        json_details = {"id": f.id, "renter": f.renter, "date_of_receipt": f.date_of_receipt,
                        "date_of_claiming": f.date_of_claiming, "amount": f.amount, "notes": f.notes}
        all_offices.append(json_details)
    return {
        "office_details": all_offices,
        "success": True
    }


# POST `/offices/<office_id>`
# - Add office details to the database.
# - Request Body: renter, date of receipt, date of claiming, amount and notes.
# - Returns: renter of office.
# Example Request Payload `{
#     "renter": "علي",
#     "date_of_receipt": "1",
#     "date_of_claiming": "1",
#     "amount": 1,
#     "notes": "1",
# }`
# Example Response `{
#     "renter": "علي",
#     "success": true
# }`
@fast_router.post('/offices/{office_id}')
async def post_office_details(office_id, renter: str, date_of_receipt: str, date_of_claiming: str, amount: float,
                              notes: str):
    async with in_transaction() as conn:
        new = OfficeDetails(office_id=office_id, renter=renter, date_of_receipt=date_of_receipt,
                            date_of_claiming=date_of_claiming, amount=amount, notes=notes)
        await new.save(using_db=conn)
    return {
        "renter": new.renter,
        "success": True
    }


# GET `/expenses`
# - Get expenses from the database.
# - Request Arguments: Page Number.
# - Returns: List of date of receipt, date of claiming, amount and notes.
# Example Response `{
#     "expenses": [
#         {
#             "id": 1,
#             "voucher_number": 1,
#             "name": "علي"
#             "type": "اصلاحيات",
#             "amount": 1,
#         }
#     ],
#     "success": true
# }`
@fast_router.get('/expenses')
async def get_expenses():
    return {
        "expenses": await Expenses.all(),
        "success": True
    }


# POST `/expenses`
# - Add an expense to the database.
# - Request Body: renter, date of receipt, date of claiming, amount and notes.
# - Returns: renter of office.
# Example Request Payload `{
#     "voucher_number": 1,
#     "name": "علي"
#     "type": "اصلاحيات",
#     "amount": 1,
# }`
# Example Response `{
#     "voucher_number": 12,
#     "success": true
# }`
@fast_router.post('/expenses')
async def post_expenses(voucher_number: int, name: str, expense_type: str,
                        amount: float, date: str):
    async with in_transaction() as conn:
        new = Expenses(voucher_number=voucher_number, name=name, type=expense_type,
                       amount=amount, date=date)
        await new.save(using_db=conn)
    return {
        "voucher_number": new.voucher_number,
        "success": True
    }


# GET `/notifications`
# - Get notifications about date of claiming from the database.
# - Request Arguments: None
# - Returns: id, date_of_claiming and seen.
# Example Response `{
#     "notifications": [
#         {
#             "id": 1,
#             "date_of_claiming": "1",
#             "seen": 0
#         }
#     ],
#     "success": true
# }`
@fast_router.get('/notifications')
async def get_notify():
    return {
        "notifications": await Notifications.all(),
        "success": True
    }


# PATCH `/notifications/<notification_id>`
# - Change the notification seen state to 1 in the database.
# - Request Arguments: notification_id
# - Returns: None.
# Example Response `{
#     "success": true
# }`
@fast_router.patch('/notifications/{notification_id}')
async def patch_notification(notification_id):
    await Notifications.filter(id=notification_id).update(seen=1)
    return {
        "success": True
    }