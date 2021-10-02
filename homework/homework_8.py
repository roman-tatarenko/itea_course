"""
Вам нужно создать своего собственного телеграмм-бота. Для бота реализовать следующий набор команд на основе прошлых
дз которые будут:

- отдавать перечень заявок в определённом статусе (можно выбрать любой) за конкретный день, созданных
конкретным сотрудником;
- отдавать перечень сотрудников и департаментов, в которых они работают;
- отдавать количество заявок в определенном статусе (можно выбрать любой) по дням;
- отдавать перечень id заявок и ФИО сотрудников, которые их создали.
- получение сотрудника, департамента, заявки по id


Так как у нас может быть очень много данных в базе, поэтому все общие выдачи ограничить 5ю элементами.
"""

# Внимание:
# Параметры: --postgres_username=roman --postgres_password= --postgres_host=localhost --postgres_port=5432
# --postgres_database=crm_studio
# Бот называется alpha_project_crm_bot_02102021
# Переменная окружения(токен) PYTHONUNBUFFERED=1;TOKEN=2007099196:AAG6ja5-BCPHG_OSAuUaHhc2Hd0PbmM7UP4
import psycopg2
import argparse
from datetime import datetime
import requests
import telebot.types
from telebot import TeleBot
from envparse import Env

parser = argparse.ArgumentParser()
parser.add_argument("--postgres_username", required=True, type=str)
parser.add_argument("--postgres_password", required=True, type=str)
parser.add_argument("--postgres_host", required=True, type=str)
parser.add_argument("--postgres_port", required=True, type=str)
parser.add_argument("--postgres_database", required=True, type=str)
args = parser.parse_args()

DB_URL = f"postgresql://{args.postgres_username}:{args.postgres_password}@{args.postgres_host}:{args.postgres_port}" \
         f"/{args.postgres_database}"

connection_to_database = psycopg2.connect(DB_URL)

select_available_order_status = "SELECT status FROM orders;"
select_available_order_date = "SELECT created_dt FROM orders;"
select_available_employee = "SELECT employee_id, fio FROM employees;"

env = Env()
TOKEN = env.str('TOKEN')
ADMIN_CHAT_ID = 1011486660
bot = TeleBot(TOKEN)

order_status = None
order_date = None
order_employee_id = None

with connection_to_database.cursor() as cursor_zero:
    cursor_zero.execute(select_available_order_status)
    available_order_status = set(cursor_zero.fetchall())

    string = str(available_order_status).replace('{', '').replace('}', '').replace('(', '').replace(',)', '')
    string = string.replace("'", "")
    button = string.split(',')

    cursor_zero.execute(select_available_order_date)
    available_order_date = set(cursor_zero.fetchall())
    button_of_date = str(available_order_date)
    button_of_date = button_of_date.replace('{', '').replace('}', '').replace('datetime.date(', '')
    button_of_date = button_of_date.replace(',)', '').replace("'", "").replace(",", "").replace("(", "")
    button_of_date = button_of_date.split(') ')
    button_of_date = str(button_of_date).replace(' ', '-').replace('[', '').replace(']', '').replace("-'", "")
    button_of_date = button_of_date.replace("'", "").replace(")", "")
    button_of_date = button_of_date.split(',')
    button_of_date_list_as_list = list()
    for month in button_of_date:
        like_date = datetime.strptime(month, '%Y-%m-%d')
        like_str = datetime.strftime(like_date, '%Y-%m-%d')
        button_of_date_list_as_list.append(like_str)
    button_of_date_list_as_string = str(button_of_date_list_as_list)

    cursor_zero.execute(select_available_employee)
    available_order_employee = set(cursor_zero.fetchall())
    button_of_employee = str(available_order_employee)
    button_of_employee = button_of_employee.replace('{', '').replace('}', '')
    button_of_employee = button_of_employee.split('),')
    button_of_employee_list_as_string = str(button_of_employee)


@bot.message_handler(commands=['start'], content_types=['text'])
def say_hello_for_new_user(message):
    bot.reply_to(message, f"Hello dear, {message.from_user.full_name}!")


@bot.message_handler(commands=['get_order'], content_types=['text'])
def get_order(message_one):
    quantity = len(available_order_status) - 1
    user_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_list = list()
    while quantity >= 0:
        user_keyboard.row().add(f"{button[quantity]}")
        button_list.append(button[quantity])
        quantity -= 1

    bot.send_message(chat_id=message_one.chat.id,
                     text="What kind of order status do you need?",
                     reply_markup=user_keyboard)

    @bot.message_handler(content_types=['text'])
    def handle_text_data(message_two):
        with connection_to_database.cursor() as cursor_second:
            try:
                global order_status
                global order_date
                global order_employee_id
                button_list_as_string = str(button_list)
                try:
                    if message_two.text in button_list_as_string:
                        hide_keyboard = telebot.types.ReplyKeyboardRemove()
                        bot.send_message(chat_id=message_two.chat.id,
                                         text=f"'{message_two.text}' status was selected",
                                         reply_markup=hide_keyboard)
                        order_status = message_two.text

                        quantity_of_date = len(button_of_date_list_as_list) - 1
                        user_keyboard_of_date = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                  one_time_keyboard=True)
                        button_of_date_list = list()
                        while quantity_of_date >= 0:
                            user_keyboard_of_date.row().add(f"{button_of_date_list_as_list[quantity_of_date]}")
                            button_of_date_list.append(button_of_date_list_as_list[quantity_of_date])
                            quantity_of_date -= 1
                        bot.send_message(chat_id=message_two.chat.id,
                                         text="What kind of order date do you need?",
                                         reply_markup=user_keyboard_of_date)
                    elif message_two.text in button_of_date_list_as_string:
                        hide_keyboard = telebot.types.ReplyKeyboardRemove()
                        bot.send_message(chat_id=message_two.chat.id,
                                         text=f"'{message_two.text}' date was selected",
                                         reply_markup=hide_keyboard)
                        order_date = message_two.text

                        quantity_of_employee = len(button_of_employee) - 1
                        user_keyboard_of_employee = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                      one_time_keyboard=True)
                        button_of_employee_list = list()
                        while quantity_of_employee >= 0:
                            button_of_employee_clean = button_of_employee[quantity_of_employee].replace('(', '')
                            button_of_employee_clean = button_of_employee_clean.replace(')', '')
                            user_keyboard_of_employee.row().add(f"{button_of_employee_clean}")
                            button_of_employee_list.append(button_of_employee_clean)
                            quantity_of_employee -= 1
                        bot.send_message(chat_id=message_two.chat.id,
                                         text="What kind of employee data do you need?",
                                         reply_markup=user_keyboard_of_employee)
                    elif message_two.text in button_of_employee_list_as_string:
                        hide_keyboard = telebot.types.ReplyKeyboardRemove()
                        bot.send_message(chat_id=message_two.chat.id,
                                         text=f"'{message_two.text}' employee was selected",
                                         reply_markup=hide_keyboard)
                        order_employee = message_two.text
                        order_employee = order_employee.split(',')
                        order_employee_id = int(order_employee[0])
                        try:
                            select_orders = f"SELECT order_id FROM orders WHERE status='{order_status}' AND " \
                                            f"created_dt='{order_date}' AND creator_id={order_employee_id} LIMIT 5;"
                            cursor_second.execute(select_orders)
                            order_by_params = set(cursor_second.fetchall())
                            if order_by_params != set():
                                bot.reply_to(message_two, f"The id of order is {order_by_params}")
                            else:
                                bot.reply_to(message_two, f"The id of order is empty by your params.")
                        except Exception:
                            raise Exception("Impossible to execute SQL request.")
                    else:
                        bot.reply_to(message_two, "You did not choose correct value from menu. "
                                                  "Please, resend the request.")
                        raise TeleBot
                except ValueError:
                    log_msg_one = f"User {message_two.from_user.id} choose invalid value '{message_two.text}' " \
                                  f"at {datetime.now()}\n"
                    with open('logfile.txt', 'a') as logfile:
                        logfile.write(log_msg_one)
                        requests.get(
                            url=f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}"
                                f"&text={log_msg_one}")
                    raise ValueError("Unknown the data.")
            except ValueError:
                bot.reply_to(message_two, "You did not choose correct value from menu. Please, resend the request.")


@bot.message_handler(commands=['get_employees_and_departments'], content_types=['text'])
def get_employees_and_departments(message_one):
    with connection_to_database.cursor() as cursor_first:
        cursor_first.execute("""SELECT fio, department_name FROM employees INNER JOIN departments
                                        ON employees.department_id= departments.department_id LIMIT 5;""")
        employees_and_departments = cursor_first.fetchall()
        my_list = []
        for x in employees_and_departments:
            my_list.append(' | '.join(x))
        employees_and_departments_finished = '\n'.join(my_list)
        bot.reply_to(message_one, employees_and_departments_finished)


@bot.message_handler(commands=['get_count_of_order'], content_types=['text'])
def get_count_of_order(message_one):
    quantity = len(available_order_status) - 1
    user_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_list = list()
    while quantity >= 0:
        user_keyboard.row().add(f"{button[quantity]}")
        button_list.append(button[quantity])
        quantity -= 1

    bot.send_message(chat_id=message_one.chat.id,
                     text="What kind of order status do you need?",
                     reply_markup=user_keyboard)

    @bot.message_handler(content_types=['text'])
    def handle_text_data(message_two):
        with connection_to_database.cursor() as cursor_second:
            try:
                global order_status
                global order_date
                button_list_as_string = str(button_list)
                try:
                    if message_two.text in button_list_as_string:
                        hide_keyboard = telebot.types.ReplyKeyboardRemove()
                        bot.send_message(chat_id=message_two.chat.id,
                                         text=f"'{message_two.text}' status was selected",
                                         reply_markup=hide_keyboard)
                        order_status = message_two.text

                        bot.send_message(chat_id=message_two.chat.id,
                                         text="Please, set the some date YYYY-MM-DD")

                    elif message_two.text in button_of_date_list_as_string:
                        hide_keyboard = telebot.types.ReplyKeyboardRemove()
                        bot.send_message(chat_id=message_two.chat.id,
                                         text=f"'{message_two.text}' date was selected",
                                         reply_markup=hide_keyboard)
                        order_date = message_two.text

                        try:
                            select_count_of_orders = f"SELECT count(status) FROM orders WHERE " \
                                                     f"created_dt='{order_date}' " \
                                                     f"AND status='{order_status}' LIMIT 5;"
                            cursor_second.execute(select_count_of_orders)
                            quantity_of_order = cursor_second.fetchall()
                            bot.send_message(chat_id=message_two.chat.id,
                                             text=f"The quantity of order is {quantity_of_order}")
                        except Exception:
                            raise Exception("Impossible to execute SQL request.")
                    else:
                        bot.reply_to(message_two, "You did not choose correct value. "
                                                  "Please, resend the request.")
                        raise TeleBot
                except ValueError:
                    log_msg_one = f"User {message_two.from_user.id} choose invalid value '{message_two.text}' " \
                                  f"at {datetime.now()}\n"
                    with open('logfile.txt', 'a') as logfile:
                        logfile.write(log_msg_one)
                        requests.get(
                            url=f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}"
                                f"&text={log_msg_one}")
                    raise ValueError("Unknown the data.")
            except ValueError:
                bot.reply_to(message_two, "You did not choose correct value. Please, resend the request.")


@bot.message_handler(commands=['get_order_id_and_employees'], content_types=['text'])
def get_order_id_and_employees(message_one):
    with connection_to_database.cursor() as cursor_first:
        cursor_first.execute("""SELECT order_id, fio FROM orders INNER JOIN employees ON 
                                    orders.creator_id = employees.employee_id LIMIT 5;""")
        order_id_and_employees = cursor_first.fetchall()
        my_list = []
        for x in order_id_and_employees:
            my_list.append(f"{x}")

        my_list = set(my_list)
        order_id_and_employees_finished = '\n'.join(my_list)
        bot.reply_to(message_one, order_id_and_employees_finished)


@bot.message_handler(commands=['get_order_id_and_employees_and_departments'], content_types=['text'])
def get_order_id_and_employees_and_departments(message_one):
    with connection_to_database.cursor() as cursor_first:
        cursor_first.execute("""SELECT order_id, fio, department_name FROM orders INNER JOIN employees ON 
                                orders.creator_id = employees.employee_id INNER JOIN departments ON 
                                employees.department_id = departments.department_id LIMIT 5;""")
        order_id_and_employees_and_departments = cursor_first.fetchall()
        my_list = []
        for x in order_id_and_employees_and_departments:
            my_list.append(f"{x}")

        my_list = set(my_list)
        order_id_and_employees_and_departments_finished = '\n'.join(my_list)
        bot.reply_to(message_one, order_id_and_employees_and_departments_finished)


while True:
    try:
        bot.polling()
    except Exception as err:
        log_msg = f"The Bot was felt down at {datetime.now()}\n with error {err}"
        with open('logfile.txt', 'a') as logfile:
            logfile.write(log_msg)
            requests.get(url=f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text={log_msg}")
