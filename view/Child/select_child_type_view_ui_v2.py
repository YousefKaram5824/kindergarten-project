import flet as ft
import os
import shutil
import datetime
from pathlib import Path
from typing import Optional, Any

# Local imports
from database import db_session
from database import get_db
from logic.child_logic import ChildService
from models import ChildTypeEnum
from DTOs.child_dto import UpdateChildDTO
from DTOs.full_day_program_dto import CreateFullDayProgramDTO, UpdateFullDayProgramDTO
from DTOs.individual_session_dto import (
    CreateIndividualSessionDTO,
    UpdateIndividualSessionDTO,
)
from logic.full_day_program_logic import FullDayProgramService
from logic.individual_session_logic import IndividualSessionService


def create_child_details_view_v2(
    page: ft.Page, child_id: int, update_callback=None, is_edit=False, current_user=None
):
    """Create and return the child details view - simplified version with improved compatibility"""

    # Global variables for file paths
    file_paths: dict[str, Optional[str]] = {
        "birth_certificate": None,
        "father_id_card": None,
        "tests_applied": None,
        "training_plan": None,
        "monthly_report": None,
    }

    # Temporary file storage
    _selected_files: dict[str, Optional[Any]] = {
        "birth_certificate": None,
        "father_id_card": None,
        "tests_applied": None,
        "training_plan": None,
        "monthly_report": None,
    }

    current_file_type = None

    # Load child data
    child_data = None
    try:
        with db_session() as db:
            child_data = ChildService.get_child_by_id(db, child_id)
    except Exception as e:
        print(f"Error loading child data: {e}")
        child_data = None

    # Title
    child_name = child_data.name if child_data is not None else "غير محدد"
    title = ft.Text(
        (
            f"تعديل بيانات الطفل: {child_name}"
            if is_edit
            else f"عرض بيانات الطفل: {child_name}"
        ),
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.RIGHT,
        color=ft.Colors.BLUE_800,
    )

    def go_back(e=None):
        if update_callback:
            update_callback()
        # Clear the page and reload the children table view
        page.clean()
        from view.Child.child_ui import (
            create_child_registration_tab,
            create_back_button,
        )

        page.add(create_back_button(page, current_user))
        page.add(create_child_registration_tab(page, current_user))
        page.update()

    # Back button
    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK, tooltip="العودة", on_click=go_back
    )

    # Header
    header = ft.Row(
        [back_button, ft.Container(expand=True), title],
        alignment=ft.MainAxisAlignment.START,
    )

    # Create text fields with improved RTL support
    def create_text_field(
        label, width=300, multiline=False, is_number=False, read_only=None
    ):
        if read_only is None:
            read_only = not is_edit
        return ft.TextField(
            label=label,
            text_align=ft.TextAlign.RIGHT,
            width=width,
            multiline=multiline,
            min_lines=3 if multiline else 1,
            max_lines=5 if multiline else 1,
            read_only=read_only,
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.WHITE if not read_only else ft.Colors.GREY_50,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600,
            input_filter=(
                ft.InputFilter(
                    allow=True, regex_string=r"[0-9.]", replacement_string=""
                )
                if is_number and not read_only
                else None
            ),
        )

    # Basic info fields (read-only)
    name_field = create_text_field("اسم الطفل", 300, read_only=True)
    department_field = create_text_field("القسم", 300, read_only=True)
    age_field = create_text_field("العمر", 150, read_only=True)

    if child_data:
        name_field.value = child_data.name or ""
        department_field.value = getattr(child_data, "department", "") or ""
        age_field.value = str(child_data.age) if child_data.age else ""

    # Type dropdown
    type_dropdown = ft.Dropdown(
        label="نوع الطفل",
        options=[
            ft.dropdown.Option(
                ChildTypeEnum.FULL_DAY.name, ChildTypeEnum.FULL_DAY.value
            ),
            ft.dropdown.Option(
                ChildTypeEnum.SESSIONS.name, ChildTypeEnum.SESSIONS.value
            ),
        ],
        on_change=lambda e: update_field_visibility(e.control.value),
        text_align=ft.TextAlign.RIGHT,
        width=300,
        disabled=not is_edit,
        border_radius=10,
        filled=True,
        bgcolor=ft.Colors.WHITE,
        border_color=ft.Colors.BLUE_300,
        value=(
            child_data.child_type.name
            if child_data and child_data.child_type != ChildTypeEnum.NONE
            else None
        ),
    )

    # Common fields
    diagnosis_field = create_text_field("التشخيص", 400, True)
    notes_field = create_text_field("ملاحظات", 500, True)

    # Full day program fields
    monthly_fee_field = create_text_field("قيمة الاشتراك الشهري", 280, False, True)
    bus_fee_field = create_text_field("قيمة اشتراك الباص", 280, False, True)
    attendance_status_field = create_text_field("حالة الحضور", 280)

    # Sessions fields
    session_fee_field = create_text_field("قيمة الجلسة", 280, False, True)
    monthly_sessions_count_field = create_text_field(
        "عدد الجلسات الشهرية", 280, False, True
    )
    attended_sessions_count_field = create_text_field(
        "عدد الجلسات المحضورة", 280, False, True
    )
    specialist_name_field = create_text_field("اسم المتخصص", 280)

    def show_snackbar(message, color):
        snackbar = ft.SnackBar(
            content=ft.Text(message, text_align=ft.TextAlign.RIGHT),
            bgcolor=color,
            duration=3000,
        )
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    # File handling functions
    def get_file_type_name(file_type):
        names = {
            "birth_certificate": "شهادة الميلاد",
            "father_id_card": "بطاقة الأب",
            "tests_applied": "الاختبارات المطبقة",
            "training_plan": "الخطة التدريبية",
            "monthly_report": "التقرير الشهري",
        }
        return names.get(file_type, "الملف")

    def pick_file(file_type):
        nonlocal current_file_type
        current_file_type = file_type
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
            dialog_title=f"اختر {get_file_type_name(file_type)}",
        )

    def handle_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal current_file_type

        if e.files and current_file_type is not None:
            try:
                # Store the selected file temporarily without copying
                _selected_files[current_file_type] = e.files[0]

                # Update preview with temporary file path (original path)
                update_file_preview(current_file_type, e.files[0].path)
                show_snackbar(
                    f"تم اختيار {get_file_type_name(current_file_type)}",
                    ft.Colors.GREEN,
                )

            except Exception as ex:
                show_snackbar(f"خطأ في اختيار الملف: {str(ex)}", ft.Colors.RED)

    # File picker
    file_picker = ft.FilePicker(on_result=handle_file_picker_result)
    page.overlay.append(file_picker)

    def view_file(file_type):
        file_path = file_paths.get(file_type)
        if file_path and os.path.exists(file_path):
            try:
                import subprocess
                import platform

                if platform.system() == "Windows":
                    os.startfile(file_path)
                elif platform.system() == "Darwin":
                    subprocess.call(["open", file_path])
                else:
                    subprocess.call(["xdg-open", file_path])
            except Exception as ex:
                show_snackbar(f"خطأ في فتح الملف: {str(ex)}", ft.Colors.RED)
        else:
            show_snackbar("الملف غير موجود", ft.Colors.ORANGE)

    def delete_file(file_type):
        def confirm_delete(e):
            file_paths[file_type] = None
            update_file_preview(file_type, None)
            page.close(confirm_dialog)
            show_snackbar(f"تم حذف {get_file_type_name(file_type)}", ft.Colors.ORANGE)

        confirm_dialog = ft.AlertDialog(
            title=ft.Text("تأكيد الحذف", text_align=ft.TextAlign.RIGHT),
            content=ft.Text(
                f"هل تريد حذف {get_file_type_name(file_type)}؟",
                text_align=ft.TextAlign.RIGHT,
            ),
            actions=[
                ft.TextButton("نعم", on_click=confirm_delete),
                ft.TextButton("لا", on_click=lambda e: page.close(confirm_dialog)),
            ],
        )
        page.open(confirm_dialog)

    # File preview function with improved path handling
    def create_file_preview_card(file_type, title, icon):
        preview_container = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=50, color=ft.Colors.GREY_400),
                    ft.Text("لا يوجد ملف", size=12, color=ft.Colors.GREY_600),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=200,
            height=120,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.GREY_50,
        )

        actions = []
        actions.append(
            ft.IconButton(
                icon=ft.Icons.VISIBILITY,
                tooltip="عرض",
                on_click=lambda e: view_file(file_type),
                visible=False,
            )
        )

        if is_edit:
            actions.extend(
                [
                    ft.IconButton(
                        icon=ft.Icons.UPLOAD_FILE,
                        tooltip="رفع ملف",
                        on_click=lambda e: pick_file(file_type),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        tooltip="حذف",
                        on_click=lambda e: delete_file(file_type),
                        visible=False,
                    ),
                ]
            )

        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            title,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        preview_container,
                        ft.Row(actions, alignment=ft.MainAxisAlignment.CENTER),
                    ]
                ),
                padding=15,
            ),
            width=230,
        )

        return card, preview_container, actions

    # Create file cards
    birth_cert_card, birth_cert_preview, birth_cert_actions = create_file_preview_card(
        "birth_certificate", "شهادة الميلاد", ft.Icons.ASSIGNMENT
    )
    father_id_card, father_id_preview, father_id_actions = create_file_preview_card(
        "father_id_card", "بطاقة الأب", ft.Icons.BADGE
    )
    tests_applied_card, tests_preview, tests_actions = create_file_preview_card(
        "tests_applied", "ملف الاختبارات", ft.Icons.QUIZ
    )
    training_plan_card, training_preview, training_actions = create_file_preview_card(
        "training_plan", "الخطة التدريبية", ft.Icons.SCHOOL
    )
    monthly_report_card, monthly_preview, monthly_actions = create_file_preview_card(
        "monthly_report", "التقرير الشهري", ft.Icons.ASSESSMENT
    )

    def update_file_preview(file_type, file_path):
        preview_map = {
            "birth_certificate": (birth_cert_preview, birth_cert_actions),
            "father_id_card": (father_id_preview, father_id_actions),
            "tests_applied": (tests_preview, tests_actions),
            "training_plan": (training_preview, training_actions),
            "monthly_report": (monthly_preview, monthly_actions),
        }

        if file_type not in preview_map:
            return

        preview_container, actions_list = preview_map[file_type]

        if file_path:
            # Fix for relative paths: convert to absolute if needed
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)

        if file_path and os.path.exists(file_path):
            filename = os.path.basename(file_path)
            file_ext = Path(file_path).suffix.lower()

            if file_ext in [".jpg", ".jpeg", ".png"]:
                preview_content = ft.Image(
                    src=file_path,
                    width=180,
                    height=100,
                    fit=ft.ImageFit.COVER,
                    border_radius=5,
                )
            else:
                preview_content = ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.DESCRIPTION, size=40, color=ft.Colors.BLUE_500
                        ),
                        ft.Text(
                            filename[:20] + "..." if len(filename) > 20 else filename,
                            size=10,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )

            preview_container.content = preview_content
            preview_container.border = ft.border.all(2, ft.Colors.GREEN_400)
            preview_container.bgcolor = ft.Colors.WHITE

            # Show buttons
            for action in actions_list:
                if hasattr(action, "icon"):
                    if action.icon in [ft.Icons.VISIBILITY, ft.Icons.DELETE]:
                        action.visible = True
        else:
            # Reset to default
            icon_map = {
                "birth_certificate": ft.Icons.ASSIGNMENT,
                "father_id_card": ft.Icons.BADGE,
                "tests_applied": ft.Icons.QUIZ,
                "training_plan": ft.Icons.SCHOOL,
                "monthly_report": ft.Icons.ASSESSMENT,
            }

            preview_container.content = ft.Column(
                [
                    ft.Icon(
                        icon_map.get(file_type, ft.Icons.FILE_PRESENT),
                        size=50,
                        color=ft.Colors.GREY_400,
                    ),
                    ft.Text("لا يوجد ملف", size=12, color=ft.Colors.GREY_600),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            preview_container.border = ft.border.all(1, ft.Colors.GREY_300)
            preview_container.bgcolor = ft.Colors.GREY_50

            # Hide buttons
            for action in actions_list:
                if hasattr(action, "icon"):
                    if action.icon in [ft.Icons.VISIBILITY, ft.Icons.DELETE]:
                        action.visible = False

        page.update()

    # Create sections
    basic_info_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "البيانات الأساسية للطفل",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.INDIGO_700,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        name_field,
                        ft.Container(width=20),
                        age_field,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=20),
                ft.Row(
                    [
                        department_field,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.INDIGO_50,
        border_radius=10,
        margin=ft.margin.only(bottom=20),
    )

    common_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "البيانات العامة",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        type_dropdown,
                        ft.Container(width=50),
                        diagnosis_field,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=20),
                notes_field,
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        margin=ft.margin.only(bottom=20),
    )

    full_day_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "بيانات نظام اليوم الكامل",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN_700,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        monthly_fee_field,
                        ft.Container(width=20),
                        bus_fee_field,
                        ft.Container(width=20),
                        attendance_status_field,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=20),
                ft.Text(
                    "الملفات الخاصة بالبرنامج الكامل:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row([training_plan_card], alignment=ft.MainAxisAlignment.CENTER),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.GREEN_50,
        border_radius=10,
        margin=ft.margin.only(bottom=20),
        visible=False,
    )

    sessions_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "بيانات نظام الجلسات الفردية",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ORANGE_700,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        session_fee_field,
                        ft.Container(width=20),
                        monthly_sessions_count_field,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=20),
                ft.Row(
                    [
                        attended_sessions_count_field,
                        ft.Container(width=20),
                        specialist_name_field,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.ORANGE_50,
        border_radius=10,
        margin=ft.margin.only(bottom=20),
        visible=False,
    )

    files_section = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "الملفات والمستندات",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.PURPLE_700,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        birth_cert_card,
                        father_id_card,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                ),
                ft.Container(height=20),
                ft.Row(
                    [tests_applied_card, monthly_report_card],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                ),
            ]
        ),
        padding=20,
        bgcolor=ft.Colors.PURPLE_50,
        border_radius=10,
        margin=ft.margin.only(bottom=20),
    )

    def update_field_visibility(selected_type):
        if selected_type == ChildTypeEnum.FULL_DAY.name:
            full_day_section.visible = True
            sessions_section.visible = False
        elif selected_type == ChildTypeEnum.SESSIONS.name:
            full_day_section.visible = False
            sessions_section.visible = True
        else:
            full_day_section.visible = False
            sessions_section.visible = False
        page.update()

    # Load existing data
    def load_existing_data():
        if not child_data:
            return

        try:
            with db_session() as db:
                if child_data.child_type == ChildTypeEnum.FULL_DAY:
                    program = FullDayProgramService.get_program_by_child_id(
                        db, child_id
                    )
                    if program:
                        diagnosis_field.value = program.diagnosis or ""
                        monthly_fee_field.value = (
                            str(program.monthly_fee) if program.monthly_fee else ""
                        )
                        bus_fee_field.value = (
                            str(program.bus_fee) if program.bus_fee else ""
                        )
                        attendance_status_field.value = program.attendance_status or ""
                        notes_field.value = program.notes or ""

                        # Load file paths
                        file_paths["birth_certificate"] = program.birth_certificate
                        file_paths["father_id_card"] = program.father_id_card
                        file_paths["tests_applied"] = program.tests_applied_file
                        file_paths["training_plan"] = program.training_plan_file
                        file_paths["monthly_report"] = program.monthly_report_file

                        # Update file previews
                        for file_type, file_path in file_paths.items():
                            if file_path:
                                update_file_preview(file_type, file_path)

                        update_field_visibility(ChildTypeEnum.FULL_DAY.name)

                elif child_data.child_type == ChildTypeEnum.SESSIONS:
                    session = IndividualSessionService.get_session_by_child_id(
                        db, child_id
                    )
                    if session:
                        diagnosis_field.value = session.diagnosis or ""
                        session_fee_field.value = (
                            str(session.session_fee) if session.session_fee else ""
                        )
                        monthly_sessions_count_field.value = (
                            str(session.monthly_sessions_count)
                            if session.monthly_sessions_count
                            else ""
                        )
                        attended_sessions_count_field.value = (
                            str(session.attended_sessions_count)
                            if session.attended_sessions_count
                            else ""
                        )
                        specialist_name_field.value = session.specialist_name or ""
                        notes_field.value = session.notes or ""

                        # Load file paths
                        file_paths["birth_certificate"] = session.birth_certificate
                        file_paths["father_id_card"] = session.father_id_card
                        file_paths["tests_applied"] = session.tests_applied_file
                        file_paths["monthly_report"] = session.monthly_report_file

                        # Update file previews
                        for file_type, file_path in file_paths.items():
                            if file_path:
                                update_file_preview(file_type, file_path)

                        update_field_visibility(ChildTypeEnum.SESSIONS.name)

        except Exception as e:
            print(f"Error loading existing data: {e}")

    # Load data
    load_existing_data()

    def save_changes(e):
        selected_type = type_dropdown.value
        if not selected_type:
            show_snackbar("يرجى اختيار نوع الطفل", ft.Colors.RED)
            return

        try:
            # If a file was selected, copy it now
            if (
                current_file_type is not None
                and _selected_files.get(current_file_type) is not None
            ):
                dir_name = "child_documents"
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                selected_file = _selected_files[current_file_type]
                if selected_file:
                    new_filename = f"{timestamp}_{selected_file.name}"
                    file_path = os.path.join(dir_name, new_filename)
                    shutil.copy2(selected_file.path, file_path)
                else:
                    show_snackbar("لم يتم العثور على الملف المحدد", ft.Colors.RED)
                    return

                # Update the corresponding file path
                file_paths[current_file_type] = file_path

            with db_session() as db:
                # Update child type
                update_dto = UpdateChildDTO(child_type=ChildTypeEnum[selected_type])
                success = ChildService.update_child(db, child_id, update_dto)

                if not success:
                    show_snackbar("فشل في تحديث نوع الطفل", ft.Colors.RED)
                    return

                # Save type-specific data
                if selected_type == ChildTypeEnum.FULL_DAY.name:
                    existing_program = FullDayProgramService.get_program_by_child_id(
                        db, child_id
                    )

                    program_data = {
                        "diagnosis": diagnosis_field.value or None,
                        "monthly_fee": (
                            float(monthly_fee_field.value)
                            if monthly_fee_field.value
                            else None
                        ),
                        "bus_fee": (
                            float(bus_fee_field.value) if bus_fee_field.value else None
                        ),
                        "attendance_status": attendance_status_field.value or None,
                        "notes": notes_field.value or None,
                        "birth_certificate": file_paths["birth_certificate"],
                        "father_id_card": file_paths["father_id_card"],
                        "tests_applied_file": file_paths["tests_applied"],
                        "training_plan_file": file_paths["training_plan"],
                        "monthly_report_file": file_paths["monthly_report"],
                    }

                    if existing_program:
                        update_dto = UpdateFullDayProgramDTO(**program_data)
                        FullDayProgramService.update_program(
                            db, existing_program.id, update_dto
                        )
                    else:
                        create_dto = CreateFullDayProgramDTO(**program_data)
                        FullDayProgramService.create_program(db, create_dto, child_id)

                elif selected_type == ChildTypeEnum.SESSIONS.name:
                    existing_session = IndividualSessionService.get_session_by_child_id(
                        db, child_id
                    )

                    session_data = {
                        "diagnosis": diagnosis_field.value or None,
                        "session_fee": (
                            float(session_fee_field.value)
                            if session_fee_field.value
                            else None
                        ),
                        "monthly_sessions_count": (
                            int(monthly_sessions_count_field.value)
                            if monthly_sessions_count_field.value
                            else None
                        ),
                        "attended_sessions_count": (
                            int(attended_sessions_count_field.value)
                            if attended_sessions_count_field.value
                            else None
                        ),
                        "specialist_name": specialist_name_field.value or None,
                        "notes": notes_field.value or None,
                        "birth_certificate": file_paths["birth_certificate"],
                        "father_id_card": file_paths["father_id_card"],
                        "tests_applied_file": file_paths["tests_applied"],
                        "monthly_report_file": file_paths["monthly_report"],
                    }

                    if existing_session:
                        update_dto = UpdateIndividualSessionDTO(**session_data)
                        IndividualSessionService.update_session(
                            db, existing_session.id, update_dto
                        )
                    else:
                        create_dto = CreateIndividualSessionDTO(**session_data)
                        IndividualSessionService.create_session(
                            db, create_dto, child_id
                        )

                show_snackbar("تم حفظ البيانات بنجاح", ft.Colors.GREEN)

                if update_callback:
                    update_callback()

        except Exception as ex:
            show_snackbar(f"خطأ في حفظ البيانات: {str(ex)}", ft.Colors.RED)

    # Action buttons
    buttons = []
    if is_edit:
        buttons.append(
            ft.ElevatedButton(
                "حفظ التغييرات",
                icon=ft.Icons.SAVE,
                on_click=save_changes,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
            )
        )
    buttons.append(
        ft.ElevatedButton(
            "العودة",
            icon=ft.Icons.ARROW_BACK,
            on_click=go_back,
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE,
        )
    )

    action_buttons = ft.Row(buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    # Main content
    content = ft.Column(
        [
            header,
            basic_info_section,
            common_section,
            full_day_section,
            sessions_section,
            files_section,
            action_buttons,
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    # Set initial visibility based on child type
    if child_data and child_data.child_type and hasattr(child_data.child_type, "name"):
        update_field_visibility(child_data.child_type.name)

    return ft.Container(content=content, padding=30, expand=True)


# Compatibility functions
def open_child_details_view_v2(
    page: ft.Page, child_id: int, update_callback=None, is_edit=False, current_user=None
):
    """Open child details as a full page view"""
    page.clean()
    child_view = create_child_details_view_v2(
        page, child_id, update_callback, is_edit, current_user
    )
    page.add(child_view)
    page.update()


def open_child_edit_view_v2(
    page: ft.Page, child_id: int, update_callback=None, current_user=None
):
    """Open child details in edit mode"""
    open_child_details_view_v2(
        page, child_id, update_callback, is_edit=True, current_user=current_user
    )


def open_child_view_only_v2(
    page: ft.Page, child_id: int, update_callback=None, current_user=None
):
    """Open child details in view-only mode"""
    open_child_details_view_v2(
        page, child_id, update_callback, is_edit=False, current_user=current_user
    )
