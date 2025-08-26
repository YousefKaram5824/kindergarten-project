import datetime
import flet as ft
# Removed MaterialState import

# Local imports
from auth_ui import set_show_main_system_callback, show_login_page
from database import db
from financial_ui import create_financial_tab
from inventory_ui import create_inventory_tab
from kindergarten_management import auth_manager, FinancialRecord, InventoryItem
from reports_ui import create_reports_tab
from student_ui import create_student_registration_tab

# Initialize default admin user
auth_manager.initialize_default_admin()

def show_main_system(page: ft.Page, current_user):
    """Show the main system after successful login"""
    # Clear login page
    page.clean()
    
    # Check if current_user is valid before accessing username
    if current_user:
        page.title = f"نظام إدارة رياض الأطفال - {current_user.username}"
    else:
        page.title = "نظام إدارة رياض الأطفال - غير مسجل الدخول"
    
    # Data storage
    financial_records = []
    inventory_items = []

    # Create tabs for different sections in Arabic
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="تسجيل الطلاب"),
            ft.Tab(text="الإدارة المالية"),
            ft.Tab(text="إدارة المخزون"),
            ft.Tab(text="التقارير")
        ],
        expand=1,
    )

    # Update tabs content
    tabs.tabs[0].content = create_student_registration_tab(page)
    tabs.tabs[1].content = create_financial_tab(page)
    tabs.tabs[2].content = create_inventory_tab(page)
    tabs.tabs[3].content = create_reports_tab(page, financial_records, inventory_items)

    # Back button for returning to login
    back_to_login_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_size=24,
        tooltip="العودة إلى تسجيل الدخول",
        on_click=lambda e: back_to_login(page)
    )
    
    # Main layout in Arabic
    page.add(back_to_login_button)
    page.add(
        ft.Text("نظام إدارة رياض الأطفال", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
        ft.Divider(),
        tabs
    )

def back_to_login(page: ft.Page):
    """Return to login page"""
    page.clean()
    show_login_page(page)

def main(page: ft.Page):
    # Configure page settings for Arabic RTL
    page.bgcolor = "#E3DCCC"  # Set background color
    page.title = "نظام إدارة رياض الأطفال - تسجيل الدخول"
    page.window.icon = "Y:\\kindengarten\\logo.ico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.rtl = True  # Enable Right-to-Left layout
    page.window.maximized = True
    
    # Custom scrollbar styling
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color=ft.Colors.GREY_300,
            track_visibility=True,
            track_border_color=ft.Colors.GREY_600,
            thumb_color=ft.Colors.BLUE_700,
            thumb_visibility=True,
            thickness=12,
            radius=6,
            main_axis_margin=2,
            cross_axis_margin=2,
        )
    )
    
    # Set the callback for showing main system
    set_show_main_system_callback(show_main_system)
    
    # Show login page initially
    show_login_page(page)

if __name__ == "__main__":
    ft.app(target=main)
