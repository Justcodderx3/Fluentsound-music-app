from kivymd.app import MDApp
from kivy.app import App
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from api_client import login
from i18n import _


class LoginScreen(Screen, ):
    gradient_texture = ObjectProperty(None)

    LIGHT_GRADIENT = [160, 32, 240, 255, 0, 255, 255, 255]
    DARK_GRADIENT = [0, 255, 255, 255, 160, 32, 240, 255]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_texture(LoginScreen.DARK_GRADIENT)

    def process_login(self, username, password):
        success, result = login(username, password)
        if success is True:
            app = MDApp.get_running_app()
            app.save_token(result['access_token'])
            self.ids.error_label.text = ''
        else:
            self.ids.error_label.text = result

    def translate_texts(self):
        self.ids.username_field.hint_text = _('username_hint')
        self.ids.password_field.hint_text = _("password_hint")
        self.ids.Login_button.text = _("Login_button")

    def open_language_menu(self):
        app = MDApp.get_running_app()
        color = self.get_theme_hex_color()
        menu_items = [
            {
                "text": "English",
                "text_color": color if app.current_language == "en" else app.theme_cls.text_color,
                "on_release": lambda: self.set_language("en"),
            },
            {
                "text": "Русский",
                "text_color": color if app.current_language == "ru" else app.theme_cls.text_color,
                "on_release": lambda: self.set_language("ru"),
            }
        ]
        self.menu = MDDropdownMenu(caller=self.ids.language_button, items=menu_items)
        self.menu.open()

    def set_language(self, lang_code):
        app = MDApp.get_running_app()
        app.current_language = lang_code
        self.translate_texts()
        self.menu.dismiss()

    def create_texture(self, gradient_mode):
        pixels = bytearray(gradient_mode)
        texture = Texture.create(size=(1, 2), colorfmt='rgba')
        texture.blit_buffer(pixels, colorfmt='rgba', bufferfmt='ubyte')
        texture.mag_filter = 'linear'
        self.gradient_texture = texture

    def update_gradient(self, is_dark: bool):
        if is_dark is True:
            LoginScreen.create_texture(self, LoginScreen.DARK_GRADIENT)
        else:
            LoginScreen.create_texture(self, LoginScreen.LIGHT_GRADIENT)

    def get_theme_hex_color(self):
        app = MDApp.get_running_app()
        if app.is_dark:
            return "A020F0"
        else:
            return "00FFFF"


class MainApp(MDApp):
    is_dark = True
    access_token = None
    current_language = "en"

    def save_token(self, token):
        self.access_token = token

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Purple'
        sm = ScreenManager()
        login_screen = LoginScreen(name='login')
        sm.add_widget(login_screen)
        return sm

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        if self.is_dark is True:
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.primary_palette = 'Purple'
        else:
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.primary_palette = 'Cyan'
        login_screen = self.root.get_screen('login')
        login_screen.update_gradient(self.is_dark)


if __name__ == '__main__':
    MainApp().run()
    app = App.get_running_app()
