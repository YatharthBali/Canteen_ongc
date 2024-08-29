from kivy.app import App
import sys
import argparse
from kivy.uix.screenmanager import ScreenManager
from user_login_screen import UserLoginScreen
from user_order_screen import UserOrderScreen
from canteen_login_screen import CanteenLoginScreen
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from canteen_order_history_screen import CanteenOrderHistoryScreen



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        # Adding a title label
        title = Label(text='Canteen Ordering System', font_size=32, bold=True, color=(0.2, 0.6, 0.8, 1))
        self.layout.add_widget(title)
        parser = argparse.ArgumentParser(description="Kivy Application")
        parser.add_argument("--host", type=str, default="0.0.0.0", help="Host IP")
        parser.add_argument("--port", type=int, default=5678, help="Port number")    
        args = parser.parse_args()
        print(f"Starting server on {args.host}:{args.port}")

        # Adding a background image (optional, replace with your image path)
        # bg_image = Image(source='background_image.png', size_hint=(1, 0.6))
        # self.layout.add_widget(bg_image)

        # Buttons for User and Canteen Login
        user_login = Button(text='User Login', font_size=24, size_hint=(1, 0.3), background_color=(0.1, 0.6, 0.8, 1))
        user_login.bind(on_press=self.go_to_user_login)
        
        canteen_login = Button(text='Canteen Login', font_size=24, size_hint=(1, 0.3), background_color=(0.8, 0.4, 0.2, 1))
        canteen_login.bind(on_press=self.go_to_canteen_login)
        
        self.layout.add_widget(user_login)
        self.layout.add_widget(canteen_login)
        
        self.add_widget(self.layout)
    
    def go_to_user_login(self, instance):
        self.manager.current = 'user_login'
    
    def go_to_canteen_login(self, instance):
        self.manager.current = 'canteen_login'

class CanteenApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(UserLoginScreen(name='user_login'))
        sm.add_widget(UserOrderScreen(name='user_order'))
        sm.add_widget(CanteenLoginScreen(name='canteen_login'))
        sm.add_widget(CanteenOrderHistoryScreen(name='canteen_order_history'))

        return sm

if __name__ == '__main__':
    CanteenApp().run()



 

   