from kivymd.app import MDApp

TRANSLATIONS = {
    'en': {
        "username_hint": "Username",
        "password_hint": "Password",
        "Login_button": "Sign in"
    },
    'ru': {
           "username_hint": "Никнейм",
           "password_hint": "Пароль",
           "Login_button": "Вход"
           }
}



def _(key: str) -> str:
    app = MDApp.get_running_app()
    translate = TRANSLATIONS[app.current_language]
    if key not in translate:
        return key
    return translate[key]
