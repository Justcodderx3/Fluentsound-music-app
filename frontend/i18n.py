from kivymd.app import MDApp

TRANSLATIONS = {
    'en': {
        "username_hint": "Username",
        "password_hint": "Password",
        "Login_button": "Sign in",
        "error_user_not_found": "User not found",
        "error_incorrect_password": "Incorrect password",
        "error_server_unavailable": "Server unavailable",
        "error_unknown": "Unknown error"
    },
    'ru': {
           "username_hint": "Никнейм",
           "password_hint": "Пароль",
           "Login_button": "Вход",
            "error_user_not_found": "Пользователь не найден",
            "error_incorrect_password": "Неверный пароль",
            "error_server_unavailable": "Сервер недоступен",
            "error_unknown": "Неизвестная ошибка"
           }
}



def _(key: str) -> str:
    app = MDApp.get_running_app()
    translate = TRANSLATIONS[app.current_language]
    if key not in translate:
        return key
    return translate[key]
