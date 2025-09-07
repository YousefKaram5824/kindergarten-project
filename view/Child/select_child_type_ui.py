import flet as ft
import os
import shutil
import datetime

# Local imports
from database import db_session
from models import ChildTypeEnum
from logic.child_logic import ChildService
from DTOs.child_dto import UpdateChildDTO
from DTOs.full_day_program_dto import CreateFullDayProgramDTO
from DTOs.individual_session_dto import CreateIndividualSessionDTO
from logic.full_day_program_logic import FullDayProgramService
from logic.individual_session_logic import IndividualSessionService


def open_type_selection_dialog(page: ft.Page, child_id: int, update_callback=None):
    """Open the type selection dialog for a child"""

    # Fields for both types
    diagnosis_field = ft.TextField(
        label="التشخيص",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    monthly_fee_field = ft.TextField(
        label="قيمة الاشتراك الشهري",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9.]", replacement_string=""
        ),
    )
    bus_fee_field = ft.TextField(
        label="قيمة اشتراك الباص",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9.]", replacement_string=""
        ),
    )
    attendance_status_field = ft.TextField(
        label="حالة الحضور",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    session_fee_field = ft.TextField(
        label="قيمة الجلسة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9.]", replacement_string=""
        ),
    )
    monthly_sessions_count_field = ft.TextField(
        label="عدد الجلسات الشهرية",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
    )
    attended_sessions_count_field = ft.TextField(
        label="عدد الجلسات المحضورة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
    )
    specialist_name_field = ft.TextField(
        label="اسم المتخصص",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    notes_field = ft.TextField(
        label="ملاحظات",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    # File fields
    birth_certificate_path = None
    father_id_card_path = None
    tests_applied_file_path = None
    training_plan_file_path = None
    monthly_report_file_path = None

    birth_certificate_status = ft.Text(
        "لم يتم اختيار ملف", size=12, color=ft.Colors.GREY
    )
    father_id_card_status = ft.Text("لم يتم اختيار ملف", size=12, color=ft.Colors.GREY)
    tests_applied_status = ft.Text("لم يتم اختيار ملف", size=12, color=ft.Colors.GREY)
    training_plan_status = ft.Text("لم يتم اختيار ملف", size=12, color=ft.Colors.GREY)
    monthly_report_status = ft.Text("لم يتم اختيار ملف", size=12, color=ft.Colors.GREY)

    current_file_type = None

    def pick_birth_certificate(e):
        nonlocal current_file_type
        current_file_type = "birth_certificate"
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
            dialog_title="اختر شهادة الميلاد",
        )

    def pick_father_id_card(e):
        nonlocal current_file_type
        current_file_type = "father_id_card"
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
            dialog_title="اختر بطاقة الأب",
        )

    def pick_tests_applied(e):
        nonlocal current_file_type
        current_file_type = "tests_applied"
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
            dialog_title="اختر ملف الاختبارات المطبقة",
        )

    def pick_training_plan(e):
        nonlocal current_file_type
        current_file_type = "training_plan"
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
            dialog_title="اختر ملف الخطة التدريبية",
        )

    def pick_monthly_report(e):
        nonlocal current_file_type
        current_file_type = "monthly_report"
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
            dialog_title="اختر ملف التقرير الشهري",
        )

    birth_certificate_btn = ft.ElevatedButton(
        "رفع شهادة الميلاد", icon=ft.Icons.UPLOAD_FILE, on_click=pick_birth_certificate
    )
    father_id_card_btn = ft.ElevatedButton(
        "رفع بطاقة الأب", icon=ft.Icons.UPLOAD_FILE, on_click=pick_father_id_card
    )
    tests_applied_btn = ft.ElevatedButton(
        "رفع ملف الاختبارات", icon=ft.Icons.UPLOAD_FILE, on_click=pick_tests_applied
    )
    training_plan_btn = ft.ElevatedButton(
        "رفع ملف الخطة التدريبية",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=pick_training_plan,
    )
    monthly_report_btn = ft.ElevatedButton(
        "رفع ملف التقرير الشهري",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=pick_monthly_report,
    )

    def handle_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal birth_certificate_path, father_id_card_path, tests_applied_file_path, training_plan_file_path, monthly_report_file_path
        if e.files and current_file_type:
            uploaded_file = e.files[0]
            dir_name = "child_documents"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{timestamp}_{uploaded_file.name}"
            file_path = os.path.join(dir_name, new_filename)
            shutil.copy2(uploaded_file.path, file_path)

            if current_file_type == "birth_certificate":
                birth_certificate_path = file_path
                birth_certificate_status.value = f"تم اختيار: {uploaded_file.name}"
                birth_certificate_status.color = ft.Colors.GREEN
            elif current_file_type == "father_id_card":
                father_id_card_path = file_path
                father_id_card_status.value = f"تم اختيار: {uploaded_file.name}"
                father_id_card_status.color = ft.Colors.GREEN
            elif current_file_type == "tests_applied":
                tests_applied_file_path = file_path
                tests_applied_status.value = f"تم اختيار: {uploaded_file.name}"
                tests_applied_status.color = ft.Colors.GREEN
            elif current_file_type == "training_plan":
                training_plan_file_path = file_path
                training_plan_status.value = f"تم اختيار: {uploaded_file.name}"
                training_plan_status.color = ft.Colors.GREEN
            elif current_file_type == "monthly_report":
                monthly_report_file_path = file_path
                monthly_report_status.value = f"تم اختيار: {uploaded_file.name}"
                monthly_report_status.color = ft.Colors.GREEN
            page.update()

    file_picker = ft.FilePicker(on_result=handle_file_picker_result)
    page.overlay.append(file_picker)

    # Fields containers
    common_fields = ft.Column(
        [
            diagnosis_field,
            notes_field,
            ft.Container(
                ft.Text("شهادة الميلاد:", text_align=ft.TextAlign.RIGHT),
                padding=ft.padding.only(bottom=5),
            ),
            birth_certificate_btn,
            birth_certificate_status,
            ft.Container(
                ft.Text("بطاقة الأب:", text_align=ft.TextAlign.RIGHT),
                padding=ft.padding.only(bottom=5),
            ),
            father_id_card_btn,
            father_id_card_status,
            ft.Container(
                ft.Text("ملف الاختبارات المطبقة:", text_align=ft.TextAlign.RIGHT),
                padding=ft.padding.only(bottom=5),
            ),
            tests_applied_btn,
            tests_applied_status,
            ft.Container(
                ft.Text("ملف التقرير الشهري:", text_align=ft.TextAlign.RIGHT),
                padding=ft.padding.only(bottom=5),
            ),
            monthly_report_btn,
            monthly_report_status,
        ],
        visible=True,
    )

    full_day_fields = ft.Column(
        [
            monthly_fee_field,
            bus_fee_field,
            attendance_status_field,
            ft.Container(
                ft.Text("ملف الخطة التدريبية:", text_align=ft.TextAlign.RIGHT),
                padding=ft.padding.only(bottom=5),
            ),
            training_plan_btn,
            training_plan_status,
        ],
        visible=False,
    )

    sessions_fields = ft.Column(
        [
            session_fee_field,
            monthly_sessions_count_field,
            attended_sessions_count_field,
            specialist_name_field,
        ],
        visible=False,
    )

    def update_field_visibility(selected_type):
        if selected_type == ChildTypeEnum.FULL_DAY.name:
            full_day_fields.visible = True
            sessions_fields.visible = False
        elif selected_type == ChildTypeEnum.SESSIONS.name:
            full_day_fields.visible = False
            sessions_fields.visible = True
        else:
            full_day_fields.visible = False
            sessions_fields.visible = False
        page.update()

    type_dropdown = ft.Dropdown(
        label="اختر نوع الطالب",
        options=[
            ft.dropdown.Option(
                ChildTypeEnum.FULL_DAY.name, ChildTypeEnum.FULL_DAY.value
            ),
            ft.dropdown.Option(
                ChildTypeEnum.SESSIONS.name, ChildTypeEnum.SESSIONS.value
            ),
        ],
        on_change=lambda e: update_field_visibility(e.control.value),
    )

    def save_type(e):
        selected_type = type_dropdown.value
        if selected_type:
            with db_session() as db:
                update_dto = UpdateChildDTO(child_type=ChildTypeEnum[selected_type])
                success = ChildService.update_child(db, child_id, update_dto)
                if success:
                    # Create the program/session
                    if selected_type == ChildTypeEnum.FULL_DAY.name:
                        program_data = CreateFullDayProgramDTO(
                            diagnosis=diagnosis_field.value or None,
                            monthly_fee=(
                                float(monthly_fee_field.value)
                                if monthly_fee_field.value
                                else None
                            ),
                            bus_fee=(
                                float(bus_fee_field.value)
                                if bus_fee_field.value
                                else None
                            ),
                            attendance_status=attendance_status_field.value or None,
                            notes=notes_field.value or None,
                            birth_certificate=birth_certificate_path,
                            father_id_card=father_id_card_path,
                            tests_applied_file=tests_applied_file_path,
                            training_plan_file=training_plan_file_path,
                            monthly_report_file=monthly_report_file_path,
                        )
                        FullDayProgramService.create_program(db, program_data, child_id)
                    elif selected_type == ChildTypeEnum.SESSIONS.name:
                        session_data = CreateIndividualSessionDTO(
                            diagnosis=diagnosis_field.value or None,
                            session_fee=(
                                float(session_fee_field.value)
                                if session_fee_field.value
                                else None
                            ),
                            monthly_sessions_count=(
                                int(monthly_sessions_count_field.value)
                                if monthly_sessions_count_field.value
                                else None
                            ),
                            attended_sessions_count=(
                                int(attended_sessions_count_field.value)
                                if attended_sessions_count_field.value
                                else None
                            ),
                            specialist_name=specialist_name_field.value or None,
                            notes=notes_field.value or None,
                            birth_certificate=birth_certificate_path,
                            father_id_card=father_id_card_path,
                            tests_applied_file=tests_applied_file_path,
                            monthly_report_file=monthly_report_file_path,
                        )
                        IndividualSessionService.create_session(
                            db, session_data, child_id
                        )

                    if update_callback:
                        update_callback()

                    snackbar = ft.SnackBar(
                        content=ft.Text("تم تحديث نوع الطالب وإنشاء البرنامج"),
                        bgcolor=ft.Colors.GREEN,
                        duration=3000,
                    )
                    page.overlay.append(snackbar)
                    page.update()
                    snackbar.open = True
                    snackbar.update()
        page.close(dialog)

    dialog = ft.AlertDialog(
        title=ft.Text("اختيار نوع الطالب وإدخال البيانات"),
        content=ft.Column(
            [
                type_dropdown,
                common_fields,
                full_day_fields,
                sessions_fields,
            ],
            scroll=ft.ScrollMode.AUTO,
            height=600,
        ),
        actions=[
            ft.TextButton("حفظ", on_click=save_type),
            ft.TextButton("إلغاء", on_click=lambda e: page.close(dialog)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.open(dialog)
