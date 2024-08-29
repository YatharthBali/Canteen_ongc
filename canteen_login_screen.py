from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import random
import string

class CanteenLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(CanteenLoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        # Title Label
        title_label = Label(text='Canteen Login', font_size=32, bold=True, color=(0.2, 0.6, 0.8, 1))
        self.layout.add_widget(title_label)

        # Username input
        self.username = TextInput(hint_text='Username', font_size=18, multiline=False, size_hint_y=None, height=50)
        self.layout.add_widget(self.username)

        # Password input
        self.password = TextInput(hint_text='Password', password=True, font_size=18, multiline=False, size_hint_y=None, height=50)
        self.layout.add_widget(self.password)

        # CAPTCHA Label and Input
        self.captcha_text = self.generate_captcha()
        captcha_label = Label(text=f'CAPTCHA: {self.captcha_text}', font_size=18, color=(0.8, 0.2, 0.2, 1))
        self.layout.add_widget(captcha_label)

        self.captcha = TextInput(hint_text='Enter CAPTCHA', font_size=18, multiline=False, size_hint_y=None, height=50)
        self.layout.add_widget(self.captcha)

        # Login button
        login_button = Button(text='Login', font_size=20, background_color=(0.1, 0.6, 0.8, 1), size_hint_y=None, height=50)
        login_button.bind(on_press=self.validate_login)
        self.layout.add_widget(login_button)

        # Add layout to screen
        self.add_widget(self.layout)

    def generate_captcha(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def validate_login(self, instance):
        username = self.username.text
        password = self.password.text
        captcha = self.captcha.text

        if captcha == self.captcha_text:
            if username == 'canteen' and password == 'password':  # Replace with actual credentials
                self.manager.current = 'canteen_order_history'
            else:
                self.show_error("Invalid username or password.")
        else:
            self.show_error("Invalid CAPTCHA.")

    def show_error(self, message):
        content = BoxLayout(orientation='vertical', padding=20)
        content.add_widget(Label(text=message, font_size=18, color=(0.8, 0.2, 0.2, 1)))
        popup = Popup(title="Error", content=content, size_hint=(0.6, 0.4))
        popup.open()
