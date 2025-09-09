import flet as ft
import os
import re
import shutil
import datetime
from pathlib import Path
from typing import Optional, Any

# Local imports
from database import db_session
from models import ChildTypeEnum
from logic.child_logic import ChildService
from DTOs.child_dto import UpdateChildDTO
from DTOs.full_day_program_dto import CreateFullDayProgramDTO, UpdateFullDayProgramDTO
from DTOs.individual_session_dto import (
    CreateIndividualSessionDTO,
    UpdateIndividualSessionDTO,
)
from logic.full_day_program_logic import FullDayProgramService
from logic.individual_session_logic import IndividualSessionService


def open_child_details_view(
    page: ft.Page, child_id: int, update_callback=None, is_edit=False
):
    """Open child details as a full page view"""

    # Clear the page first
    page.clean()

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

    # Title and header
    title = ft.Text(
        "تعديل بيانات الطالب" if is_edit else "عرض بيانات الطالب",
        size=28,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.RIGHT,
        color=ft.Colors.BLUE_900,
    )

    def go_back():
        if update_callback:
            update_callback()
        # Clear the page and reload the children table view
        page.clean()
        from view.Child.child_ui import create_child_registration_tab

        page.add(create_child_registration_tab(page))
        page.update()

    back_button = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS,
            tooltip="العودة",
            on_click=lambda e: go_back(),
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_600,
            icon_size=20,
        ),
        padding=5,
    )

    header = ft.Container(
        content=ft.Row(
            [back_button, ft.Container(expand=True), title],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.BLUE_50,
        padding=20,
        border_radius=15,
        margin=ft.margin.only(bottom=20),
    )

    # Create text fields - much simpler approach
    def create_text_field(label, width=300, multiline=False, is_number=False):
        return ft.TextField(
            label=label,
            text_align=ft.TextAlign.RIGHT,
            width=width,
            multiline=multiline,
            min_lines=2 if multiline else 1,
            max_lines=4 if multiline else 1,
            read_only=not is_edit,  # Simple boolean check
            border_radius=10,
            filled=True,
            bgcolor=ft.Colors.WHITE,
            border_color=ft.Colors.BLUE_300,
            focused_border_color=ft.Colors.BLUE_600,
            input_filter=(
                ft.InputFilter(
                    allow=True, regex_string=r"[0-9.]", replacement_string=""
                )
                if is_number and is_edit
                else None
            ),
        )

    # Create all fields
    diagnosis_field = create_text_field("التشخيص", 400, True)
    notes_field = create_text_field("ملاحظات", 500, True)

    # Full day fields
    monthly_fee_field = create_text_field("قيمة الاشتراك الشهري", 280, False, True)
    bus_fee_field = create_text_field("قيمة اشتراك الباص", 280, False, True)
    attendance_status_field = create_text_field("حالة الحضور", 280)

    # Session fields
    session_fee_field = create_text_field("قيمة الجلسة", 280, False, True)
    monthly_sessions_count_field = create_text_field(
        "عدد الجلسات الشهرية", 280, False, True
    )
    attended_sessions_count_field = create_text_field(
        "عدد الجلسات المحضورة", 280, False, True
    )
    specialist_name_field = create_text_field("اسم المتخصص", 280)

    # Type dropdown
    type_dropdown = ft.Dropdown(
        label="نوع الطالب",
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
    )

    def show_snackbar(message, color):
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=color,
            duration=4000,
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

        if e.files and current_file_type:
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

    # Simple file preview function
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
                            filename[:20] + "...",
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
    common_section = ft.Card(
        content=ft.Container(
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
                        [type_dropdown, ft.Container(width=20), diagnosis_field],
                        alignment=ft.MainAxisAlignment.END,
                        wrap=True,
                    ),
                    ft.Container(height=10),
                    notes_field,
                ]
            ),
            padding=20,
        ),
        margin=ft.margin.only(bottom=20),
    )

    full_day_section = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "بيانات البرنامج الكامل",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_700,
                    ),
                    ft.Divider(),
                    ft.Row(
                        [
                            monthly_fee_field,
                            ft.Container(width=10),
                            bus_fee_field,
                            ft.Container(width=10),
                            attendance_status_field,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                    ft.Container(height=15),
                    ft.Text("الخطة التدريبية:", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([training_plan_card], alignment=ft.MainAxisAlignment.CENTER),
                ]
            ),
            padding=20,
        ),
        margin=ft.margin.only(bottom=20),
        visible=False,
    )

    sessions_section = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "بيانات الجلسات الفردية",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ORANGE_700,
                    ),
                    ft.Divider(),
                    ft.Row(
                        [
                            session_fee_field,
                            ft.Container(width=10),
                            monthly_sessions_count_field,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        [
                            attended_sessions_count_field,
                            ft.Container(width=10),
                            specialist_name_field,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                ]
            ),
            padding=20,
        ),
        margin=ft.margin.only(bottom=20),
        visible=False,
    )

    files_section = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "الملفات والمستندات",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.PURPLE_700,
                    ),
                    ft.Divider(),
                    ft.Text("المستندات الأساسية:", size=14, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            birth_cert_card,
                            father_id_card,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                    ft.Container(height=15),
                    ft.Text(
                        "التقارير والاختبارات:", size=14, weight=ft.FontWeight.BOLD
                    ),
                    ft.Row(
                        [tests_applied_card, monthly_report_card],
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                ]
            ),
            padding=20,
        ),
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
        try:
            with db_session() as db:
                child = ChildService.get_child_by_id(db, child_id)
                if child:
                    type_dropdown.value = (
                        child.child_type.name
                        if child.child_type != ChildTypeEnum.NONE
                        else None
                    )

                    if child.child_type == ChildTypeEnum.FULL_DAY:
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
                            attendance_status_field.value = (
                                program.attendance_status or ""
                            )
                            notes_field.value = program.notes or ""

                            file_paths["birth_certificate"] = program.birth_certificate
                            file_paths["father_id_card"] = program.father_id_card
                            file_paths["tests_applied"] = program.tests_applied_file
                            file_paths["training_plan"] = program.training_plan_file
                            file_paths["monthly_report"] = program.monthly_report_file

                            # Update previews
                            for file_type, file_path in file_paths.items():
                                if file_path:
                                    update_file_preview(file_type, file_path)

                            update_field_visibility(ChildTypeEnum.FULL_DAY.name)
                            page.update()

                    elif child.child_type == ChildTypeEnum.SESSIONS:
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

                            file_paths["birth_certificate"] = session.birth_certificate
                            file_paths["father_id_card"] = session.father_id_card
                            file_paths["tests_applied"] = session.tests_applied_file
                            file_paths["monthly_report"] = session.monthly_report_file

                            # Update previews
                            for file_type, file_path in file_paths.items():
                                if file_path:
                                    update_file_preview(file_type, file_path)

                            update_field_visibility(ChildTypeEnum.SESSIONS.name)
                            page.update()

        except Exception as ex:
            show_snackbar(f"خطأ في تحميل البيانات: {str(ex)}", ft.Colors.RED)

    # Load data
    load_existing_data()

    def save_changes(e):
        selected_type = type_dropdown.value
        if not selected_type:
            show_snackbar("يرجى اختيار نوع الطالب", ft.Colors.ORANGE)
            return

        try:
            # Handle file copying for newly selected files
            for file_type, selected_file in _selected_files.items():
                if selected_file:
                    # Get child's name from database to create folder
                    with db_session() as db:
                        child = ChildService.get_child_by_id(db, child_id)
                        if child:
                            child_name_str = child.name.strip()
                            # Sanitize the folder name (replace spaces and special chars with underscores)
                            folder_name = re.sub(r"[^\w\-_\.]", "_", child_name_str)
                            child_folder = os.path.join("child_documents", folder_name)
                            if not os.path.exists(child_folder):
                                os.makedirs(child_folder)

                            # Generate unique filename
                            timestamp = datetime.datetime.now().strftime(
                                "%Y%m%d_%H%M%S"
                            )
                            file_extension = Path(selected_file.name).suffix
                            new_filename = f"{file_type}_{timestamp}{file_extension}"
                            file_path = os.path.join(child_folder, new_filename)

                            # Copy file
                            shutil.copy2(selected_file.path, file_path)

                            # Update file path
                            file_paths[file_type] = file_path

                            # Clear the temporary selection
                            _selected_files[file_type] = None

            with db_session() as db:
                # Update child type
                update_dto = UpdateChildDTO(child_type=ChildTypeEnum[selected_type])
                success = ChildService.update_child(db, child_id, update_dto)

                if success:
                    if selected_type == ChildTypeEnum.FULL_DAY.name:
                        existing_program = (
                            FullDayProgramService.get_program_by_child_id(db, child_id)
                        )

                        program_data_dict = {
                            "diagnosis": diagnosis_field.value or None,
                            "monthly_fee": (
                                float(monthly_fee_field.value)
                                if monthly_fee_field.value
                                else None
                            ),
                            "bus_fee": (
                                float(bus_fee_field.value)
                                if bus_fee_field.value
                                else None
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
                            program_data = UpdateFullDayProgramDTO(**program_data_dict)
                            FullDayProgramService.update_program(
                                db, existing_program.id, program_data
                            )
                        else:
                            program_data = CreateFullDayProgramDTO(**program_data_dict)
                            FullDayProgramService.create_program(
                                db, program_data, child_id
                            )

                    elif selected_type == ChildTypeEnum.SESSIONS.name:
                        existing_session = (
                            IndividualSessionService.get_session_by_child_id(
                                db, child_id
                            )
                        )

                        session_data_dict = {
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
                            session_data = UpdateIndividualSessionDTO(
                                **session_data_dict
                            )
                            IndividualSessionService.update_session(
                                db, existing_session.id, session_data
                            )
                        else:
                            session_data = CreateIndividualSessionDTO(
                                **session_data_dict
                            )
                            IndividualSessionService.create_session(
                                db, session_data, child_id
                            )

                    show_snackbar("تم حفظ البيانات بنجاح! ✅", ft.Colors.GREEN)

        except Exception as ex:
            show_snackbar(f"خطأ في حفظ البيانات: {str(ex)}", ft.Colors.RED)

    # Action buttons
    buttons = []
    if is_edit:
        buttons.append(
            ft.ElevatedButton(
                "💾 حفظ التغييرات",
                on_click=save_changes,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                height=50,
                width=150,
            )
        )

    buttons.append(
        ft.ElevatedButton(
            "🔙 العودة",
            on_click=lambda e: go_back(),
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            height=50,
            width=150,
        )
    )

    action_buttons = ft.Row(buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    # Main content
    content = ft.Column(
        [
            header,
            common_section,
            full_day_section,
            sessions_section,
            files_section,
            action_buttons,
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    main_container = ft.Container(content=content, padding=30, expand=True)

    # Add to page
    page.add(main_container)
    page.update()


# Alternative function names for compatibility
def open_type_selection_dialog(
    page: ft.Page, child_id: int, update_callback=None, is_edit=True
):
    """Compatibility function"""
    open_child_details_view(page, child_id, update_callback, is_edit)


def open_child_edit_view(page: ft.Page, child_id: int, update_callback=None):
    """Open child details in edit mode"""
    open_child_details_view(page, child_id, update_callback, is_edit=True)


def open_child_view_only(page: ft.Page, child_id: int, update_callback=None):
    """Open child details in view-only mode"""
    open_child_details_view(page, child_id, update_callback, is_edit=False)
