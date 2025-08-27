import flet as ft
import datetime
from kindergarten_management import (
    Student,
    Parent,
    FinancialRecord,
    InventoryItem,
    auth_manager,
)
from database import db

# Initialize default admin user
auth_manager.initialize_default_admin()


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

    # Session management
    current_user = None
    login_error_text = ft.Text("", color=ft.Colors.RED)

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

    def handle_login(e):
        nonlocal current_user
        username = username_field.value.strip() if username_field.value else ""
        password = password_field.value.strip() if password_field.value else ""

        if not username or not password:
            login_error_text.value = "يرجى إدخال اسم المستخدم وكلمة المرور"
            page.update()
            return

        success, result = auth_manager.authenticate(username, password)
        if success:
            current_user = result
            show_main_system()
        else:
            login_error_text.value = result
            page.update()

    login_button.on_click = handle_login

    # Hyperlinks for forgot password and create account
    forgot_password_link = ft.TextButton(
        "نسيت كلمة المرور",
        style=ft.ButtonStyle(color=ft.Colors.BLUE),
        on_click=lambda e: show_forgot_password_page(),
    )

    create_account_link = ft.TextButton(
        "إنشاء حساب جديد",
        style=ft.ButtonStyle(color=ft.Colors.BLUE),
        on_click=lambda e: show_create_account_page(),
    )

    # Forgot password page components
    admin_username_field = ft.TextField(
        label="اسم مستخدم المدير", width=300, text_align=ft.TextAlign.RIGHT
    )

    admin_password_field = ft.TextField(
        label="كلمة مرور المدير",
        width=300,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.RIGHT,
    )

    reset_username_field = ft.TextField(
        label="اسم المستخدم المراد إعادة تعيين كلمة المرور",
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

    admin_verify_button = ft.ElevatedButton("تحقق", width=150)
    reset_button = ft.ElevatedButton("إعادة تعيين", width=150)
    # Arrow icon for back buttons
    back_to_login_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK, icon_size=24, tooltip="العودة إلى تسجيل الدخول"
    )
    admin_error_text = ft.Text("", color=ft.Colors.RED)
    reset_error_text = ft.Text("", color=ft.Colors.RED)
    reset_success_text = ft.Text("", color=ft.Colors.GREEN)

    # Create account page components
    new_username_field = ft.TextField(
        label="اسم المستخدم الجديد", width=300, text_align=ft.TextAlign.RIGHT
    )

    new_user_password_field = ft.TextField(
        label="كلمة المرور",
        width=300,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.RIGHT,
    )

    confirm_new_password_field = ft.TextField(
        label="تأكيد كلمة المرور",
        width=300,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.RIGHT,
    )

    user_role_field = ft.Dropdown(
        label="الدور",
        width=300,
        options=[
            ft.dropdown.Option("admin", "مدير"),
            ft.dropdown.Option("user", "مستخدم عادي"),
        ],
        value="user",
    )

    create_user_button = ft.ElevatedButton("إنشاء حساب", width=150)
    create_back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK, icon_size=24, tooltip="العودة إلى تسجيل الدخول"
    )
    create_user_error_text = ft.Text("", color=ft.Colors.RED)
    create_user_success_text = ft.Text("", color=ft.Colors.GREEN)

    def show_forgot_password_page():
        admin_username_field.value = ""
        admin_password_field.value = ""
        reset_username_field.value = ""
        new_password_field.value = ""
        confirm_password_field.value = ""
        admin_error_text.value = ""
        reset_error_text.value = ""
        reset_success_text.value = ""

        forgot_password_page = ft.Column(
            [
                ft.Row(
                    [
                        back_to_login_button,
                        ft.Text(
                            "إعادة تعيين كلمة المرور",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            expand=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Divider(),
                ft.Text("التحقق من هوية المدير", size=18, weight=ft.FontWeight.BOLD),
                admin_username_field,
                admin_password_field,
                admin_error_text,
                admin_verify_button,
                ft.Divider(),
                ft.Text("إعادة تعيين كلمة المرور", size=18, weight=ft.FontWeight.BOLD),
                reset_username_field,
                new_password_field,
                confirm_password_field,
                reset_error_text,
                reset_success_text,
                reset_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        page.clean()
        page.add(forgot_password_page)
        page.update()

    def handle_admin_verification(e):
        admin_username = (
            admin_username_field.value.strip() if admin_username_field.value else ""
        )
        admin_password = (
            admin_password_field.value.strip() if admin_password_field.value else ""
        )

        if not admin_username or not admin_password:
            admin_error_text.value = "يرجى إدخال اسم المستخدم وكلمة المرور"
            page.update()
            return

        success, message = auth_manager.verify_admin(admin_username, admin_password)
        if success:
            admin_error_text.value = "تم التحقق من هوية المدير بنجاح ✓"
            admin_error_text.color = ft.Colors.GREEN
        else:
            admin_error_text.value = message
            admin_error_text.color = ft.Colors.RED

        page.update()

    def handle_password_reset(e):
        username = (
            reset_username_field.value.strip() if reset_username_field.value else ""
        )
        new_password = (
            new_password_field.value.strip() if new_password_field.value else ""
        )
        confirm_password = (
            confirm_password_field.value.strip() if confirm_password_field.value else ""
        )

        if not username or not new_password or not confirm_password:
            reset_error_text.value = "يرجى ملء جميع الحقول"
            page.update()
            return

        if new_password != confirm_password:
            reset_error_text.value = "كلمتا المرور غير متطابقتين"
            page.update()
            return

        success, message = auth_manager.reset_password(
            username,
            new_password,
            admin_username_field.value,
            admin_password_field.value,
        )

        if success:
            reset_success_text.value = message
            reset_error_text.value = ""
            # Clear fields after successful reset
            reset_username_field.value = ""
            new_password_field.value = ""
            confirm_password_field.value = ""
        else:
            reset_error_text.value = message
            reset_success_text.value = ""

        page.update()

    def show_create_account_page():
        new_username_field.value = ""
        new_user_password_field.value = ""
        confirm_new_password_field.value = ""
        user_role_field.value = "user"
        create_user_error_text.value = ""
        create_user_success_text.value = ""

        create_account_page = ft.Column(
            [
                ft.Row(
                    [
                        create_back_button,
                        ft.Text(
                            "إنشاء حساب جديد",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            expand=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Divider(),
                ft.Text("التحقق من هوية المدير", size=18, weight=ft.FontWeight.BOLD),
                admin_username_field,
                admin_password_field,
                admin_error_text,
                admin_verify_button,
                ft.Divider(),
                ft.Text("معلومات الحساب الجديد", size=18, weight=ft.FontWeight.BOLD),
                new_username_field,
                new_user_password_field,
                confirm_new_password_field,
                user_role_field,
                create_user_error_text,
                create_user_success_text,
                create_user_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        page.clean()
        page.add(create_account_page)
        page.update()

    def handle_create_account(e):
        username = new_username_field.value.strip() if new_username_field.value else ""
        password = (
            new_user_password_field.value.strip()
            if new_user_password_field.value
            else ""
        )
        confirm_password = (
            confirm_new_password_field.value.strip()
            if confirm_new_password_field.value
            else ""
        )
        role = user_role_field.value

        if not username or not password or not confirm_password:
            create_user_error_text.value = "يرجى ملء جميع الحقول"
            page.update()
            return

        if password != confirm_password:
            create_user_error_text.value = "كلمتا المرور غير متطابقتين"
            page.update()
            return

        success, message = auth_manager.create_user(username, password, role)

        if success:
            create_user_success_text.value = message
            create_user_error_text.value = ""
            # Clear fields after successful creation
            new_username_field.value = ""
            new_user_password_field.value = ""
            confirm_new_password_field.value = ""
        else:
            create_user_error_text.value = message
            create_user_success_text.value = ""

        page.update()

    def back_to_login(e):
        page.clean()
        page.add(login_page)
        page.update()

    admin_verify_button.on_click = handle_admin_verification
    reset_button.on_click = handle_password_reset
    create_user_button.on_click = handle_create_account
    back_to_login_button.on_click = back_to_login
    create_back_button.on_click = back_to_login

    # Login page layout
    login_page = ft.Column(
        [
            ft.Image(src="logo.jpg", width=200),  # Add logo at the top center
            ft.Text(
                "نظام إدارة رياض الأطفال",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Divider(color="#E3DCCC"),
            ft.Text("تسجيل الدخول إلى النظام", size=24, weight=ft.FontWeight.BOLD),
            username_field,
            password_field,
            login_button,
            login_error_text,
            ft.Row(
                [forgot_password_link, create_account_link],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    def show_main_system():
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
                ft.Tab(text="التقارير"),
            ],
            expand=1,
        )

        # Student Registration Form in Arabic
        student_name = ft.TextField(label="اسم الطالب")

        # Age counter
        student_age = ft.Text("0", size=20, weight=ft.FontWeight.BOLD)
        age_counter = 0

        def increment_age(e):
            nonlocal age_counter
            age_counter += 1
            student_age.value = str(age_counter)
            page.update()

        def decrement_age(e):
            nonlocal age_counter
            if age_counter > 0:
                age_counter -= 1
                student_age.value = str(age_counter)
                page.update()

        age_controls = ft.Row(
            [
                ft.ElevatedButton("-", on_click=decrement_age, width=40),
                student_age,
                ft.ElevatedButton("+", on_click=increment_age, width=40),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Date picker for birth date
        birth_date = ft.TextField(label="تاريخ الميلاد", read_only=True)
        selected_date = None

        def handle_date_picker(e):
            nonlocal selected_date
            if e.control.value:
                selected_date = e.control.value
                birth_date.value = selected_date.strftime("%Y-%m-%d")
                page.update()

        date_picker = ft.DatePicker(
            on_change=handle_date_picker,
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime.now(),
        )
        page.overlay.append(date_picker)

        def open_date_picker(e):
            page.open(date_picker)

        date_picker_btn = ft.ElevatedButton("اختر التاريخ", on_click=open_date_picker)

        phone = ft.TextField(label="رقم التليفون")
        dad_job = ft.TextField(label="وظيفة الأب")
        mum_job = ft.TextField(label="وظيفة الأم")
        additional_notes = ft.TextField(label="ملاحظات إضافية", multiline=True)

        def add_student(e):
            if student_name.value and student_age.value:
                # Add student to database
                student_id = db.create_student(
                    name=student_name.value,
                    age=int(student_age.value),
                    birth_date=birth_date.value,
                    phone=phone.value,
                    dad_job=dad_job.value,
                    mum_job=mum_job.value,
                )

                if student_id != -1:
                    # Clear form fields
                    student_name.value = ""
                    student_age.value = "0"
                    age_counter = 0
                    birth_date.value = ""
                    phone.value = ""
                    dad_job.value = ""
                    mum_job.value = ""
                    additional_notes.value = ""

                    # Refresh student table
                    update_student_table()

                    snackbar = ft.SnackBar(
                        content=ft.Text("تم إضافة الطالب بنجاح!"),
                        bgcolor=ft.Colors.GREEN,
                        duration=3000,
                    )
                    page.overlay.append(snackbar)
                    page.update()
                    snackbar.open = True
                    snackbar.update()
                    page.update()
                else:
                    snackbar = ft.SnackBar(
                        content=ft.Text("فشل في إضافة الطالب!"),
                        bgcolor=ft.Colors.RED,
                        duration=3000,
                    )
                    page.overlay.append(snackbar)
                    page.update()
                    snackbar.open = True
                    snackbar.update()
                    page.update()

        add_student_btn = ft.ElevatedButton("إضافة طالب", on_click=add_student)

        # Student table with database integration
        student_data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("الاسم")),
                ft.DataColumn(ft.Text("العمر")),
                ft.DataColumn(ft.Text("تاريخ الميلاد")),
                ft.DataColumn(ft.Text("رقم التليفون")),
                ft.DataColumn(ft.Text("وظيفة الأب")),
                ft.DataColumn(ft.Text("وظيفة الأم")),
            ],
            rows=[],
        )

        def update_student_table():
            # Get students from database
            students_data = db.get_all_students()
            student_data_table.rows.clear()

            for student in students_data:
                student_data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(student["name"])),
                            ft.DataCell(ft.Text(str(student["age"]))),
                            ft.DataCell(ft.Text(student["birth_date"] or "-")),
                            ft.DataCell(ft.Text(student["phone"] or "-")),
                            ft.DataCell(ft.Text(student["dad_job"] or "-")),
                            ft.DataCell(ft.Text(student["mum_job"] or "-")),
                        ]
                    )
                )
            page.update()

        # Refresh button for student table
        refresh_students_btn = ft.ElevatedButton(
            "تحديث القائمة", on_click=lambda e: update_student_table()
        )

        student_registration_tab = ft.Column(
            [
                ft.Text("تسجيل الطلاب", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                student_name,
                age_controls,
                birth_date,
                date_picker_btn,
                phone,
                dad_job,
                mum_job,
                additional_notes,
                add_student_btn,
                ft.Divider(),
                ft.Row(
                    [
                        ft.Text("الطلاب المسجلين:", size=18, weight=ft.FontWeight.BOLD),
                        refresh_students_btn,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=student_data_table,
                    height=400,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=10,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        # Load initial student data
        update_student_table()

        # Financial Management Form in Arabic
        financial_student_name = ft.TextField(label="اسم الطالب")
        monthly_fee = ft.TextField(
            label="المصروفات الشهرية", keyboard_type=ft.KeyboardType.NUMBER
        )
        bus_fee = ft.TextField(label="أجرة الباص", keyboard_type=ft.KeyboardType.NUMBER)

        def add_financial_record(e):
            if financial_student_name.value and monthly_fee.value:
                record = FinancialRecord(
                    student_name=financial_student_name.value,
                    monthly_fee=monthly_fee.value,
                    bus_fee=bus_fee.value,
                )
                financial_records.append(record)
                financial_student_name.value = ""
                monthly_fee.value = ""
                bus_fee.value = ""
                update_financial_list()
                snackbar = ft.SnackBar(
                    content=ft.Text("تم إضافة السجل المالي بنجاح!"),
                    bgcolor=ft.Colors.GREEN,
                    duration=3000,
                )
                page.overlay.append(snackbar)
                page.update()
                snackbar.open = True
                snackbar.update()
                page.update()

        add_financial_btn = ft.ElevatedButton(
            "إضافة سجل مالي", on_click=add_financial_record
        )

        financial_list = ft.Column()

        def update_financial_list():
            financial_list.controls.clear()
            for record in financial_records:
                financial_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(record.student_name),
                        subtitle=ft.Text(
                            f"شهري: ${record.monthly_fee}, باص: ${record.bus_fee}"
                        ),
                    )
                )

        financial_tab = ft.Column(
            [
                ft.Text("الإدارة المالية", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                financial_student_name,
                monthly_fee,
                bus_fee,
                add_financial_btn,
                ft.Divider(),
                ft.Text("السجلات المالية:", size=18, weight=ft.FontWeight.BOLD),
                financial_list,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        # Inventory Management Form in Arabic
        item_name = ft.TextField(label="اسم الأداة")
        item_quantity = ft.TextField(
            label="الكمية", keyboard_type=ft.KeyboardType.NUMBER
        )
        purchase_price = ft.TextField(
            label="سعر الشراء", keyboard_type=ft.KeyboardType.NUMBER
        )

        def add_inventory_item(e):
            if item_name.value and item_quantity.value:
                item = InventoryItem(
                    item_name=item_name.value,
                    quantity=item_quantity.value,
                    purchase_price=purchase_price.value,
                )
                inventory_items.append(item)
                item_name.value = ""
                item_quantity.value = ""
                purchase_price.value = ""
                update_inventory_list()
                snackbar = ft.SnackBar(
                    content=ft.Text("تم إضافة العنصر بنجاح!"),
                    bgcolor=ft.Colors.GREEN,
                    duration=3000,
                )
                page.overlay.append(snackbar)
                page.update()
                snackbar.open = True
                snackbar.update()
                page.update()

        add_inventory_btn = ft.ElevatedButton("إضافة عنصر", on_click=add_inventory_item)

        inventory_list = ft.Column()

        def update_inventory_list():
            inventory_list.controls.clear()
            for item in inventory_items:
                inventory_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(item.item_name),
                        subtitle=ft.Text(
                            f"الكمية: {item.quantity}, السعر: ${item.purchase_price}"
                        ),
                    )
                )

        inventory_tab = ft.Column(
            [
                ft.Text("إدارة المخزون", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                item_name,
                item_quantity,
                purchase_price,
                add_inventory_btn,
                ft.Divider(),
                ft.Text("عناصر المخزون:", size=18, weight=ft.FontWeight.BOLD),
                inventory_list,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        # Reports Tab in Arabic
        def generate_report(e):
            students_data = db.get_all_students()
            total_students = len(students_data)
            total_financial = sum(
                float(record.monthly_fee) + float(record.bus_fee or 0)
                for record in financial_records
            )
            total_inventory = sum(
                float(item.quantity) * float(item.purchase_price or 0)
                for item in inventory_items
            )

            report_content.value = f"""
            تقرير نظام إدارة رياض الأطفال
            =============================
            
            إجمالي الطلاب: {total_students}
            القيمة المالية الإجمالية: ${total_financial:,.2f}
            قيمة المخزون الإجمالية: ${total_inventory:,.2f}
            
            الطلاب:
            {chr(10).join([f"- {s.name} (العمر: {s.age})" for s in students])}
            
            السجلات المالية:
            {chr(10).join([f"- {r.student_name}: شهري ${r.monthly_fee}, باص ${r.bus_fee or 0}" for r in financial_records])}
            
            عناصر المخزون:
            {chr(10).join([f"- {i.item_name}: {i.quantity} وحدة @ ${i.purchase_price or 0} لكل" for i in inventory_items])}
            """
            page.update()

        report_content = ft.TextField(
            multiline=True, read_only=True, expand=True, border=ft.InputBorder.NONE
        )

        generate_report_btn = ft.ElevatedButton("إنشاء تقرير", on_click=generate_report)

        reports_tab = ft.Column(
            [
                ft.Text("التقارير", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                generate_report_btn,
                ft.Divider(),
                report_content,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # Update tabs content
        tabs.tabs[0].content = student_registration_tab
        tabs.tabs[1].content = financial_tab
        tabs.tabs[2].content = inventory_tab
        tabs.tabs[3].content = reports_tab

        # Back button for returning to login
        back_to_login_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_size=24,
            tooltip="العودة إلى تسجيل الدخول",
            on_click=back_to_login,  # Connect to the existing back_to_login function
        )

        # Main layout in Arabic
        page.add(back_to_login_button)  # Add the back button to the layout
        page.add(
            ft.Text(
                "نظام إدارة رياض الأطفال",
                size=32,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Divider(),
            tabs,
        )

    # Display login page initially
    page.add(login_page)


if __name__ == "__main__":
    ft.app(target=main)
