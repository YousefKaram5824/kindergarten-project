import datetime
import flet as ft

# Local imports
from database import db

def create_student_registration_tab(page: ft.Page):
    """Create and return the student registration tab"""
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
                mum_job=mum_job.value
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
                    duration=3000
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
                    duration=3000
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
                        ft.DataCell(ft.Text(student['name'])),
                        ft.DataCell(ft.Text(str(student['age']))),
                        ft.DataCell(ft.Text(student['birth_date'] or "-")),
                        ft.DataCell(ft.Text(student['phone'] or "-")),
                        ft.DataCell(ft.Text(student['dad_job'] or "-")),
                        ft.DataCell(ft.Text(student['mum_job'] or "-")),
                    ]
                )
            )
        page.update()

    # Load initial student data
    update_student_table()

    return ft.Column(
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
            ft.Row([
                ft.Text("الطلاب المسجلين:", size=18, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=student_data_table,
                height=400,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                padding=10,
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )
