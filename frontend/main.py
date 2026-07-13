from kivymd.app import MDApp
from kivy.app import App
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from api_client import login


class LoginScreen(Screen):
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


class MainApp(MDApp):
    is_dark = True
    access_token = None

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
