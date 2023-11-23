import os
import sqlite3
import telebot

from os.path import join, dirname
from dotenv import load_dotenv  # Загрузка токена из 'env.' файла
from integrations.buttons import *
from integrations.import_lead import set_lead
from integrations.validation import check_symbol_for_email, check_symbols_for_phone
from integrations.cleaning_the_list import filtered


def get_from_env(key: str):
    """Загрузка токена по ключу"""
    dotenv_path = join(dirname(__file__), 'config/token.env')
    load_dotenv(dotenv_path)  # в той же папке, где находится python файл, есть файл с названием bot.env
    return os.environ.get(key)  # возвращаем то, что у нас получается по этому ключу


# Передаём значение переменной с кодом экземпляру бота
token = get_from_env('BOT_TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    """ПОДКЛЮЧАЕМСЯ и СОЗДАЕМ базу данных users.db с таблицей Users
    ПРИВЕТСТВУЕМ пользователя и запрашиваем email"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    email TEXT NON NULL,
    name TEXT NON NULL,
    surname TEXT NON NULL,
    phone INTEGER NON NULL,
    position TEXT NON NULL,
    company TEXT NON NULL,
    sfera TEXT NON NULL,
    geography TEXT NON NULL,
    username TEXT NOT NULL ON CONFLICT REPLACE DEFAULT 0,
    user_number INTEGER NON NULL)''')
    cursor.execute('SELECT user_number FROM Users WHERE user_number = ?', (message.from_user.id,))
    user_number = cursor.fetchone()
    try:
        if user_number[0] == message.from_user.id:
            bot.send_message(message.from_user.id, 'Вы уже зарегистрированы')
    except TypeError:
        if message.from_user.username is None:
            cursor.execute('INSERT INTO Users (user_number) VALUES (?)',
                           (message.from_user.id,))
        else:
            cursor.execute('INSERT INTO Users (username, user_number) VALUES (?, ?)',
                           (message.from_user.username, message.from_user.id))

    bot.send_message(message.from_user.id, f'{message.from_user.first_name},'
                                           f' приветствуем, в нашем telegram боте!\n\nНапишите свой Email\n')
    bot.register_next_step_handler(message, get_name)
    connection.commit()
    cursor.close()
    connection.close()


def get_name(message):
    """СОХРАНЯЕМ email в БД, если введен правильно (см. функцию "check_symbol_for_email", и запрашиваем имя"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    if check_symbol_for_email(str(message.text)) is True:
        cursor.execute('UPDATE Users SET email = ? WHERE user_number = ?', (message.text, message.from_user.id))
        bot.send_message(message.from_user.id, 'Напишите свое имя')
        bot.register_next_step_handler(message, get_surname)
    else:
        bot.send_message(message.from_user.id, 'Корректно напишите свой Email')
        bot.register_next_step_handler(message, get_name)
    connection.commit()
    cursor.close()
    connection.close()


def get_surname(message):
    """СОХРАНЯЕМ имя в БД и запрашиваем фамилию"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET name = ? WHERE user_number = ?', (message.text, message.from_user.id))
    connection.commit()
    cursor.close()
    connection.close()

    bot.send_message(message.from_user.id, 'Напишите свою фамилию')
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    """СОХРАНЯЕМ фамилию в БД и запрашиваем мобильный телефон"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET surname = ? WHERE user_number = ?', (message.text, message.from_user.id))
    connection.commit()
    cursor.close()
    connection.close()

    bot.send_message(message.from_user.id, 'Напишите свой номер мобильного телефона\n\n'
                                           'Пример оформления: 8 999 888 77 66')
    bot.register_next_step_handler(message, get_position)


def get_position(message):
    """СОХРАНЯЕМ телефон в БД, если введен правильно (см. функцию "check_symbols_for_phone",
    и запрашиваем должность"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    if check_symbols_for_phone(str(message.text)) is True:
        cursor.execute('UPDATE Users SET phone = ? WHERE user_number = ?', (message.text.replace(' ', ''),
                                                                            message.from_user.id))
        bot.send_message(message.from_user.id, 'Напишите свою должность')
        bot.register_next_step_handler(message, get_company)
    else:
        bot.send_message(message.from_user.id, 'Напишите номер мобильного телефона корректно\n\n'
                                               'Пример оформления: 8 999 888 77 66')
        bot.register_next_step_handler(message, get_position)
    connection.commit()
    cursor.close()
    connection.close()


def get_company(message):
    """СОХРАНЯЕМ должность в БД и запрашиваем название компании"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET position = ? WHERE user_number = ?', (message.text, message.from_user.id))
    connection.commit()
    cursor.close()
    connection.close()

    bot.send_message(message.from_user.id, 'Напишите название своей компании')
    bot.register_next_step_handler(message, get_sfera)


def get_sfera(message):
    """СОХРАНЯЕМ название компании в БД и запрашиваем сферу деятельности (предоставляется выборка в виде кнопок)"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET company = ? WHERE user_number = ?', (message.text, message.from_user.id))
    connection.commit()
    cursor.close()
    connection.close()

    bot.send_message(message.from_user.id, 'Выберите сферу деятельности своей компании из предложенного списка',
                     parse_mode='html', reply_markup=markup_sfera)
    bot.register_next_step_handler(message, get_geography)


def get_geography(message):
    """СОХРАНЯЕМ сферу деятельности в БД и запрашиваем географию присутствия
    (предоставляется выборка из кнопок)"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET sfera = ? WHERE user_number = ?', (message.text, message.from_user.id))
    connection.commit()
    cursor.close()
    connection.close()

    bot.send_message(message.from_user.id, 'Выберите географию присутствия компании на рынке из предложенного списка',
                     parse_mode='html', reply_markup=markup_geography)
    bot.register_next_step_handler(message, final)


def final(message):
    """СОХРАНЯЕМ географию присутствия в БД и благодарим за регистрацию
    При вводе любого текста или команд пользователем бот будет ТОЛЬКО отвечать, что пользователь зарегистрирован
    !!! Исключение сотрудники "Флавита" !!!"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET geography = ? WHERE user_number = ?', (message.text, message.from_user.id))
    connection.commit()
    cursor.close()
    connection.close()
    bot.send_message(message.from_user.id, 'Вы зарегистрированы! Благодарим за участие в нашем вебинаре!',
                     reply_markup=None)
    set_lead(message.from_user.id)  # Отправка данных пользователя в SendSay (см. функцию "set_lead")


@bot.message_handler(commands=['mailing'])
def mailing(message):
    """Команда для сотрудников "Флавита". Скрипт отвечает за рассылку сообщений всем пользователям из БД"""
    if message.from_user.username == 'dandrozdov2129' or message.from_user.username == 'username Нины' \
            or message.from_user.username == 'username Миланы' or message.from_user.username == 'username Саши':
        bot.send_message(message.from_user.id, 'В рассылке будет фотография?')
        bot.register_next_step_handler(message, response_handler)
    else:
        bot.send_message(message.from_user.id, 'Вы уже зарегистрированы')


def response_handler(message):
    """Уточнение, рассылка будет с фотографией или без"""
    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, 'Напиши текст для рассылки')
        bot.register_next_step_handler(message, get_text)
    elif message.text == 'нет':
        bot.send_message(message.from_user.id, 'Напиши текст для рассылки, и я ее сразу запущу')
        bot.register_next_step_handler(message, mailing_without_photo)
    else:
        bot.send_message(message.from_user.id, 'В рассылке будет фотография?')
        bot.register_next_step_handler(message, response_handler)


def get_text(message):
    """Получение текста для рассылки с фотографией"""
    global mailing_text
    mailing_text = message.text
    bot.send_message(message.from_user.id, 'Пришли фотографию для рассылки')
    bot.register_next_step_handler(message, mailing_with_photo)


def mailing_with_photo(message):
    """Отправка рассылки с фотографией"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user_number FROM Users')
    user_numbers = cursor.fetchall()
    raw = message.photo[2].file_id
    name = raw + '.jpg'
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)
    for number in filtered(user_numbers):
        try:
            img = open(name, 'rb')
            bot.send_photo(number, img, caption=mailing_text)
            img.close()
        except Exception:
            continue
    bot.send_message(message.from_user.id, 'Рассылка отправлена!')
    os.remove(name)
    connection.commit()
    cursor.close()
    connection.close()


def mailing_without_photo(message):
    """Отправка рассылки без фотографии"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user_number FROM Users')
    user_numbers = cursor.fetchall()
    for number in filtered(user_numbers):
        try:
            bot.send_message(number, message.text)
        except Exception:
            continue
    bot.send_message(message.from_user.id, 'Рассылка отправлена!')
    connection.commit()
    cursor.close()
    connection.close()


@bot.message_handler(content_types=['text'])
def repeat_registration(message):
    """Обработчик спама от пользователя"""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user_number FROM Users WHERE user_number = ?', (message.from_user.id,))
    user_number = cursor.fetchone()
    try:
        if user_number[0] == message.from_user.id:
            bot.send_message(message.from_user.id, 'Вы уже зарегистрированы')
    except TypeError:
        bot.send_message(message.from_user.id, 'Для начала регистрации введите "/start"')

    connection.commit()
    cursor.close()
    connection.close()


# бесконечное выполнение кода
bot.polling(none_stop=True)
