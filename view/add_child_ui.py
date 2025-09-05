import datetime
import os
import shutil
import flet as ft

# Local imports
from database import db_session
from DTOs.child_dto import CreateChildDTO
from DTOs.full_day_program_dto import CreateFullDayProgramDTO
from DTOs.individual_session_dto import CreateIndividualSessionDTO
from models import ChildTypeEnum
from logic.child_logic import ChildService
from logic.full_day_program_logic import FullDayProgramService
from logic.individual_session_logic import IndividualSessionService

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8


def create_add_child_dialog(page: ft.Page, update_table_callback):
    """Create and return the add child dialog and button"""

    # Form fields
    child_id = ft.TextField(
        label="رقم التعريفي للطالب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        hint_text="أدخل رقم أكبر من 100",
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
    )
    child_name = ft.TextField(
        label="اسم الطالب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    child_age = ft.TextField(
        value="3",
        text_align=ft.TextAlign.CENTER,
        width=60,
        height=40,
        content_padding=ft.padding.all(8),
        border_radius=ft.border_radius.all(BORDER_RADIUS),
        border_color=ft.Colors.BLUE,
        bgcolor=INPUT_BGCOLOR,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
    )
    age_counter = 3
    birth_date = ft.TextField(
        label="تاريخ الميلاد",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=210,
    )
    selected_date = None
    created_at_date = ft.TextField(
        label="تاريخ التسجيل",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=170,
    )
    created_at_time = ft.TextField(
        label="وقت التسجيل",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=170,
    )
    selected_created_at_date = None
    selected_created_at_time = None
    phone = ft.TextField(
        label="رقم التليفون",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    dad_job = ft.TextField(
        label="وظيفة الأب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    mum_job = ft.TextField(
        label="وظيفة الأم",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    problem = ft.TextField(
        label="المشكلة",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    additional_notes = ft.TextField(
        label="ملاحظات إضافية",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    photo_path = None
    photo_preview = ft.Image(
        src="", width=100, height=100, fit=ft.ImageFit.COVER, visible=False
    )
    photo_status = ft.Text(
        "لم يتم اختيار صورة",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
    )

    # Child type dropdown
    selected_child_type = None

    # Checkboxes for child type
    full_day_checkbox = ft.Checkbox(
        label=ChildTypeEnum.FULL_DAY.value,
        value=False,
        on_change=lambda e: on_checkbox_change(e, ChildTypeEnum.FULL_DAY),
    )
    sessions_checkbox = ft.Checkbox(
        label=ChildTypeEnum.SESSIONS.value,
        value=False,
        on_change=lambda e: on_checkbox_change(e, ChildTypeEnum.SESSIONS),
    )

    # Conditional fields
    monthly_fee = ft.TextField(
        label="قيمة الاشتراك الشهري",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9.]", replacement_string=""
        ),
        visible=False,
    )
    bus_fee = ft.TextField(
        label="قيمة اشتراك الباص",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9.]", replacement_string=""
        ),
        visible=False,
    )
    session_fee = ft.TextField(
        label="قيمة الجلسة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9.]", replacement_string=""
        ),
        visible=False,
    )
    monthly_sessions_count = ft.TextField(
        label="عدد الجلسات الشهرية",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
        visible=False,
    )

    # Additional fields for program/session data
    diagnosis = ft.TextField(
        label="التشخيص",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        multiline=True,
        visible=False,
    )
    tests_applied = ft.TextField(
        label="الاختبارات المطبقة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        multiline=True,
        visible=False,
    )
    training_plan = ft.TextField(
        label="خطة التدريب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        multiline=True,
        visible=False,
    )
    monthly_report = ft.TextField(
        label="التقرير الشهري",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        multiline=True,
        visible=False,
    )
    attendance_status = ft.TextField(
        label="حالة الحضور",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        visible=False,
    )
    attended_sessions_count = ft.TextField(
        label="عدد الجلسات المحضورة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
        visible=False,
    )
    specialist_name = ft.TextField(
        label="اسم المتخصص",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        visible=False,
    )

    # File upload fields
    personal_photo_path = None
    birth_certificate_path = None
    father_id_card_path = None
    test_documents_path = None
    tests_applied_file_path = None
    training_plan_file_path = None
    monthly_report_file_path = None
    child_documents_file_path = None

    personal_photo_status = ft.Text(
        "لم يتم اختيار صورة شخصية",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
    )
    birth_certificate_status = ft.Text(
        "لم يتم اختيار شهادة الميلاد",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
    )
    father_id_card_status = ft.Text(
        "لم يتم اختيار بطاقة الأب",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
    )
    test_documents_status = ft.Text(
        "لم يتم اختيار وثائق الاختبارات",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
    )
    tests_applied_file_status = ft.Text(
        "لم يتم اختيار ملف الاختبارات المطبقة",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
    )
    training_plan_file_status = ft.Text(
        "لم يتم اختيار ملف خطة التدريب",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
    )
    monthly_report_file_status = ft.Text(
        "لم يتم اختيار ملف التقرير الشهري",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
    )
    child_documents_file_status = ft.Text(
        "لم يتم اختيار ملف وثائق الطفل",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
        visible=False,
    )

    # File upload buttons
    personal_photo_btn = ft.ElevatedButton(
        "رفع صورة شخصية",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: pick_file(e, "personal_photo"),
        visible=False,
    )
    birth_certificate_btn = ft.ElevatedButton(
        "رفع شهادة الميلاد",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: pick_file(e, "birth_certificate"),
        visible=False,
    )
    father_id_card_btn = ft.ElevatedButton(
        "رفع بطاقة الأب",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: pick_file(e, "father_id_card"),
        visible=False,
    )
    test_documents_btn = ft.ElevatedButton(
        "رفع وثائق الاختبارات",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: pick_file(e, "test_documents"),
        visible=False,
    )
    tests_applied_file_btn = ft.ElevatedButton(
        "رفع ملف الاختبارات المطبقة",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: pick_file(e, "tests_applied_file"),
        visible=False,
    )
    training_plan_file_btn = ft.ElevatedButton(
        "رفع ملف خطة التدريب",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: pick_file(e, "training_plan_file"),
        visible=False,
    )
    monthly_report_file_btn = ft.ElevatedButton(
        "رفع ملف التقرير الشهري",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: pick_file(e, "monthly_report_file"),
        visible=False,
    )
    child_documents_file_btn = ft.ElevatedButton(
        "رفع ملف وثائق الطفل",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: pick_file(e, "child_documents_file"),
        visible=False,
    )

    def on_checkbox_change(e, checkbox_type):
        nonlocal selected_child_type
        if checkbox_type == ChildTypeEnum.FULL_DAY:
            if e.control.value:
                selected_child_type = ChildTypeEnum.FULL_DAY
                sessions_checkbox.value = False
                # Show full day fields, hide sessions fields
                monthly_fee.visible = True
                bus_fee.visible = True
                session_fee.visible = False
                monthly_sessions_count.visible = False
                # Show additional fields for full day
                diagnosis.visible = True
                tests_applied.visible = True
                training_plan.visible = True
                monthly_report.visible = True
                attendance_status.visible = True
                attended_sessions_count.visible = False
                specialist_name.visible = False
                # Show file upload buttons for full day
                personal_photo_btn.visible = True
                birth_certificate_btn.visible = True
                father_id_card_btn.visible = True
                test_documents_btn.visible = True
                tests_applied_file_btn.visible = True
                training_plan_file_btn.visible = True
                monthly_report_file_btn.visible = True
                child_documents_file_btn.visible = True
                personal_photo_status.visible = True
                birth_certificate_status.visible = True
                father_id_card_status.visible = True
                test_documents_status.visible = True
                tests_applied_file_status.visible = True
                training_plan_file_status.visible = True
                monthly_report_file_status.visible = True
                child_documents_file_status.visible = True
            else:
                selected_child_type = None
                monthly_fee.visible = False
                bus_fee.visible = False
                session_fee.visible = False
                monthly_sessions_count.visible = False
                # Hide additional fields
                diagnosis.visible = False
                tests_applied.visible = False
                training_plan.visible = False
                monthly_report.visible = False
                attendance_status.visible = False
                attended_sessions_count.visible = False
                specialist_name.visible = False
                # Hide file upload buttons
                personal_photo_btn.visible = False
                birth_certificate_btn.visible = False
                father_id_card_btn.visible = False
                test_documents_btn.visible = False
                tests_applied_file_btn.visible = False
                training_plan_file_btn.visible = False
                monthly_report_file_btn.visible = False
                child_documents_file_btn.visible = False
                personal_photo_status.visible = False
                birth_certificate_status.visible = False
                father_id_card_status.visible = False
                test_documents_status.visible = False
                tests_applied_file_status.visible = False
                training_plan_file_status.visible = False
                monthly_report_file_status.visible = False
                child_documents_file_status.visible = False
        elif checkbox_type == ChildTypeEnum.SESSIONS:
            if e.control.value:
                selected_child_type = ChildTypeEnum.SESSIONS
                full_day_checkbox.value = False
                # Show sessions fields, hide full day fields
                monthly_fee.visible = False
                bus_fee.visible = False
                session_fee.visible = True
                monthly_sessions_count.visible = True
                # Show additional fields for sessions
                diagnosis.visible = True
                tests_applied.visible = True
                training_plan.visible = False
                monthly_report.visible = True
                attendance_status.visible = False
                attended_sessions_count.visible = True
                specialist_name.visible = True
                # Hide file upload buttons for sessions (no file uploads for sessions)
                personal_photo_btn.visible = False
                birth_certificate_btn.visible = False
                father_id_card_btn.visible = False
                test_documents_btn.visible = False
                tests_applied_file_btn.visible = False
                training_plan_file_btn.visible = False
                monthly_report_file_btn.visible = False
                child_documents_file_btn.visible = False
                personal_photo_status.visible = False
                birth_certificate_status.visible = False
                father_id_card_status.visible = False
                test_documents_status.visible = False
                tests_applied_file_status.visible = False
                training_plan_file_status.visible = False
                monthly_report_file_status.visible = False
                child_documents_file_status.visible = False
            else:
                selected_child_type = None
                monthly_fee.visible = False
                bus_fee.visible = False
                session_fee.visible = False
                monthly_sessions_count.visible = False
                # Hide additional fields
                diagnosis.visible = False
                tests_applied.visible = False
                training_plan.visible = False
                monthly_report.visible = False
                attendance_status.visible = False
                attended_sessions_count.visible = False
                specialist_name.visible = False
                # Hide file upload buttons
                personal_photo_btn.visible = False
                birth_certificate_btn.visible = False
                father_id_card_btn.visible = False
                test_documents_btn.visible = False
                tests_applied_file_btn.visible = False
                training_plan_file_btn.visible = False
                monthly_report_file_btn.visible = False
                child_documents_file_btn.visible = False
                personal_photo_status.visible = False
                birth_certificate_status.visible = False
                father_id_card_status.visible = False
                test_documents_status.visible = False
                tests_applied_file_status.visible = False
                training_plan_file_status.visible = False
                monthly_report_file_status.visible = False
                child_documents_file_status.visible = False
        # Update UI to reflect changes
        page.update()

    def increment_age(e):
        nonlocal age_counter
        age_counter += 1
        child_age.value = str(age_counter)
        page.update()

    def decrement_age(e):
        nonlocal age_counter
        if age_counter > 0:
            age_counter -= 1
            child_age.value = str(age_counter)
        page.update()

    age_controls = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                on_click=decrement_age,
                icon_size=20,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.BLUE,
                    shape=ft.RoundedRectangleBorder(
                        radius=ft.border_radius.all(BORDER_RADIUS)
                    ),
                ),
            ),
            child_age,
            ft.IconButton(
                icon=ft.Icons.ADD,
                on_click=increment_age,
                icon_size=20,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.BLUE,
                    shape=ft.RoundedRectangleBorder(
                        radius=ft.border_radius.all(BORDER_RADIUS)
                    ),
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    def handle_date_picker(e):
        nonlocal selected_date
        if e.control.value:
            selected_date = e.control.value
            birth_date.value = selected_date.strftime("%Y-%m-%d")
            page.update()

    def open_date_picker(e):
        page.open(date_picker)

    date_picker_btn = ft.ElevatedButton("اختر التاريخ", on_click=open_date_picker)

    def handle_created_at_date_picker(e):
        nonlocal selected_created_at_date
        if e.control.value:
            selected_created_at_date = e.control.value
            created_at_date.value = selected_created_at_date.strftime("%Y-%m-%d")
            page.update()

    def open_created_at_date_picker(e):
        page.open(created_at_date_picker)

    created_at_date_picker_btn = ft.ElevatedButton(
        "اختر تاريخ التسجيل", on_click=open_created_at_date_picker
    )

    def handle_created_at_time_picker(e):
        nonlocal selected_created_at_time
        if e.control.value:
            selected_created_at_time = e.control.value
            created_at_time.value = selected_created_at_time.strftime("%H:%M")
            page.update()

    def open_created_at_time_picker(e):
        page.open(created_at_time_picker)

    created_at_time_picker_btn = ft.ElevatedButton(
        "اختر وقت التسجيل", on_click=open_created_at_time_picker
    )

    def pick_photo(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الطالب",
        )

    def pick_file(e, file_type):
        nonlocal file_picker
        extensions = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"]
        dialog_title = "اختر ملف"

        if file_type == "personal_photo":
            extensions = ["jpg", "jpeg", "png", "gif"]
            dialog_title = "اختر صورة شخصية"
        elif file_type == "birth_certificate":
            extensions = ["jpg", "jpeg", "png", "gif", "pdf"]
            dialog_title = "اختر شهادة الميلاد"
        elif file_type == "father_id_card":
            extensions = ["jpg", "jpeg", "png", "gif", "pdf"]
            dialog_title = "اختر بطاقة الأب"
        elif file_type == "test_documents":
            extensions = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"]
            dialog_title = "اختر وثائق الاختبارات"
        elif file_type == "tests_applied_file":
            extensions = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"]
            dialog_title = "اختر ملف الاختبارات المطبقة"
        elif file_type == "training_plan_file":
            extensions = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"]
            dialog_title = "اختر ملف خطة التدريب"
        elif file_type == "monthly_report_file":
            extensions = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"]
            dialog_title = "اختر ملف التقرير الشهري"
        elif file_type == "child_documents_file":
            extensions = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"]
            dialog_title = "اختر ملف وثائق الطفل"

        # Create a new file picker for this specific file type
        file_picker = ft.FilePicker(
            on_result=lambda e, ft=file_type: handle_file_picker_result(e, ft)
        )
        page.overlay.append(file_picker)
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=extensions,
            dialog_title=dialog_title,
        )

    photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الطالب", icon=ft.Icons.UPLOAD_FILE, on_click=pick_photo
    )

    # Add child Dialog - Matching auth dialog style
    add_child_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("إضافة طالب جديد", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                child_id,
                child_name,
                ft.Container(
                    ft.Text("العمر:", size=16, text_align=ft.TextAlign.RIGHT),
                    padding=ft.padding.only(bottom=5),
                ),
                age_controls,
                ft.Row(
                    [date_picker_btn, birth_date],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [created_at_date_picker_btn, created_at_date],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [created_at_time_picker_btn, created_at_time],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                phone,
                dad_job,
                mum_job,
                problem,
                additional_notes,
                ft.Container(
                    ft.Text(
                        "صورة الطالب:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    padding=ft.padding.only(top=10, bottom=5),
                ),
                photo_upload_btn,
                ft.Container(
                    ft.Row([photo_preview], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(top=5, bottom=5),
                ),
                ft.Container(photo_status, padding=ft.padding.only(bottom=10)),
                ft.Container(
                    ft.Text("نوع الطالب:", size=16, text_align=ft.TextAlign.RIGHT),
                    padding=ft.padding.only(bottom=5),
                ),
                ft.Row(
                    [full_day_checkbox, sessions_checkbox],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                monthly_fee,
                bus_fee,
                session_fee,
                monthly_sessions_count,
                # Additional fields for program/session data
                diagnosis,
                tests_applied,
                training_plan,
                monthly_report,
                attendance_status,
                attended_sessions_count,
                specialist_name,
                # File upload section
                ft.Container(
                    ft.Text(
                        "الملفات والوثائق:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    padding=ft.padding.only(top=10, bottom=5),
                ),
                personal_photo_btn,
                ft.Container(personal_photo_status, padding=ft.padding.only(bottom=5)),
                birth_certificate_btn,
                ft.Container(
                    birth_certificate_status, padding=ft.padding.only(bottom=5)
                ),
                father_id_card_btn,
                ft.Container(father_id_card_status, padding=ft.padding.only(bottom=5)),
                test_documents_btn,
                ft.Container(test_documents_status, padding=ft.padding.only(bottom=5)),
                tests_applied_file_btn,
                ft.Container(
                    tests_applied_file_status, padding=ft.padding.only(bottom=5)
                ),
                training_plan_file_btn,
                ft.Container(
                    training_plan_file_status, padding=ft.padding.only(bottom=5)
                ),
                monthly_report_file_btn,
                ft.Container(
                    monthly_report_file_status, padding=ft.padding.only(bottom=5)
                ),
                child_documents_file_btn,
                ft.Container(
                    child_documents_file_status, padding=ft.padding.only(bottom=10)
                ),
            ],
            width=400,
            height=800,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: [reset_form(), close_dialog()]),
            ft.TextButton("إضافة", on_click=lambda e: add_child()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Date picker for birth date
    date_picker = ft.DatePicker(
        on_change=handle_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(date_picker)

    # Date picker for created_at
    created_at_date_picker = ft.DatePicker(
        on_change=handle_created_at_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(created_at_date_picker)

    # Time picker for created_at
    created_at_time_picker = ft.TimePicker(
        on_change=handle_created_at_time_picker,
    )
    page.overlay.append(created_at_time_picker)

    def handle_file_picker_result(e: ft.FilePickerResultEvent, file_type=None):
        nonlocal photo_path, personal_photo_path, birth_certificate_path, father_id_card_path, test_documents_path, tests_applied_file_path, training_plan_file_path, monthly_report_file_path, child_documents_file_path
        if e.files:
            # Create child_documents directory if it doesn't exist
            docs_dir = "child_documents"
            if not os.path.exists(docs_dir):
                os.makedirs(docs_dir)

            # Copy the file to child_documents directory
            uploaded_file = e.files[0]
            file_extension = os.path.splitext(uploaded_file.name)[1]
            new_filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_type}{file_extension}"
            file_path = os.path.join(docs_dir, new_filename)

            # Copy the file
            shutil.copy2(uploaded_file.path, file_path)

            # Update the appropriate path and status based on file type
            if file_type == "personal_photo":
                personal_photo_path = file_path
                personal_photo_status.value = f"تم اختيار: {uploaded_file.name}"
                personal_photo_status.color = ft.Colors.GREEN
            elif file_type == "birth_certificate":
                birth_certificate_path = file_path
                birth_certificate_status.value = f"تم اختيار: {uploaded_file.name}"
                birth_certificate_status.color = ft.Colors.GREEN
            elif file_type == "father_id_card":
                father_id_card_path = file_path
                father_id_card_status.value = f"تم اختيار: {uploaded_file.name}"
                father_id_card_status.color = ft.Colors.GREEN
            elif file_type == "test_documents":
                test_documents_path = file_path
                test_documents_status.value = f"تم اختيار: {uploaded_file.name}"
                test_documents_status.color = ft.Colors.GREEN
            elif file_type == "tests_applied_file":
                tests_applied_file_path = file_path
                tests_applied_file_status.value = f"تم اختيار: {uploaded_file.name}"
                tests_applied_file_status.color = ft.Colors.GREEN
            elif file_type == "training_plan_file":
                training_plan_file_path = file_path
                training_plan_file_status.value = f"تم اختيار: {uploaded_file.name}"
                training_plan_file_status.color = ft.Colors.GREEN
            elif file_type == "monthly_report_file":
                monthly_report_file_path = file_path
                monthly_report_file_status.value = f"تم اختيار: {uploaded_file.name}"
                monthly_report_file_status.color = ft.Colors.GREEN
            elif file_type == "child_documents_file":
                child_documents_file_path = file_path
                child_documents_file_status.value = f"تم اختيار: {uploaded_file.name}"
                child_documents_file_status.color = ft.Colors.GREEN
            else:
                # Handle main photo upload
                photo_path = file_path
                photo_preview.src = photo_path
                photo_preview.visible = True
                photo_status.value = f"تم اختيار: {uploaded_file.name}"
                photo_status.color = ft.Colors.GREEN

            page.update()

    # Photo upload functionality
    file_picker = ft.FilePicker(on_result=handle_file_picker_result)
    page.overlay.append(file_picker)

    def add_child():
        # Validate required fields
        if not child_id.value:
            show_error("يجب إدخال رقم التعريفي!")
            return

        try:
            child_id_int = int(child_id.value)
        except ValueError:
            show_error("الرقم التعريفي يجب أن يكون رقماً صحيحاً!")
            return

        if child_id_int <= 100:
            show_error("الرقم التعريفي يجب أن يكون أكبر من 100!")
            return

        # Check uniqueness
        with db_session() as db:
            if not ChildService.is_id_available(db, child_id_int):
                show_error("الرقم التعريفي مستخدم من قبل طفل آخر!")
                return

        if not child_name.value:
            show_error("يجب إدخال اسم الطالب!")
            return

        if not child_age.value or int(child_age.value) <= 0:
            show_error("يجب إدخال عمر صحيح للطالب!")
            return

        if not birth_date.value:
            show_error("يجب اختيار تاريخ الميلاد!")
            return

        # Validate created_at date and time if provided
        created_at_value = None
        if created_at_date.value and created_at_time.value:
            try:
                created_at_value = datetime.datetime.strptime(
                    f"{created_at_date.value} {created_at_time.value}", "%Y-%m-%d %H:%M"
                )
                if created_at_value > datetime.datetime.now():
                    show_error("تاريخ ووقت التسجيل لا يمكن أن يكون في المستقبل!")
                    return
            except ValueError:
                show_error("صيغة تاريخ أو وقت التسجيل غير صحيحة!")
                return
        else:
            created_at_value = datetime.datetime.now()

        # Create child DTO with created_at value
        child_data = CreateChildDTO(
            id=child_id_int,
            name=str(child_name.value),
            age=int(child_age.value),
            birth_date=datetime.datetime.strptime(birth_date.value, "%Y-%m-%d").date(),
            phone_number=str(phone.value) if phone.value else None,
            father_job=str(dad_job.value) if dad_job.value else None,
            mother_job=str(mum_job.value) if mum_job.value else None,
            notes=str(additional_notes.value) if additional_notes.value else None,
            problems=str(problem.value) if problem.value else None,
            child_image=photo_path,
            created_at=created_at_value,
            child_type=(
                selected_child_type
                if selected_child_type is not None
                else ChildTypeEnum.FULL_DAY
            ),
        )

        # Add child to database with photo path using ChildService
        with db_session() as db:
            try:
                child_dto = ChildService.create_child(db, child_data)

                # After creating child, create related full day program or individual session data
                if child_dto:
                    if child_data.child_type == ChildTypeEnum.FULL_DAY:
                        full_day_data = CreateFullDayProgramDTO(
                            entry_date=datetime.datetime.now().date(),
                            diagnosis=str(diagnosis.value) if diagnosis.value else None,
                            tests_applied=(
                                str(tests_applied.value)
                                if tests_applied.value
                                else None
                            ),
                            monthly_fee=(
                                float(monthly_fee.value) if monthly_fee.value else None
                            ),
                            bus_fee=float(bus_fee.value) if bus_fee.value else None,
                            training_plan=(
                                str(training_plan.value)
                                if training_plan.value
                                else None
                            ),
                            monthly_report=(
                                str(monthly_report.value)
                                if monthly_report.value
                                else None
                            ),
                            attendance_status=(
                                str(attendance_status.value)
                                if attendance_status.value
                                else None
                            ),
                            notes=(
                                additional_notes.value
                                if additional_notes.value
                                else None
                            ),
                            personal_photo=personal_photo_path,
                            birth_certificate=birth_certificate_path,
                            father_id_card=father_id_card_path,
                            test_documents=test_documents_path,
                            tests_applied_file=tests_applied_file_path,
                            training_plan_file=training_plan_file_path,
                            monthly_report_file=monthly_report_file_path,
                            child_documents_file=child_documents_file_path,
                        )
                        FullDayProgramService.create_program(db, full_day_data)
                    elif child_data.child_type == ChildTypeEnum.SESSIONS:
                        individual_session_data = CreateIndividualSessionDTO(
                            entry_date=datetime.datetime.now().date(),
                            diagnosis=str(diagnosis.value) if diagnosis.value else None,
                            tests_applied=(
                                str(tests_applied.value)
                                if tests_applied.value
                                else None
                            ),
                            session_fee=(
                                float(session_fee.value) if session_fee.value else None
                            ),
                            monthly_sessions_count=(
                                int(monthly_sessions_count.value)
                                if monthly_sessions_count.value
                                else None
                            ),
                            attended_sessions_count=(
                                int(attended_sessions_count.value)
                                if attended_sessions_count.value
                                else None
                            ),
                            specialist_name=(
                                str(specialist_name.value)
                                if specialist_name.value
                                else None
                            ),
                            monthly_report=(
                                str(monthly_report.value)
                                if monthly_report.value
                                else None
                            ),
                            notes=(
                                additional_notes.value
                                if additional_notes.value
                                else None
                            ),
                        )
                        IndividualSessionService.create_session(
                            db, individual_session_data
                        )

                    # Clear form and close dialog
                    reset_form()
                    close_dialog()

                    # Refresh child table
                    update_table_callback()

                    show_success("تم إضافة الطالب بنجاح!")
                else:
                    show_error("فشل في إضافة الطالب!")
            except Exception as ex:
                show_error(f"خطأ في إضافة الطالب: {str(ex)}")

    def show_error(message):
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED,
            duration=3000,
        )
        page.overlay.append(snackbar)
        page.update()
        snackbar.open = True
        snackbar.update()
        page.update()

    def show_success(message):
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.GREEN,
            duration=3000,
        )
        page.overlay.append(snackbar)
        page.update()
        snackbar.open = True
        snackbar.update()
        page.update()

    def reset_form():
        nonlocal age_counter, photo_path, selected_date, selected_child_type, selected_created_at_date, selected_created_at_time, personal_photo_path, birth_certificate_path, father_id_card_path, test_documents_path, tests_applied_file_path, training_plan_file_path, monthly_report_file_path, child_documents_file_path
        child_id.value = ""
        child_name.value = ""
        age_counter = 3
        child_age.value = "3"
        birth_date.value = ""
        selected_date = None
        created_at_date.value = ""
        selected_created_at_date = None
        created_at_time.value = ""
        selected_created_at_time = None
        phone.value = ""
        dad_job.value = ""
        mum_job.value = ""
        problem.value = ""
        additional_notes.value = ""
        photo_path = None
        photo_preview.src = ""
        photo_preview.visible = False
        photo_status.value = "لم يتم اختيار صورة"
        photo_status.color = ft.Colors.GREY
        selected_child_type = None
        full_day_checkbox.value = False
        sessions_checkbox.value = False
        monthly_fee.value = ""
        bus_fee.value = ""
        session_fee.value = ""
        monthly_sessions_count.value = ""
        # Reset additional fields
        diagnosis.value = ""
        tests_applied.value = ""
        training_plan.value = ""
        monthly_report.value = ""
        attendance_status.value = ""
        attended_sessions_count.value = ""
        specialist_name.value = ""
        # Reset file paths
        personal_photo_path = None
        birth_certificate_path = None
        father_id_card_path = None
        test_documents_path = None
        tests_applied_file_path = None
        training_plan_file_path = None
        monthly_report_file_path = None
        child_documents_file_path = None
        # Reset file status texts
        personal_photo_status.value = "لم يتم اختيار صورة شخصية"
        personal_photo_status.color = ft.Colors.GREY
        birth_certificate_status.value = "لم يتم اختيار شهادة الميلاد"
        birth_certificate_status.color = ft.Colors.GREY
        father_id_card_status.value = "لم يتم اختيار بطاقة الأب"
        father_id_card_status.color = ft.Colors.GREY
        test_documents_status.value = "لم يتم اختيار وثائق الاختبارات"
        test_documents_status.color = ft.Colors.GREY
        tests_applied_file_status.value = "لم يتم اختيار ملف الاختبارات المطبقة"
        tests_applied_file_status.color = ft.Colors.GREY
        training_plan_file_status.value = "لم يتم اختيار ملف خطة التدريب"
        training_plan_file_status.color = ft.Colors.GREY
        monthly_report_file_status.value = "لم يتم اختيار ملف التقرير الشهري"
        monthly_report_file_status.color = ft.Colors.GREY
        child_documents_file_status.value = "لم يتم اختيار ملف وثائق الطفل"
        child_documents_file_status.color = ft.Colors.GREY
        # Reset visibility
        monthly_fee.visible = False
        bus_fee.visible = False
        session_fee.visible = False
        monthly_sessions_count.visible = False
        diagnosis.visible = False
        tests_applied.visible = False
        training_plan.visible = False
        monthly_report.visible = False
        attendance_status.visible = False
        attended_sessions_count.visible = False
        specialist_name.visible = False
        personal_photo_btn.visible = False
        birth_certificate_btn.visible = False
        father_id_card_btn.visible = False
        test_documents_btn.visible = False
        tests_applied_file_btn.visible = False
        training_plan_file_btn.visible = False
        monthly_report_file_btn.visible = False
        child_documents_file_btn.visible = False
        personal_photo_status.visible = False
        birth_certificate_status.visible = False
        father_id_card_status.visible = False
        test_documents_status.visible = False
        tests_applied_file_status.visible = False
        training_plan_file_status.visible = False
        monthly_report_file_status.visible = False
        child_documents_file_status.visible = False

    def open_add_child_dialog(e):
        page.open(add_child_dialog)

    def close_dialog():
        page.close(add_child_dialog)

    # Add child button
    add_child_btn = ft.ElevatedButton(
        "إضافة طالب جديد", icon=ft.Icons.ADD, on_click=open_add_child_dialog
    )

    return add_child_dialog, add_child_btn
