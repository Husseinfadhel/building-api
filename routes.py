import signal
from fastapi import APIRouter
from models import *
import datetime
from tortoise.transactions import in_transaction
from random import randrange
from starlette.exceptions import HTTPException as StarletteHTTPException
import os

fast_router = APIRouter()


# register a new user
@fast_router.post('/register')
async def register(username: str, password: str, name: str, building: str):
    try:    
        async with in_transaction() as conn:
            new = Users(username=username, password=password, name=name, building=building)
            await new.save(using_db=conn)
            return {
                "success": True,
            }
    except:
        raise StarletteHTTPException(500, "internal Server Error")


# login route
@fast_router.post('/login')
async def login(username: str, password: str):
    query = await Users.filter(username=username).first()
    try:
        if query.username == username and query.password == password:
            return {
                "success": True,
                "token": randrange(999999999, 1000000000000000),
                "id": query.id,
                "name": query.name,
                "username": query.username,
                "password": query.password,
                "building": query.building
            }
    except: 
        raise StarletteHTTPException(401, "Unauthorized")


# to get users
@fast_router.get('/users')
async def get_users():
    try:
        return {
            "users": await Users.all(),
        }
    except:
        raise StarletteHTTPException(404, "Not Found")


# to modify user
@fast_router.patch('/user')
async def patch_user(user_id: int, name: str, username: str, password: str, building: str):
    try:
        await Users.filter(id=user_id).update(name=name, username=username, password=password, building=building)
        return {
            "success": True
        }
    except:
        raise StarletteHTTPException(500, "internal Server Error")


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
    offices = await Offices.all().order_by("name")
    all_offices = []
    for office in offices:
        off = await OfficeDetails.filter(office_id=office.id).order_by("-renter").first()
        if off == None:
            json_details = {"id": office.id, "name": office.name}
        else:
            json_details = {"id": office.id, "name": office.name, "renter": off.renter,}
        all_offices.append(json_details)
    return {
        "offices": all_offices,
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

@fast_router.patch('/offices')
async def patch_office(office_id: int, name: str):
    await Offices.filter(id=office_id).update(name=name)
    return {
        "name": name,
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
async def get_office_details(office_id):
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
        notify = Notifications(office_details_id=new.id)
        await notify.save(using_db=conn)
    return {
        "renter": new.renter,
        "success": True
    }

@fast_router.patch('/offices/{office_id}')
async def patch_office_details(office_details_id: int, office_id, renter: str, date_of_receipt: str, date_of_claiming: str, amount: float,
                              notes: str):
    await OfficeDetails.filter(id=office_details_id).update(renter=renter, date_of_receipt=date_of_receipt, date_of_claiming=date_of_claiming, amount=amount, notes=notes)
    await Notifications.filter(office_details_id=office_details_id).update(seen=0)
    return {
        "renter": renter,
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
async def post_expenses( name: str, expense_type: str,
                        amount: float, date: str):
    async with in_transaction() as conn:
        new = Expenses( name=name, type=expense_type,
                       amount=amount, date=date)
        await new.save(using_db=conn)
    return {
        "id": new.id,
        "success": True
    }

@fast_router.patch('/expenses/{expense_id}')
async def patch_expenses( expense_id, name: str, expense_type: str,
                        amount: float, date: str):
    await Expenses.filter(id=expense_id).update(name=name, type=expense_type, amount=amount, date=date)
    return {
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
    notifications = await Notifications.all().prefetch_related('office_details')
    notifications_list = [(n.id, n.seen, n.office_details.id, n.office_details.renter, n.office_details.date_of_receipt, n.office_details.date_of_claiming, n.office_details.amount, n.office_details.notes, n.office_details.office_id) for n in notifications]
    notifications_jsons = []
    for record in notifications_list:
        office = await Offices.filter(id= record[8]).first()
        notifications = {'id': record[0], 'seen': record[1], 'office_details_id': record[2], 'renter': record[3], 'date_of_receipt': record[4], 'date_of_claiming': record[5], 'amount': record[6], 'notes': record[7], 'office_name': office.name}
        notifications_jsons.append(notifications)
    return {
        "notifications": notifications_jsons,
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

@fast_router.delete('/offices')
async def delete_offices(office_id: int):
    await Offices.filter(id=office_id).delete()
    return {
        "success": True
    }

@fast_router.delete('/offices/{office_id}')
async def delete_office_details(office_details_id: int):
    await OfficeDetails.filter(id=office_details_id).delete()
    return {
        "success": True
    }
    
@fast_router.delete('/expenses/{expense_id}')
async def delete_expenses(expense_id):
    await Expenses.filter(id=expense_id).delete()
    return {
        "success": True
    }

@fast_router.get('/shutdown')
def shut():
    pid = os.getpid()
    print(pid)
    os.kill(pid, signal.CTRL_C_EVENT)