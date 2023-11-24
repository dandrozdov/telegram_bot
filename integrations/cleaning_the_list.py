# -*- coding: cp1251 -*-
def filtered(user_numbers):
    filtered_list = []
    """���������� ��������� ������ ����� ������� (������������ ��� �������� ���������)"""
    for i in range(0, len(user_numbers)):
        filtered_list.append(user_numbers[i][0])
    return filtered_list
