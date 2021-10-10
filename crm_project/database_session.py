import argparse
import asyncpg
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument("--postgres_username", required=True, type=str)
parser.add_argument("--postgres_password", required=True, type=str)
parser.add_argument("--postgres_host", required=True, type=str)
parser.add_argument("--postgres_port", required=True, type=str)
parser.add_argument("--postgres_database", required=True, type=str)
args = parser.parse_args()

DB_URL = f"postgresql://{args.postgres_username}:{args.postgres_password}@{args.postgres_host}:{args.postgres_port}" \
         f"/{args.postgres_database}"


class AsyncDbClient:
    ROLE_SELECT_QUERY = "SELECT user_role FROM roles WHERE user_name = '%s' AND user_password = '%s';"
    DEPARTMENT_SELECT_QUERY = "SELECT department_name FROM departments WHERE department_name = '%s';"
    DEPARTMENT_INSERT_QUERY = "INSERT INTO departments (department_name) VALUES ('%s');"
    DEPARTMENT_UPDATE_QUERY = "UPDATE departments SET department_name = '%s' WHERE department_name = '%s';"
    DEPARTMENT_DELETE_QUERY = "DELETE FROM departments WHERE department_name = '%s';"

    EMPLOYEE_SELECT_QUERY_BY_LASTNAME = "SELECT * FROM employees WHERE lastname = '%s';"
    EMPLOYEE_SELECT_QUERY_ALL_ID = "SELECT employee_id FROM employees WHERE job_position = '%s';"
    EMPLOYEE_SELECT_QUERY_BY_ID = "SELECT * FROM employees WHERE employee_id = %d;"
    EMPLOYEE_INSERT_QUERY = "INSERT INTO employees (lastname, job_position, department_id) VALUES ('%s', '%s', %d);"
    EMPLOYEE_UPDATE_QUERY = "UPDATE employees SET lastname= '%s', job_position= '%s', department_id= %d " \
                            "WHERE employee_id = %d;"
    EMPLOYEE_DELETE_QUERY = "DELETE FROM employees WHERE employee_id = %d;"

    ORDER_INSERT_QUERY = "INSERT INTO orders (created_dt, order_type, description, status, serial_no, " \
                         "client_id, assigned_to) VALUES ('%s', '%s', '%s', '%s', %d, %d, %d);"
    ORDER_SELECT_QUERY = "SELECT order_id FROM orders WHERE created_dt = '%s' AND order_type = '%s' AND " \
                         "description = '%s' AND status = '%s' AND serial_no =  %d AND client_id = %d AND" \
                         " assigned_to = %d;"

    CLIENT_INSERT_QUERY = "INSERT INTO clients (legal_name, contract, email) VALUES ('%s', '%s', '%s');"
    CLIENT_SELECT_QUERY_BY_CONTRACT = "SELECT * FROM clients WHERE contract = '%s';"
    CLIENT_SELECT_QUERY_BY_ID = "SELECT email FROM clients WHERE client_id = %d;"

    def __init__(self, db_url):
        self.db_url = db_url
        self.db_pool = None

    async def setup(self):
        self.db_pool = await asyncpg.create_pool(DB_URL)

    def _check_connection(self):
        if not self.db_pool:
            print("Pool has not been set up! Please, user client.setup method to create pool!")
            return False
        return True

    async def get_role(self, user_name, user_password):
        """Получает возможные роли из таблица roles"""
        if self._check_connection():
            return await self.db_pool.fetch(self.ROLE_SELECT_QUERY % (user_name, user_password))

    async def get_department(self, department_name):
        """Получает департамент из таблицы departments"""
        if self._check_connection():
            return await self.db_pool.fetch(self.DEPARTMENT_SELECT_QUERY % department_name)

    async def create_new_department(self, department_name):
        """Создает департамент в таблице departments"""
        if self._check_connection():
            return await self.db_pool.fetch(self.DEPARTMENT_INSERT_QUERY % department_name)

    async def update_department(self, new_department_name, old_department_name):
        """Обновляет департамент в таблице departments"""
        if self._check_connection():
            return await self.db_pool.fetch(self.DEPARTMENT_UPDATE_QUERY % (new_department_name, old_department_name))

    async def delete_department(self, department_name):
        """Удаляет департамент в таблице departments"""
        if self._check_connection():
            return await self.db_pool.fetch(self.DEPARTMENT_DELETE_QUERY % department_name)

    async def get_employee_by_lastname(self, employee_name):
        """Получает сотруднка из таблицы employees"""
        if self._check_connection():
            return await self.db_pool.fetch(self.EMPLOYEE_SELECT_QUERY_BY_LASTNAME % employee_name)

    async def get_all_employee_id(self, job_position):
        """Получает сотруднка из таблицы employees"""
        if self._check_connection():
            return await self.db_pool.fetch(self.EMPLOYEE_SELECT_QUERY_ALL_ID % job_position)

    async def get_employee_by_id(self, employee_id):
        """Получает сотруднка из таблицы employees"""
        if self._check_connection():
            return await self.db_pool.fetch(self.EMPLOYEE_SELECT_QUERY_BY_ID % employee_id)

    async def create_new_employee(self, employee_name, employee_position, department_id):
        """Создает сотрудника в таблице employees"""
        if self._check_connection():
            return await self.db_pool.fetch(self.EMPLOYEE_INSERT_QUERY % (
                employee_name, employee_position, department_id))

    async def update_employee(self, employee_name, job_position, department_id, employee_id):
        """Обновляет сотрудника в таблице employees"""
        if self._check_connection():
            return await self.db_pool.fetch(self.EMPLOYEE_UPDATE_QUERY % (
                employee_name, job_position, department_id, employee_id))

    async def delete_employee(self, employee_id):
        """Удаляет сотрудника в таблице employees"""
        if self._check_connection():
            return await self.db_pool.fetch(self.EMPLOYEE_DELETE_QUERY % employee_id)

    async def create_new_order(self, created_dt, order_type, description, status, serial_no, client_id, assigned_to):
        """Создает сотрудника в таблице employees"""
        if self._check_connection():
            return await self.db_pool.fetch(self.ORDER_INSERT_QUERY % (
                created_dt, order_type, description, status, serial_no, client_id, assigned_to))

    async def create_new_client(self, legal_name, contract, email):
        """Создает Клиента в таблице clients"""
        if self._check_connection():
            return await self.db_pool.fetch(self.CLIENT_INSERT_QUERY % (legal_name, contract, email))

    async def get_client_by_contract(self, contract):
        """Получает Клиента из таблицы clients"""
        if self._check_connection():
            return await self.db_pool.fetch(self.CLIENT_SELECT_QUERY_BY_CONTRACT % contract)

    async def get_email_by_id(self, client_id):
        """Получает Клиента из таблицы clients"""
        if self._check_connection():
            return await self.db_pool.fetch(self.CLIENT_SELECT_QUERY_BY_ID % client_id)

    async def get_order_by_value(self, created_dt, order_type, description, status, serial_no, client_id, assigned_to):
        """Получает Клиента из таблицы clients"""
        if self._check_connection():
            return await self.db_pool.fetch(self.ORDER_SELECT_QUERY % (
                created_dt, order_type, description, status, serial_no, client_id, assigned_to))


loop = asyncio.get_event_loop()
