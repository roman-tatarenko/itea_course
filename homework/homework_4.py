"""
Создать базу данных с произвольным именем для нашей будущей CRM. Определить в ней несколько таблиц:

Таблица ЗАЯВКИ (orders)
- id заявки (order_id) - целое число
- дата создания (created_dt) - date
- дата обновления заявки (updated_dt) - date
- тип заявки: например ремонт, консультация, плановое обслуживание (order_type) - текст
- описание (description) - текст
- статус заявки (status) - текст
- серийный номер аппарата (serial_no) - целое число
- id сотрудника-создателя заявки (creator_id) - целое число

Таблица СОТРУДНИКИ (employees)
- id сотрудника (employee_id) - целое число
- ФИО (fio) - текст
- должность (position) - текст
- id подразделения (department_id) - целое число

Таблица ПОДРАЗДЕЛЕНИЯ (departments)
- id подразделения (department_id) - целое число
- название подразделения (department_name) - текст

ВАЖНО! ИСПОЛЬЗОВАТЬ ТЕ ИМЕНА, КТОРЫЕ УКАЗАНЫ В ЗАДАНИИ!

Написать код создания таблиц на языке SQL, предусмотреть необходимые ограничения.
"""

departments = 'create table departments (' \
              'department_id SERIAL primary key,' \
              'department_name text not NULL);'

empoyees = 'create table employees (' \
           'employee_id SERIAL primary KEY,' \
           'fio text not NULL,' \
           '"position" TEXT,' \
           'department_id INT not NULL,' \
           'foreign key (department_id) references departments (department_id));'

orders = 'create table orders (' \
         'order_id SERIAL primary key,' \
         'created_dt DATE not NULL,' \
         'update_dt DATE,' \
         'order_type text not Null,' \
         'description TEXT,' \
         'status text not NUll,' \
         'serial_no INT not NUll,' \
         'creator_id INT not NUll,' \
         'foreign key (creator_id) references employees (employee_id));'



