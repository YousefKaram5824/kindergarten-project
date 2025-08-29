import flet as ft

# Local imports
from kindergarten_management import auth_manager

# This will be set by the main application
show_main_system_callback = None


def set_show_main_system_callback(callback):
    """Set the callback function to show the main system"""
    global show_main_system_callback
    show_main_system_callback = callback


def show_forgot_password_dialog(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    """Show forgot password dialog with admin verification"""
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
        success, message = auth_manager.reset_password(
            target_username, new_password, admin_username, admin_password
        )

        if success:
            success_text.value = message
            error_text.value = ""
        else:
            error_text.value = message
            success_text.value = ""

        page.update()

    def handle_cancel(e):
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
            width=400,
            height=500,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    page.open(dialog)


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
        admin_auth, admin_msg = auth_manager.verify_admin(
            admin_username, admin_password
        )
        if not admin_auth:
            error_text.value = admin_msg
            page.update()
            return

        # Create new user
        success, message = auth_manager.create_user(new_username, new_password, role)

        if success:
            success_text.value = message
            error_text.value = ""
        else:
            error_text.value = message
            success_text.value = ""

        page.update()

    def handle_cancel(e):
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
            width=400,
            height=550,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    page.open(dialog)


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

        success, result = auth_manager.authenticate(username, password)
        if success:
            if show_main_system_callback:
                show_main_system_callback(page, result)
            # Clear any previous error message
            login_error_text.value = ""
        else:
            # Ensure result is converted to string
            login_error_text.value = str(result)
        page.update()

    login_button.on_click = handle_login

    # Hyperlinks for additional authentication features
    forgot_password_link = ft.TextButton(
        "نسيت كلمة المرور؟", on_click=lambda e: show_forgot_password_dialog(page)
    )

    create_account_link = ft.TextButton(
        "إنشاء حساب جديد", on_click=lambda e: show_create_account_dialog(page)
    )

    # Layout for login page
    login_page = ft.Column(
        [
            ft.Container(height=150),
            ft.Image(src="logo.jpg", width=200),
            ft.Text(
                "نظام إدارة رياض الأطفال",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            username_field,
            password_field,
            login_button,
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
