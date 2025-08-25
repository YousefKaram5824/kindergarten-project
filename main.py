import flet as ft
import datetime
from kindergarten_management import Student, Parent, FinancialRecord, InventoryItem, auth_manager

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
    
    # Session management
    current_user = None
    login_error_text = ft.Text("", color=ft.Colors.RED)
    
    # Login form components
    username_field = ft.TextField(
        label="اسم المستخدم",
        width=300,
        text_align=ft.TextAlign.RIGHT
    )
    
    password_field = ft.TextField(
        label="كلمة المرور",
        width=300,
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.RIGHT
    )
    
    login_button = ft.ElevatedButton(
        "تسجيل الدخول",
        width=300,
        height=50
    )
    
    def handle_login(e):
        nonlocal current_user
        username = username_field.value.strip()
        password = password_field.value.strip()
        
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
    
    # Login page layout
    login_page = ft.Column(
        [
            ft.Image(src="logo.jpg", width=200),  # Add logo at the top center
            ft.Text("نظام إدارة رياض الأطفال", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Divider(color = "#E3DCCC"),
            ft.Text("تسجيل الدخول إلى النظام", size=24, weight=ft.FontWeight.BOLD),
            username_field,
            password_field,
            login_button,
            login_error_text
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )
    
    def show_main_system():
        # Clear login page
        page.clean()
        
        # Update page title
        page.title = f"نظام إدارة رياض الأطفال - {current_user.username}"
        
        # Data storage
        students = []
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
        
        age_controls = ft.Row([
            ft.ElevatedButton("-", on_click=decrement_age, width=40),
            student_age,
            ft.ElevatedButton("+", on_click=increment_age, width=40),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
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
        
        date_picker_btn = ft.ElevatedButton(
            "اختر التاريخ",
            on_click=open_date_picker
        )
        
        phone = ft.TextField(label="رقم التليفون")
        parent_job = ft.TextField(label="وظيفة الأب")
        additional_notes = ft.TextField(label="ملاحظات إضافية", multiline=True)

        def add_student(e):
            if student_name.value and student_age.value:
                student = Student(
                    name=student_name.value,
                    age=student_age.value,
                    birth_date=birth_date.value,
                    phone=phone.value,
                    parent_job=parent_job.value
                )
                students.append(student)
                student_name.value = ""
                student_age.value = ""
                birth_date.value = ""
                phone.value = ""
                parent_job.value = ""
                additional_notes.value = ""
                update_student_list()
                snackbar = ft.SnackBar(
                    content=ft.Text("تم إضافة الطالب بنجاح!"),
                    bgcolor=ft.Colors.GREEN,
                    duration=3000
                )
                page.overlay.append(snackbar)
                page.update()
                snackbar.open = True
                snackbar.update()
                page.update()

        add_student_btn = ft.ElevatedButton("إضافة طالب", on_click=add_student)

        student_list = ft.Column()

        def update_student_list():
            student_list.controls.clear()
            for student in students:
                student_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(student.name),
                        subtitle=ft.Text(f"العمر: {student.age}, التليفون: {student.phone}"),
                    )
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
                parent_job,
                additional_notes,
                add_student_btn,
                ft.Divider(),
                ft.Text("الطلاب المسجلين:", size=18, weight=ft.FontWeight.BOLD),
                student_list
            ],
            scroll=ft.ScrollMode.AUTO
        )

        # Financial Management Form in Arabic
        financial_student_name = ft.TextField(label="اسم الطالب")
        monthly_fee = ft.TextField(label="المصروفات الشهرية", keyboard_type=ft.KeyboardType.NUMBER)
        bus_fee = ft.TextField(label="أجرة الباص", keyboard_type=ft.KeyboardType.NUMBER)

        def add_financial_record(e):
            if financial_student_name.value and monthly_fee.value:
                record = FinancialRecord(
                    student_name=financial_student_name.value,
                    monthly_fee=monthly_fee.value,
                    bus_fee=bus_fee.value
                )
                financial_records.append(record)
                financial_student_name.value = ""
                monthly_fee.value = ""
                bus_fee.value = ""
                update_financial_list()
                snackbar = ft.SnackBar(
                    content=ft.Text("تم إضافة السجل المالي بنجاح!"),
                    bgcolor=ft.Colors.GREEN,
                    duration=3000
                )
                page.overlay.append(snackbar)
                page.update()
                snackbar.open = True
                snackbar.update()
                page.update()

        add_financial_btn = ft.ElevatedButton("إضافة سجل مالي", on_click=add_financial_record)

        financial_list = ft.Column()

        def update_financial_list():
            financial_list.controls.clear()
            for record in financial_records:
                financial_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(record.student_name),
                        subtitle=ft.Text(f"شهري: ${record.monthly_fee}, باص: ${record.bus_fee}"),
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
                financial_list
            ],
            scroll=ft.ScrollMode.AUTO
        )

        # Inventory Management Form in Arabic
        item_name = ft.TextField(label="اسم الأداة")
        item_quantity = ft.TextField(label="الكمية", keyboard_type=ft.KeyboardType.NUMBER)
        purchase_price = ft.TextField(label="سعر الشراء", keyboard_type=ft.KeyboardType.NUMBER)

        def add_inventory_item(e):
            if item_name.value and item_quantity.value:
                item = InventoryItem(
                    item_name=item_name.value,
                    quantity=item_quantity.value,
                    purchase_price=purchase_price.value
                )
                inventory_items.append(item)
                item_name.value = ""
                item_quantity.value = ""
                purchase_price.value = ""
                update_inventory_list()
                snackbar = ft.SnackBar(
                    content=ft.Text("تم إضافة العنصر بنجاح!"),
                    bgcolor=ft.Colors.GREEN,
                    duration=3000
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
                        subtitle=ft.Text(f"الكمية: {item.quantity}, السعر: ${item.purchase_price}"),
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
                inventory_list
            ],
            scroll=ft.ScrollMode.AUTO
        )

        # Reports Tab in Arabic
        def generate_report(e):
            total_students = len(students)
            total_financial = sum(float(record.monthly_fee) + float(record.bus_fee or 0) for record in financial_records)
            total_inventory = sum(float(item.quantity) * float(item.purchase_price or 0) for item in inventory_items)
            
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
            multiline=True,
            read_only=True,
            expand=True,
            border=ft.InputBorder.NONE
        )

        generate_report_btn = ft.ElevatedButton("إنشاء تقرير", on_click=generate_report)

        reports_tab = ft.Column(
            [
                ft.Text("التقارير", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                generate_report_btn,
                ft.Divider(),
                report_content
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        # Update tabs content
        tabs.tabs[0].content = student_registration_tab
        tabs.tabs[1].content = financial_tab
        tabs.tabs[2].content = inventory_tab
        tabs.tabs[3].content = reports_tab

        # Main layout in Arabic
        page.add(
            ft.Text("نظام إدارة رياض الأطفال", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Divider(),
            tabs
        )

    # Display login page initially
    page.add(login_page)

if __name__ == "__main__":
    ft.app(target=main)
