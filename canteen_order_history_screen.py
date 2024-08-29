from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
import openpyxl
import datetime

# Sample order history data
orders = [
    {"user_id": "101", "name": "Parvesh", "floor": "2", "seat_no": "23", "contact_no": "9878985564", "item": "Dosa", "quantity": 3, "status": "Pending", "timestamp": "2024-08-20 14:00:00"},
    {"user_id": "102", "name": "Kartik", "floor": "5", "seat_no": "44", "contact_no": "8656554456", "item": "Dosa", "quantity": 2, "status": "Pending", "timestamp": "2024-08-21 10:00:00"},
    {"user_id": "103", "name": "Sumit", "floor": "1", "seat_no": "31", "contact_no": "5567985675", "item": "Samosa", "quantity": 1, "status": "Pending", "timestamp": "2024-08-21 11:00:00"}
]

class CanteenOrderHistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(CanteenOrderHistoryScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Title Label
        title_label = Label(text='Order History', font_size=32, bold=True, color=(0.2, 0.6, 0.2, 1))
        self.layout.add_widget(title_label)

        # Logout Button
        logout_button = Button(text='Logout', font_size=18, background_color=(0.8, 0.2, 0.2, 1), size_hint_y=None, height=50)
        logout_button.bind(on_press=self.logout)
        self.layout.add_widget(logout_button)

        # Order List in Tabular Format
        self.order_list = GridLayout(cols=9, spacing=10, size_hint_y=None)
        self.order_list.bind(minimum_height=self.order_list.setter('height'))
        self.update_order_list()

        # Export to Excel button
        export_button = Button(text='Export to Excel', font_size=18, background_color=(0.1, 0.6, 0.8, 1), size_hint_y=None, height=50)
        export_button.bind(on_press=self.export_to_excel)
        
        self.layout.add_widget(self.order_list)
        self.layout.add_widget(export_button)

        self.add_widget(self.layout)

    def update_order_list(self):
        self.order_list.clear_widgets()
        
        # Table Headers
        headers = ['Name', 'Floor', 'Seat No', 'Contact No', 'Item', 'Quantity', 'Status', 'Timestamp', 'Action']
        for header in headers:
            label = Label(text=header, bold=True, size_hint_y=None, height=40, color=(0.2, 0.6, 0.2, 1))
            self.order_list.add_widget(label)

        # Order Data
        for order in orders:
            order_info = [
                order['name'], order['floor'], order['seat_no'], order['contact_no'],
                order['item'], str(order['quantity']), order['status'], order['timestamp']
            ]
            for info in order_info:
                label = Label(text=info, size_hint_y=None, height=40, font_size=16)
                self.order_list.add_widget(label)

            mark_delivered_button = Button(text='Mark as Delivered', font_size=16, background_color=(0.2, 0.8, 0.2, 1), size_hint_y=None, height=40)
            mark_delivered_button.bind(on_press=lambda btn, order=order: self.mark_as_delivered(order))
            self.order_list.add_widget(mark_delivered_button)
    
    def mark_as_delivered(self, order):
        order['status'] = 'Delivered'
        self.update_order_list()
        self.export_to_excel()

    def export_to_excel(self, instance=None):
        filename = f"order_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Order History"
        sheet.append(["User ID", "Name", "Floor", "Seat No", "Contact No", "Item", "Quantity", "Status", "Timestamp"])
        
        for order in orders:
            sheet.append([
                order["user_id"], order["name"], order["floor"], order["seat_no"], order["contact_no"],
                order["item"], order["quantity"], order["status"], order["timestamp"]
            ])
        
        workbook.save(filename)
        # Notify the user that the file has been saved
        content = BoxLayout(orientation='vertical', padding=20)
        content.add_widget(Label(text=f"Excel file '{filename}' has been saved.", font_size=18, color=(0.2, 0.6, 0.2, 1)))
        popup = Popup(title="Export Successful", content=content, size_hint=(0.6, 0.4))
        popup.open()
    
    def logout(self, instance):
        self.manager.current = 'main_page'
