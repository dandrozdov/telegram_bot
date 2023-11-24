def filtered(user_numbers):
    filtered_list = []
    """Возвращает очищенный список после запроса (используется для рассылки сообщений)"""
    for i in range(0, len(user_numbers)):
        filtered_list.append(user_numbers[i][0])
    return filtered_list
