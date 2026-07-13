import requests

BASE_URL = "http://127.0.0.1:8000"


def login(username: str, password: str):
    form_data = {'username': username, "password": password}
    response = requests.post(f"{BASE_URL}/users/login", data=form_data)
    if response.status_code == 200:
        return True, response.json()
    else:
        error_message = response.json().get('detail', 'Unknown error')
        return False, error_message
