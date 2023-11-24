# -*- coding: utf-8 -*-
def check_symbol_for_email(message):
    """�������� �� ������� ������� "@" """
    test_symbol = message.find('@') != -1
    if test_symbol is True:
        return True
    else:
        return False


def check_symbols_for_phone(text):
    """�������� �� ������ ������, ��� ������� - �����, ����� ������ - 11 �������� """
    message = text.replace(' ', '')
    test_one = message[0:1]  # �������� ������� �������
    test_two = message.isdigit()  # ��������, ��� �� ������� �����
    test_three = len(message)  # �������� ����� ���������
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
