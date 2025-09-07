import flet as ft
from database import get_db
from view.Authentication.auth_ui import set_show_main_system_callback, show_login_page
from view.dashboard_ui import show_main_system
from kindergarten_management import auth_manager


# Initialize default admin user
def init_admin():
    db = next(get_db())
    auth_manager.initialize_default_admin(db)
    db.close()


init_admin()


def main(page: ft.Page):
    page.title = "نظام إدارة رياض الأطفال - تسجيل الدخول"
    page.bgcolor = "#E3DCCC"
    page.window.icon = "logo.ico"
    page.window.maximized = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.rtl = True

    # Custom scrollbar
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

    # Callback للانتقال للنظام الرئيسي بعد تسجيل الدخول
    set_show_main_system_callback(show_main_system)
    show_login_page(page)


if __name__ == "__main__":
    ft.app(target=main)
