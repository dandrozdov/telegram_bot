# -*- coding: cp1251 -*-
def check_symbol_for_email(message):
    """Проверка на наличие символа "@" """
    test_symbol = message.find('@') != -1
    if test_symbol is True:
        return True
    else:
        return False


def check_symbols_for_phone(text):
    """Проверка на первый символ, все символы - цифры, длина номера - 11 символов """
    message = text.replace(' ', '')
    test_one = message[0:1]  # Проверка первого символа
    test_two = message.isdigit()  # Проверка, все ли символы цифры
    test_three = len(message)  # Проверка длины сообщения
    if test_one == '8':
        if test_two is True:
            if test_three == 11:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
