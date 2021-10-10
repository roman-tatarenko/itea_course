import datetime
import json
import random
from sanic import Sanic

from crm_project.MailSender import Sender
from crm_project.database_session import AsyncDbClient, DB_URL
from sanic.response import HTTPResponse, text

web_app = Sanic("my_crm_application")

db_client = AsyncDbClient(DB_URL)
web_app.db_client = db_client

role = None


@web_app.listener('before_server_start')
async def setup_resources(app, loop):
    await app.db_client.setup()


@web_app.route(methods=['POST'], uri='api/v1/create/department')
async def create_department(request):
    get_department_from_db = str(await web_app.db_client.get_department(
        department_name=request.json['department_name']))
    if get_department_from_db == "[]":
        await web_app.db_client.create_new_department(
            department_name=request.json['department_name'])
        return text(f"{request.json['department_name']} was created into departments table")
    else:
        return text(f"{request.json['department_name']} could not created into departments table")


@web_app.route(methods=['PUT'], uri='api/v1/update/department')
async def update_department(request):
    get_department_from_db = str(await web_app.db_client.get_department(
        department_name=request.json['old_department_name']))
    if get_department_from_db != "[]":
        await web_app.db_client.update_department(
            old_department_name=request.json['old_department_name'],
            new_department_name=request.json['new_department_name'])
        return text(f"{request.json['old_department_name']} was updated into departments table")
    else:
        return text(f"{request.json['old_department_name']} could not updated into departments table")


@web_app.route(methods=['DELETE'], uri='api/v1/delete/department')
async def update_department(request):
    get_department_from_db = str(await web_app.db_client.get_department(
        department_name=request.json['department_name']))
    if get_department_from_db != "[]":
        await web_app.db_client.delete_department(
            department_name=request.json['department_name'])
        return text(f"{request.json['department_name']} was deleted into departments table")
    else:
        return text(f"{request.json['department_name']} could not deleted into departments table")


@web_app.route(methods=['POST'], uri='api/v1/create/employee')
async def create_employee(request):
    get_employee_from_db = str(await web_app.db_client.get_employee_by_lastname(
        employee_name=request.json['employee_name']))
    if get_employee_from_db == "[]":
        await web_app.db_client.create_new_employee(
            employee_name=request.json['employee_name'],
            employee_position=request.json['employee_position'],
            department_id=request.json['department_id'])
        get_employee_id_from_db = await web_app.db_client.get_employee_by_lastname(
            employee_name=request.json['employee_name'])
        get_employee_id_from_db_as_dict = json.dumps(dict(list(get_employee_id_from_db)[0]))
        return HTTPResponse(f" New employee was created into employees table with value:  "
                            f"{get_employee_id_from_db_as_dict}")
    else:
        return text(f"New employee could not created into employees table")


@web_app.route(methods=['PUT'], uri='api/v1/update/employee')
async def update_employee(request):
    get_employee_from_db = str(await web_app.db_client.get_employee_by_id(
        employee_id=request.json['employee_id']))
    if get_employee_from_db != "[]":
        await web_app.db_client.update_employee(
            employee_name=request.json['employee_name'],
            job_position=request.json['employee_position'],
            department_id=request.json['department_id'],
            employee_id=request.json['employee_id'])
        get_employee_value_from_db = await web_app.db_client.get_employee_by_id(
            employee_id=request.json['employee_id'])
        get_employee_value_from_db_as_dict = json.dumps(dict(list(get_employee_value_from_db)[0]))
        return HTTPResponse(f" The employee was updated into employees table with value:  "
                            f"{get_employee_value_from_db_as_dict}")
    else:
        return text(f"New employee could not updated into employees table")


@web_app.route(methods=['DELETE'], uri='api/v1/delete/employee')
async def delete_employee(request):
    get_employee_from_db = str(await web_app.db_client.get_employee_by_id(
        employee_id=request.json['employee_id']))
    if get_employee_from_db != "[]":
        await web_app.db_client.delete_employee(
            employee_id=request.json['employee_id'])
        return text(f"{request.json['employee_id']} was deleted into employees table")
    else:
        return text(f"{request.json['employee_id']} could not deleted into employees table")


@web_app.route(methods=['POST'], uri='api/v1/create/client')
async def create_client(request):
    get_client_from_db = str(await web_app.db_client.get_client_by_contract(
        contract=request.json['contract']))
    if get_client_from_db == "[]":
        await web_app.db_client.create_new_client(
            legal_name=request.json['legal_name'],
            contract=request.json['contract'],
            email=request.json['email']
        )
        get_client_id_from_db = await web_app.db_client.get_client_by_contract(
            contract=request.json['contract'])
        get_client_id_from_db_as_dict = json.dumps(dict(list(get_client_id_from_db)[0]))
        return HTTPResponse(f" New record was created into clients table with value:  "
                            f"{get_client_id_from_db_as_dict}")
    else:
        return text(f"New record could not created into clients table")


@web_app.route(methods=['POST'], uri='api/v1/create/order')
async def create_order(request):
    date = datetime.datetime.now()
    created_date = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    get_employee_from_db = await web_app.db_client.get_all_employee_id(
        job_position="manager")
    random_id = random.choice(get_employee_from_db)
    if str(get_employee_from_db) != "[]":
        assigned_to = int(list(random_id)[0])
        await web_app.db_client.create_new_order(
            created_dt=created_date,
            order_type=request.json['order_type'],
            description=request.json['description'],
            status="New",
            serial_no=request.json['serial_no'],
            client_id=request.json['client_id'],
            assigned_to=assigned_to)
        get_order_id_from_db = await web_app.db_client.get_order_by_value(
            created_dt=created_date,
            order_type=request.json['order_type'],
            description=request.json['description'],
            status="New",
            serial_no=request.json['serial_no'],
            client_id=request.json['client_id'],
            assigned_to=assigned_to)
        get_order_id_from_db_as_dict = json.dumps(dict(list(get_order_id_from_db)[0]))
        get_client_from_db = await web_app.db_client.get_email_by_id(
            client_id=request.json['client_id'])
        get_client_email_from_db_as_dict = json.dumps(dict(list(get_client_from_db)[0]))
        Sender(to_email=get_client_email_from_db_as_dict['email'],
               message=f" New order was created.{get_order_id_from_db_as_dict}").send_message()
        return HTTPResponse(f" New order was created."
                            f"{get_order_id_from_db_as_dict}")
    else:
        return text(f"New order could not created into orders table")


@web_app.route(methods=['GET'], uri='api/v1/get/role')
async def get_role(request):
    params = dict(list(request.query_args))
    res = await web_app.db_client.get_role(
        user_name=params['username'],
        user_password=params['password'])
    res_as_list = list(res)
    department_from_db = dict(res_as_list[0])
    return HTTPResponse(json.dumps(department_from_db))


@web_app.route(methods=['GET'], uri='api/v1/get/department')
async def get_department(request):
    param_1 = dict(list(request.query_args))
    res = await web_app.db_client.get_department(
        department_name=param_1['department_name'])
    res_as_list = list(res)
    department_from_db = dict(res_as_list[0])
    return HTTPResponse(json.dumps(department_from_db))


if __name__ == '__main__':
    web_app.run(host='127.0.0.1', port=5000)
