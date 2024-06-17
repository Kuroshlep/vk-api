import requests
from urllib.parse import urlencode

# Параметры вашего приложения VK
client_id = '51952311'
client_secret = '7ynvFvZFKFCmDjyVBw8k'
redirect_uri = 'https://example.com/callback'  # Настройте в своем приложении
scope = 'messages'  # Здесь можете указать необходимые права доступа, например, messages

# Шаг 1: Получение ссылки для авторизации
def get_auth_url():
    auth_params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'response_type': 'code'
    }
    url = 'https://oauth.vk.com/authorize?' + urlencode(auth_params)
    return url

# Шаг 2: Получение кода авторизации от пользователя
def get_auth_code(auth_url):
    print(f'Пожалуйста, перейдите по следующей ссылке и предоставьте доступ:')
    print(auth_url)
    code = input('Введите код авторизации из URL: ')
    return code

# Шаг 3: Получение access_token
def get_access_token(auth_code):
    token_params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': auth_code
    }
    token_url = 'https://oauth.vk.com/access_token?' + urlencode(token_params)
    response = requests.get(token_url)
    data = response.json()
    if 'access_token' in data:
        return data['access_token']
    else:
        print('Не удалось получить access_token.')
        return None

# Шаг 4: Использование access_token для выполнения запросов к VK API
def main():
    auth_url = get_auth_url()
    auth_code = get_auth_code(auth_url)
    access_token = get_access_token(auth_code)

    if access_token:
        # Пример использования access_token для выполнения запроса к VK API
        url = 'https://api.vk.com/method/newsfeed.search'
        params = {
            'q': 'https://vk.me/join/',
            'access_token': access_token,
            'v': '5.131',
            'count': 200
        }
        response = requests.get(url, params=params)
        data = response.json()

        if 'response' in data:
            news_items = data['response']['items']
            for item in news_items:
                print(item)
        else:
            print('Ошибка при получении данных:', data)
    else:
        print('Не удалось получить access_token.')

if __name__ == '__main__':
    main()
