import flet as ft

from kindergarten_management import auth_manager
from database import db_session
from view.Authentication.forgot_password_ui import show_forgot_password_dialog
from view.Authentication.create_account_ui import show_create_account_dialog


# This will be set by the main application
show_main_system_callback = None


def set_show_main_system_callback(callback):
    """Set the callback function to show the main system"""
    global show_main_system_callback
    show_main_system_callback = callback


def show_login_page(page: ft.Page):
    # Login form components
    username_field = ft.TextField(
        label="اسم المستخدم", width=300, text_align=ft.TextAlign.RIGHT
    )

    password_field = ft.TextField(
        label="كلمة المرور",
        width=300,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.RIGHT,
    )

    login_button = ft.ElevatedButton("تسجيل الدخول", width=300, height=50)

    login_error_text = ft.Text("", color=ft.Colors.RED)

    def handle_login(e):
        username = username_field.value.strip() if username_field.value else ""
        password = password_field.value.strip() if password_field.value else ""

        if not username or not password:
            login_error_text.value = "يرجى إدخال اسم المستخدم وكلمة المرور"
            page.update()
            return

        with db_session() as db:
            success, result = auth_manager.authenticate(db, username, password)
        if success:
            if show_main_system_callback:
                show_main_system_callback(page, result)
        else:
            login_error_text.value = result
            page.update()

    login_button.on_click = handle_login

    # Bind Enter key to login for both fields
    username_field.on_submit = lambda e: handle_login(e)
    password_field.on_submit = lambda e: handle_login(e)

    # Hyperlinks for additional authentication features
    forgot_password_link = ft.TextButton(
        "نسيت كلمة المرور؟", on_click=lambda e: show_forgot_password_dialog(page)
    )

    create_account_link = ft.TextButton(
        "إنشاء حساب جديد", on_click=lambda e: show_create_account_dialog(page)
    )

    # Layout for login page with RTL support
    login_page = ft.Column(
        [
            ft.Container(height=150),
            ft.Image(src="logo.jpg", width=200),
            ft.Text(
                "نظام إدارة رياض الأطفال",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
                text_align=ft.TextAlign.CENTER,
            ),
            username_field,
            password_field,
            ft.Row([login_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                [forgot_password_link, create_account_link],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            login_error_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    page.add(login_page)
