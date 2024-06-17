import json
from datetime import datetime
import vk_api

# Конфигурационные данные
# Ваш access token, полученный на странице разработчиков ВКонтакте
access_token = 'vk1.a.yKYq39-iAUSXWspBsAk4M9XQYJuxXXzFoPygyVlc_WQDy-oMe-L8rv3uo_08kRHl-Kd2zVaYC4-7ykc4IJo5azVRrn6xpoZ3CLtyWesycvy-ofzuj-XbtAWuCNdM0uEeJPcG5pH5bxVkr-o1jkQUzBxPzBLjtuopkJG0fe_Z_23jgsku26ellnEK8Cg5_07G4Yphf9bjbu07YKXGHT_M-Q'
# Инициализируем сессию API
vk_session = vk_api.VkApi(token=access_token)
# Получаем объект API
vk = vk_session.get_api()
# Строка, которую нужно найти в записях
search_string = 'https://vk.me/join/'

def get_news(search_string: str, count: int) -> dict:
    """
    Функция для получения записей с требующимся значением подстроки

    :param search_string: переменная для задания поисковой строки
    :param count: количество записей для запроса (max=200)
    :return: словарь с отформатированными данными
    """
    try:
        # Получаем новости из новостной ленты
        response = vk.newsfeed.search(q=search_string, count=count)  # Ищем первые count записей

        return response['items']

    except vk_api.exceptions.ApiError as e:
        print(f"Ошибка API: {e}")
        return None

    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def extract_first_link(post_text: str) -> str:
    """
    Функция для вычленения пригласительной ссылки из поста

    :param post_text: текст поста, в котором мы ищем ссылку
    :return: возвращает ссылку на приглашение в чат
    """
    words = post_text.split()
    for word in words:
        if word.startswith('https://vk.me/join/'):
            return word
    return None

def get_chat_info_by_link(link: str) -> dict:
    """
    Функция для получения подробной информации о беседе

    :param link: ссылка-приглашение в беседу
    :return: словарь с данными о беседе
    """
    try:
        # Получаем информацию о беседе по ссылке-приглашению
        chat_info = vk.messages.getChatPreview(link=link)

        # Возвращаем объект с информацией о беседе
        return chat_info

    except vk_api.exceptions.ApiError as e:
        print(f"Ошибка API: {e}")
        return None

    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def format_data(data: dict) -> dict:
    """
    Функция для форматирования данных

    :param data: словарь с необработанными данными
    :return: отформатированный список словарей
    """
    i = 0
    formatted_news = []
    for item in data:
        print(f'{item["text"]}\n\n https://vk.com/wall{abs(item["owner_id"])}_{item["id"]} \n{"-"*50}')
        # Преобразование даты в читаемый формат
        readable_date = datetime.fromtimestamp(item['date']).strftime('%Y-%m-%d %H:%M:%S')
        link = extract_first_link(item['text'])
        if link:
            chat_info = get_chat_info_by_link(link)
            formatted_news.append({
                'date': readable_date,
                'link': link,
                'chat_info': chat_info
            })
            i += 1

    print(formatted_news)
    return formatted_news

result = format_data(get_news(search_string, 20))

with open('news_results.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

