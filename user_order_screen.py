from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import sqlite3
import datetime
import openpyxl
from db_utils import place_order

class UserOrderScreen(Screen):
    def __init__(self, **kwargs):
        super(UserOrderScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title Label
        title_label = Label(text='Order Your Items', font_size=32, bold=True, color=(0.2, 0.6, 0.8, 1))
        self.layout.add_widget(title_label)

        # Grid layout for items
        self.items_layout = GridLayout(cols=2, spacing=20, size_hint_y=None)
        self.items_layout.bind(minimum_height=self.items_layout.setter('height'))

        # Example items with images and quantity buttons
        items = [
            {"name": "Samosa", "image": "images/samosa.jfif", "price": 10},
            {"name": "Dosa", "image": "images/dosa.jfif", "price": 20},
            {"name": "Coffee", "image": "images/coffee.jfif", "price": 30},
            {"name": "Tea", "image": "images/tea.jfif", "price": 15}
        ]

        self.item_buttons = {}

        for item in items:
            item_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=150, padding=10, spacing=10)
            item_image = Image(source=item["image"], size_hint_x=0.4)
            item_label = Label(text=f'{item["name"]}\nPrice: ₹{item["price"]}', font_size=20, halign='left', size_hint_x=0.6)

            # Box layout for quantity controls
            item_buttons_box = BoxLayout(orientation='horizontal', size_hint_x=0.4, spacing=5)
            quantity_label = Label(text='0', font_size=20, size_hint_x=0.3, halign='center')
            self.item_buttons[item["name"]] = {'quantity': quantity_label, 'price': item["price"], 'quantity_val': 0}

            minus_button = Button(text='-', font_size=20, size_hint_x=0.3)
            minus_button.bind(on_press=lambda btn, item=item: self.update_quantity(item, -1))
            plus_button = Button(text='+', font_size=20, size_hint_x=0.3)
            plus_button.bind(on_press=lambda btn, item=item: self.update_quantity(item, 1))

            item_buttons_box.add_widget(minus_button)
            item_buttons_box.add_widget(quantity_label)
            item_buttons_box.add_widget(plus_button)

            item_box.add_widget(item_image)
            item_box.add_widget(item_label)
            item_box.add_widget(item_buttons_box)

            self.items_layout.add_widget(item_box)

        self.layout.add_widget(self.items_layout)

        # User Details Label
        self.user_details_label = Label(text='Loading user details...', font_size=20, size_hint_y=None, height=100)
        self.layout.add_widget(self.user_details_label)

        # Place Order Button
        place_order_button = Button(text='Place Order', font_size=18, background_color=(0.2, 0.8, 0.2, 1), size_hint_y=None, height=50)
        place_order_button.bind(on_press=self.place_order)
        self.layout.add_widget(place_order_button)

        # Excel Export Button
        excel_export_button = Button(text='Export to Excel', font_size=18, background_color=(0.2, 0.6, 0.8, 1), size_hint_y=None, height=50)
        excel_export_button.bind(on_press=self.export_to_excel)
        self.layout.add_widget(excel_export_button)

        # Logout Button
        logout_button = Button(text='Logout', font_size=18, background_color=(0.8, 0.2, 0.2, 1), size_hint_y=None, height=50)
        logout_button.bind(on_press=self.logout)
        self.layout.add_widget(logout_button)

        self.add_widget(self.layout)

    def update_user_details(self, user_id):
        self.current_user_id = user_id
        conn = sqlite3.connect('user_db.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name, floor, seat_no, contact_no FROM users WHERE user_id=?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.user_details_label.text = f'Name: {user[0]}\nSeat No: {user[2]}\nFloor: {user[1]}\nContact No: {user[3]}'
        else:
            self.user_details_label.text = 'User not found'

    def update_quantity(self, item, delta):
        item_name = item["name"]
        if item_name in self.item_buttons:
            new_quantity = self.item_buttons[item_name]['quantity_val'] + delta
            if new_quantity < 0:
                new_quantity = 0
            self.item_buttons[item_name]['quantity_val'] = new_quantity
            self.item_buttons[item_name]['quantity'].text = str(new_quantity)

    def place_order(self, instance):
        order_details = []
        total_cost = 0

        for item_name, item_info in self.item_buttons.items():
            quantity = item_info['quantity_val']
            if quantity > 0:
                item_total_cost = quantity * item_info['price']
                order_details.append({
                    'item': item_name,
                    'quantity': quantity,
                    'price': item_info['price']
                })
                total_cost += item_total_cost

        if not order_details:
            content = BoxLayout(orientation='vertical', padding=20)
            content.add_widget(Label(text="No items selected.", font_size=18))
            popup = Popup(title="Order Error", content=content, size_hint=(0.6, 0.4))
            popup.open()
            return

        place_order(self.current_user_id, order_details)  # Ensure this matches the function signature

        content = BoxLayout(orientation='vertical', padding=20)
        content.add_widget(Label(text="Order placed successfully!", font_size=18))
        popup = Popup(title="Order Placed", content=content, size_hint=(0.6, 0.4))
        popup.open()

    def export_to_excel(self, instance):
        conn = sqlite3.connect('user_db.sqlite')
        cursor = conn.cursor()

        # Retrieve user details
        cursor.execute("SELECT name, floor, seat_no, contact_no FROM users WHERE user_id=?", (self.current_user_id,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            content = BoxLayout(orientation='vertical', padding=20)
            content.add_widget(Label(text="User not found for export.", font_size=18))
            popup = Popup(title="Export Error", content=content, size_hint=(0.6, 0.4))
            popup.open()
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Order Details"

        # Define headers
        headers = ["Name", "Floor", "Seat No", "Contact No", "Item", "Quantity", "Price", "Total Cost", "Date", "Time"]
        ws.append(headers)

        # Sample data for demonstration
        for item_name, item_info in self.item_buttons.items():
            quantity = item_info['quantity_val']
            if quantity > 0:
                total_cost = quantity * item_info['price']
                ws.append([
                    user[0], user[1], user[2], user[3], item_name, quantity, item_info['price'], total_cost,
                    datetime.datetime.now().strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%H:%M:%S")
                ])

        # Save file
        filename = f"user_{self.current_user_id}_order_details.xlsx"
        wb.save(filename)

        content = BoxLayout(orientation='vertical', padding=20)
        content.add_widget(Label(text=f"Exported to Excel successfully as {filename}!", font_size=18))
        popup = Popup(title="Export Successful", content=content, size_hint=(0.6, 0.4))
        popup.open()

    def logout(self, instance):
        self.manager.current = 'main'
