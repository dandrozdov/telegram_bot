import requests
import json
import sqlite3

LOGIN = 'LOGIN'
SUBLOGIN = 'SUBLOGIN'
PASSWORD = 'PASSWORD'
URl = 'https://api.sendsay.ru/general/api/v100/json/LOGIN/?='

DATA_AUTH = {'action': 'login',
             'login': LOGIN,
             'sublogin': SUBLOGIN,
             'passwd': PASSWORD}

HEADERS = {"Content-Type": "application/json",
           "accept": "application/json"}


def get_user_sfera(text):
    """������� ��� ������� � SendSay ������ �������� ����� ������������ �� �� ����� � ������������ �� �������� ����"""
    sfera = {
        '������� �������������� � �������': '1',
        '�������� non-food': '2',
        '�������������': '3',
        '�������� � ����������': '4',
        '������': '5',
    }
    if text.lower() in sfera.keys():
        return sfera[text.lower()]
    else:
        return sfera['������']


def get_user_geography(text):
    """������� ��� ������� � SendSay ������ �������� ��������� ����������� �� �� ����� � ������������
    �� �������� ����"""
    geography = {
        '�����������': '1',
        '������������': '2',
    }
    if text.lower() in geography.keys():
        return geography[text.lower()]
    else:
        return geography['������������']


def get_session():
    """������� ���������� ����� ������"""
    response = requests.post(URl, headers=HEADERS, json=DATA_AUTH)
    return json.loads(response.text)['session']


def set_user_data(token, user_id):
    """������� ���������� ������ ������������ � SendSay"""
    connection = sqlite3.connect(r'../users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE user_number = ?', (user_id,))
    user = cursor.fetchone()
    sfera = get_user_sfera(user[7])
    geography = get_user_geography(user[8])
    lead = {'action': 'member.set',
            "session": token,
            'login': LOGIN,
            'sublogin': SUBLOGIN,
            'email': user[1],
            'newbie.confirm': '0',
            'obj': {
                '-group': {'pl23930': '1'},
                'custom': {
                    'q406': user[2],
                    'q514': user[3],
                    'q132': user[4],
                    'q158': user[5],
                    'q733': user[6],
                    'q295': [str(sfera)],
                    'q923': [str(geography)],
                    'q453': ['1'],
                    'q33': ['1'],
                    'q369': ['1'],
                }
            }}
    requests.post(URl, headers=HEADERS, json=lead)


def set_lead(user_id):
    """������� ����������� ������������ � SendSay"""
    set_user_data(get_session(), user_id)
