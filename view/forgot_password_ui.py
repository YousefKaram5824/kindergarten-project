import flet as ft

# Local imports
from kindergarten_management import auth_manager
from database import db_session


def show_forgot_password_dialog(page: ft.Page):
    """Show forgot password dialog with admin verification"""
    admin_username_field = ft.TextField(
        label="اسم المستخدم للمدير",
        width=300,
        text_align=ft.TextAlign.RIGHT,
    )

    admin_password_field = ft.TextField(
        label="كلمة المرور المدير",
        width=300,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.RIGHT,
    )

    target_username_field = ft.TextField(
        label="اسم المستخدم المراد إعادة تعيين كلمته",
        width=300,
        text_align=ft.TextAlign.RIGHT,
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

    reset_button = ft.ElevatedButton("إعادة تعيين كلمة المرور", width=300, height=50)

    cancel_button = ft.TextButton("إلغاء", width=300)
    error_text = ft.Text("", color=ft.Colors.RED)
    success_text = ft.Text("", color=ft.Colors.GREEN)

    def handle_reset(e):
        admin_username = (
            admin_username_field.value.strip() if admin_username_field.value else ""
        )
        admin_password = (
            admin_password_field.value.strip() if admin_password_field.value else ""
        )
        target_username = (
            target_username_field.value.strip() if target_username_field.value else ""
        )
        new_password = (
            new_password_field.value.strip() if new_password_field.value else ""
        )
        confirm_password = (
            confirm_password_field.value.strip() if confirm_password_field.value else ""
        )

        # Validation
        if not all(
            [
                admin_username,
                admin_password,
                target_username,
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

        # Reset password
        with db_session() as db:
            success, message = auth_manager.reset_password(
                db, target_username, new_password, admin_username, admin_password
            )

        if success:
            success_text.value = message
            error_text.value = ""
        else:
            error_text.value = message
            success_text.value = ""

        page.update()

    def reset_forgot_password_form():
        admin_username_field.value = ""
        admin_password_field.value = ""
        target_username_field.value = ""
        new_password_field.value = ""
        confirm_password_field.value = ""
        error_text.value = ""
        success_text.value = ""

    def handle_cancel(e):
        reset_forgot_password_form()
        page.close(dialog)

    reset_button.on_click = handle_reset
    cancel_button.on_click = handle_cancel

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("إعادة تعيين كلمة المرور", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                admin_username_field,
                admin_password_field,
                target_username_field,
                new_password_field,
                confirm_password_field,
                error_text,
                success_text,
                reset_button,
                cancel_button,
            ],
            width=350,
            height=450,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    page.open(dialog)
