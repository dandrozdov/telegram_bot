# -*- coding: cp1251 -*-
from telebot import types  # Импорт кнопок

# Кнопки для выбора сферы
sfera_buttons = ['Пищевая промышленность и общепит', 'Продукты non-food', 'Фарминдустрия', 'Компании и корпорации',
                 'Другое']
# Маркап с кнопками для получения сферы деятельности
markup_sfera = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
markup_sfera.add(sfera_buttons[0], sfera_buttons[1], sfera_buttons[2], sfera_buttons[3], sfera_buttons[4])

# Кнопки для выбора географии
geography_buttons = ['Региональное', 'Федеральное']
# Маркап с кнопками для получения географии компании
markup_geography = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_geography.row(geography_buttons[0], geography_buttons[1])
