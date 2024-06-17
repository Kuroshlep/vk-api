import requests
import json
import time
from datetime import datetime
import re

start_time = time.time()
# Ваш access_token
access_token = '94b458a994b458a994b458a92d97ace21e994b494b458a9f2c447edd8d8b5ca918302c2'
service_token = 'NPi1sY2SELAfuVTcdiqj'
# Ключевое слово для поиска
query = 'https://vk.me/join/'

def get_news(query, access_token):
    url = 'https://api.vk.com/method/newsfeed.search'
    params = {
        'q': query,
        'access_token': access_token,
        'v': '5.131',  # версия API
        'count': 200  # количество возвращаемых результатов
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'response' in data:
        return data['response']['items']
    else:
        print('Error:', data)
        return []

# Функция для извлечения первой ссылки из текста
def extract_first_link(text):
    words = text.split()
    for word in words:
        if word.startswith('https://vk.me/join/'):
            return word
    return None

def get_conversation_info_by_link(chat_link, token):
    # Выполняем запрос к VK API
    url = 'https://api.vk.com/method/messages.getChatPreview'
    params = {
        'access_token': token,
        'v': '5.131',  # Версия API
        'link': chat_link  # Пригласительная ссылка
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'response' in data:
        preview = data['response']
        print(f"Название беседы: {preview['preview']['title']}")
        print(f"Тип беседы: {preview['preview']['type']}")
        print(f"Количество участников: {preview['preview']['members_count']}")
        print(f"Ссылка на беседу: {chat_link}")
        return preview

    else:
        print(f"Ошибка при получении информации о беседе: {data.get('error', 'No error details')}")
        return None

# Получение новостей
news_items = get_news(query, access_token)

end_time = time.time()

execution_time = end_time - start_time
print(f'Время работы: {execution_time}')

# Обработка и вывод новостей
formatted_news = []
for item in news_items:
    # Преобразование даты в читаемый формат
    readable_date = datetime.fromtimestamp(item['date']).strftime('%Y-%m-%d %H:%M:%S')
    link = extract_first_link(item['text'])

    if link:
        group_data = get_conversation_info_by_link(link, access_token)
        formatted_news.append({
            'date': readable_date,
            'link': link,
            'group_data': group_data
        })
        print(f"Date: {readable_date}")
        print(f"Link: {link}")
        print(f"Group Data: {group_data}")
        print('-' * 20)
    else:
        print(f"Не удалось извлечь ссылку из текста новости:\n{item['text']}")
        print('-' * 20)

# Сохранение в файл
with open('news_results.json', 'w', encoding='utf-8') as f:
    json.dump(formatted_news, f, ensure_ascii=False, indent=4)
