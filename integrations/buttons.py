# -*- coding: cp1251 -*-
from telebot import types  # ������ ������

# ������ ��� ������ �����
sfera_buttons = ['������� �������������� � �������', '�������� non-food', '�������������', '�������� � ����������',
                 '������']
# ������ � �������� ��� ��������� ����� ������������
markup_sfera = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
markup_sfera.add(sfera_buttons[0], sfera_buttons[1], sfera_buttons[2], sfera_buttons[3], sfera_buttons[4])

# ������ ��� ������ ���������
geography_buttons = ['������������', '�����������']
# ������ � �������� ��� ��������� ��������� ��������
markup_geography = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_geography.row(geography_buttons[0], geography_buttons[1])
