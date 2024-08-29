from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import random
from db_utils import place_order, user_login


class UserLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(UserLoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        # Title Label
        title_label = Label(text='User Login', font_size=32, bold=True, color=(0.2, 0.6, 0.8, 1))
        self.layout.add_widget(title_label)

        # User ID input
        self.user_id_input = TextInput(hint_text='Enter User ID', input_filter='int', font_size=24, size_hint=(1, 0.5), multiline=False)
        self.layout.add_widget(self.user_id_input)

        # CAPTCHA generation
        self.captcha_code = self.generate_captcha()
        self.captcha_label = Label(text=f"CAPTCHA: {self.captcha_code}", font_size=24, color=(0.8, 0.4, 0.2, 1))
        self.layout.add_widget(self.captcha_label)

        # CAPTCHA input
        self.captcha_input = TextInput(hint_text='Enter CAPTCHA', font_size=24, size_hint=(1, 0.5), multiline=False)
        self.layout.add_widget(self.captcha_input)

        # Login button
        login_button = Button(text='Login', font_size=24, size_hint=(1, 0.5), background_color=(0.1, 0.6, 0.8, 1))
        login_button.bind(on_press=self.validate_login)
        self.layout.add_widget(login_button)

        # Add layout to screen
        self.add_widget(self.layout)

    def generate_captcha(self):
        return str(random.randint(1000, 9999))  # Generates a random 4-digit number

    def validate_login(self, instance):
        user_id = self.user_id_input.text
        captcha_input = self.captcha_input.text

        if captcha_input == self.captcha_code:
            if user_id in ["101", "102", "103"]:  # Basic validation for example
                self.manager.current = 'user_order'
                user_order_screen = self.manager.get_screen('user_order')
                user_order_screen.update_user_details(user_id)
            else:
                self.show_error("Invalid User ID")
        else:
            self.show_error("Invalid CAPTCHA")

    def show_error(self, message):
        # Show an error message to the user
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        content.add_widget(Label(text=message, font_size=20, color=(1, 0, 0, 1)))
        popup = Popup(title="Error", content=content, size_hint=(0.6, 0.4))
        popup.open()
