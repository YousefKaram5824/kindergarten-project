import flet as ft

# Local imports
from kindergarten_management import auth_manager
from database import db_session


def show_create_account_dialog(page: ft.Page):
    """Show create account dialog with admin verification"""
    admin_username_field = ft.TextField(
        label="اسم المستخدم للمدير", width=300, text_align=ft.TextAlign.RIGHT
    )

    admin_password_field = ft.TextField(
        label="كلمة مرور المدير",
        width=300,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.RIGHT,
    )

    new_username_field = ft.TextField(
        label="اسم المستخدم الجديد", width=300, text_align=ft.TextAlign.RIGHT
    )

    new_password_field = ft.TextField(
        label="كلمة المرور الجديدة",
        width=300,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.RIGHT,
    )

    confirm_password_field = ft.TextField(
        label="تأكيد كلمة المرور",
        width=300,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.RIGHT,
    )

    role_dropdown = ft.Dropdown(
        label="الدور",
        width=300,
        options=[
            ft.dropdown.Option("admin", "مدير"),
            ft.dropdown.Option("user", "مستخدم"),
        ],
        value="user",
        text_align=ft.TextAlign.RIGHT,
    )

    create_button = ft.ElevatedButton("إنشاء حساب", width=300, height=50)

    cancel_button = ft.TextButton("إلغاء", width=300)
    error_text = ft.Text("", color=ft.Colors.RED)
    success_text = ft.Text("", color=ft.Colors.GREEN)

    def handle_create(e):
        admin_username = (
            admin_username_field.value.strip() if admin_username_field.value else ""
        )
        admin_password = (
            admin_password_field.value.strip() if admin_password_field.value else ""
        )
        new_username = (
            new_username_field.value.strip() if new_username_field.value else ""
        )
        new_password = (
            new_password_field.value.strip() if new_password_field.value else ""
        )
        confirm_password = (
            confirm_password_field.value.strip() if confirm_password_field.value else ""
        )
        role = role_dropdown.value or ""

        # Validation
        if not all(
            [
                admin_username,
                admin_password,
                new_username,
                new_password,
                confirm_password,
            ]
        ):
            error_text.value = "يرجى ملء جميع الحقول"
            page.update()
            return

        if new_password != confirm_password:
            error_text.value = "كلمات المرور غير متطابقة"
            page.update()
            return

        # Verify admin credentials first
        with db_session() as db:
            admin_auth, admin_msg = auth_manager.verify_admin(
                db, admin_username, admin_password
            )
        if not admin_auth:
            error_text.value = admin_msg
            page.update()
            return

        # Create new user
        with db_session() as db:
            success, message = auth_manager.create_user(
                db, new_username, new_password, role
            )

        if success:
            success_text.value = message
            error_text.value = ""
        else:
            error_text.value = message
            success_text.value = ""

        page.update()

    def reset_create_account_form():
        admin_username_field.value = ""
        admin_password_field.value = ""
        new_username_field.value = ""
        new_password_field.value = ""
        confirm_password_field.value = ""
        role_dropdown.value = "user"
        error_text.value = ""
        success_text.value = ""

    def handle_cancel(e):
        reset_create_account_form()
        page.close(dialog)

    create_button.on_click = handle_create
    cancel_button.on_click = handle_cancel

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("إنشاء حساب جديد", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                admin_username_field,
                admin_password_field,
                new_username_field,
                new_password_field,
                confirm_password_field,
                role_dropdown,
                error_text,
                success_text,
                create_button,
                cancel_button,
            ],
            width=350,
            height=500,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    page.open(dialog)
