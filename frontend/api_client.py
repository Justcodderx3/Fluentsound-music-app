import requests

BASE_URL = "http://127.0.0.1:8000"


def login(username: str, password: str):
    form_data = {'username': username, "password": password}
    try:
        response = requests.post(f"{BASE_URL}/users/login", data=form_data, timeout=3)
        if response.status_code != 200:
            detail = response.json().get('detail', '')
            if detail == "User not found":
                return False, "error_user_not_found"
            elif detail == "Incorrect password":
                return False, "error_incorrect_password"
            else:
                return False, "unknown_error"
        return True, response.json()
    except(requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False, "error_server_unavailable"
