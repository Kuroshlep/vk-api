import vk_api


# Функция для инициализации сессии vk_api с использованием сервисного токена
def vk_session_with_service_token(service_token):
    vk_session = vk_api.VkApi(token=service_token)
    return vk_session


# Функция для поиска записей по ключевому слову и извлечения информации о пригласительных ссылках
def search_posts(vk_session, query):
    vk = vk_session.get_api()
    try:
        response = vk.newsfeed.search(q=query, count=100,
                                      extended=1)  # Увеличиваем count для получения большего количества записей
        items = response['items']

        # Обработка результатов поиска
        for item in items:
            text = item.get('text', '')
            attachments = item.get('attachments', [])

            # Проверяем текст записи на наличие пригласительных ссылок
            if 'link' in attachments:
                link = attachments['link']
                if 'button_title' in link and 'url' in link:
                    if 'приглашение' in link[
                        'button_title'].lower():  # Можно использовать другие ключевые слова или условия
                        invite_url = link['url']
                        print(f"Найдена пригласительная ссылка: {invite_url}")

            # Также можно проверять текст записи на наличие ссылок, если они указаны в тексте
            if 'http' in text:
                # Например, можно использовать регулярные выражения для поиска ссылок
                pass

    except vk_api.ApiError as api_error:
        print(f"Ошибка API ВКонтакте: {api_error}")


# Ваш сервисный токен от ВКонтакте (полученный для мини-приложения)
service_token = '448955924489559244895592af4791eae9444894489559222f968bb96dd30318d5be422'

# Создаем сессию vk_api с использованием сервисного токена
vk_session = vk_session_with_service_token(service_token)

# Выполняем поиск записей и извлекаем пригласительные ссылки
search_posts(vk_session, 'приглашение')  # Здесь 'приглашение' - ваше ключевое слово для поиска записей
