import flet as ft
import os
import shutil
import datetime
from pathlib import Path

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


class ChildDetailsView:
    def __init__(
        self, page: ft.Page, child_id: int, update_callback=None, is_edit=False
    ):
        self.page = page
        self.child_id = child_id
        self.update_callback = update_callback
        self.is_edit = is_edit
        self.current_file_type = None

        # File paths
        self.birth_certificate_path = None
        self.father_id_card_path = None
        self.tests_applied_file_path = None
        self.training_plan_file_path = None
        self.monthly_report_file_path = None

        self.init_components()

    def init_components(self):
        # Title
        self.title = ft.Text(
            "تعديل بيانات الطالب" if self.is_edit else "عرض بيانات الطالب",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.RIGHT,
            color=ft.Colors.BLUE_800,
        )

        # Back button
        self.back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK, tooltip="العودة", on_click=self.go_back
        )

        # Header
        self.header = ft.Row(
            [self.back_button, ft.Container(expand=True), self.title],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # Form fields
        self.init_form_fields()

        # File picker
        self.file_picker = ft.FilePicker(on_result=self.handle_file_picker_result)
        self.page.overlay.append(self.file_picker)

        # Load existing data if editing
        if self.is_edit:
            self.load_existing_data()

    def init_form_fields(self):
        # Type dropdown
        self.type_dropdown = ft.Dropdown(
            label="نوع الطالب",
            options=[
                ft.dropdown.Option(
                    ChildTypeEnum.FULL_DAY.name, ChildTypeEnum.FULL_DAY.value
                ),
                ft.dropdown.Option(
                    ChildTypeEnum.SESSIONS.name, ChildTypeEnum.SESSIONS.value
                ),
            ],
            on_change=self.on_type_change,
            text_align=ft.TextAlign.RIGHT,
            width=300,
            disabled=not self.is_edit,
        )

        # Common fields
        self.diagnosis_field = ft.TextField(
            label="التشخيص",
            text_align=ft.TextAlign.RIGHT,
            width=400,
            read_only=not self.is_edit,
            multiline=True,
        )

        self.notes_field = ft.TextField(
            label="ملاحظات",
            multiline=True,
            text_align=ft.TextAlign.RIGHT,
            width=400,
            min_lines=3,
            max_lines=5,
            read_only=not self.is_edit,
        )

        # Full day program fields
        self.monthly_fee_field = ft.TextField(
            label="قيمة الاشتراك الشهري",
            text_align=ft.TextAlign.RIGHT,
            width=300,
            read_only=not self.is_edit,
            input_filter=(
                ft.InputFilter(
                    allow=True, regex_string=r"[0-9.]", replacement_string=""
                )
                if self.is_edit
                else None
            ),
        )

        self.bus_fee_field = ft.TextField(
            label="قيمة اشتراك الباص",
            text_align=ft.TextAlign.RIGHT,
            width=300,
            read_only=not self.is_edit,
            input_filter=(
                ft.InputFilter(
                    allow=True, regex_string=r"[0-9.]", replacement_string=""
                )
                if self.is_edit
                else None
            ),
        )

        self.attendance_status_field = ft.TextField(
            label="حالة الحضور",
            text_align=ft.TextAlign.RIGHT,
            width=300,
            read_only=not self.is_edit,
        )

        # Sessions fields
        self.session_fee_field = ft.TextField(
            label="قيمة الجلسة",
            text_align=ft.TextAlign.RIGHT,
            width=300,
            read_only=not self.is_edit,
            input_filter=(
                ft.InputFilter(
                    allow=True, regex_string=r"[0-9.]", replacement_string=""
                )
                if self.is_edit
                else None
            ),
        )

        self.monthly_sessions_count_field = ft.TextField(
            label="عدد الجلسات الشهرية",
            text_align=ft.TextAlign.RIGHT,
            width=300,
            read_only=not self.is_edit,
            input_filter=(
                ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string="")
                if self.is_edit
                else None
            ),
        )

        self.attended_sessions_count_field = ft.TextField(
            label="عدد الجلسات المحضورة",
            text_align=ft.TextAlign.RIGHT,
            width=300,
            read_only=not self.is_edit,
            input_filter=(
                ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string="")
                if self.is_edit
                else None
            ),
        )

        self.specialist_name_field = ft.TextField(
            label="اسم المتخصص",
            text_align=ft.TextAlign.RIGHT,
            width=300,
            read_only=not self.is_edit,
        )

        # File components
        self.init_file_components()

    def init_file_components(self):
        # File cards
        self.birth_certificate_card = self.create_file_card(
            "شهادة الميلاد", ft.Icons.ASSIGNMENT, "birth_certificate"
        )

        self.father_id_card_card = self.create_file_card(
            "بطاقة الأب", ft.Icons.BADGE, "father_id_card"
        )

        self.tests_applied_card = self.create_file_card(
            "ملف الاختبارات المطبقة", ft.Icons.QUIZ, "tests_applied"
        )

        self.training_plan_card = self.create_file_card(
            "ملف الخطة التدريبية", ft.Icons.SCHOOL, "training_plan"
        )

        self.monthly_report_card = self.create_file_card(
            "ملف التقرير الشهري", ft.Icons.ASSESSMENT, "monthly_report"
        )

    def create_file_card(self, title, icon, file_type):
        # File preview container
        file_preview = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=50, color=ft.Colors.GREY_400),
                    ft.Text("لا يوجد ملف", size=12, color=ft.Colors.GREY_600),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=200,
            height=150,
            border=ft.border.all(2, ft.Colors.GREY_300),
            border_radius=10,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.GREY_50,
        )

        # Action buttons
        actions = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.VISIBILITY,
                    tooltip="عرض الملف",
                    on_click=lambda e: self.view_file(file_type),
                    visible=False,
                ),
                ft.IconButton(
                    icon=ft.Icons.DOWNLOAD,
                    tooltip="تحميل الملف",
                    on_click=lambda e: self.download_file(file_type),
                    visible=False,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        if self.is_edit:
            actions.controls.append(
                ft.IconButton(
                    icon=ft.Icons.UPLOAD_FILE,
                    tooltip="رفع ملف جديد",
                    on_click=lambda e: self.pick_file(file_type),
                )
            )
            actions.controls.append(
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="حذف الملف",
                    on_click=lambda e: self.delete_file(file_type),
                    visible=False,
                )
            )

        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            title,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Divider(height=10),
                        file_preview,
                        actions,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=15,
            ),
            elevation=3,
            width=230,
        )

        # Store references for easy access
        setattr(self, f"{file_type}_preview", file_preview)
        setattr(self, f"{file_type}_actions", actions)

        return card

    def create_layout(self):
        # Common fields section
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
                            self.type_dropdown,
                            ft.Container(width=50),
                            self.diagnosis_field,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Container(height=20),
                    self.notes_field,
                ]
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            margin=ft.margin.only(bottom=20),
        )

        # Type-specific fields section
        self.full_day_section = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "بيانات البرنامج الكامل",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_700,
                    ),
                    ft.Divider(),
                    ft.Row(
                        [
                            self.monthly_fee_field,
                            ft.Container(width=20),
                            self.bus_fee_field,
                            ft.Container(width=20),
                            self.attendance_status_field,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "الملفات الخاصة بالبرنامج الكامل:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Row(
                        [self.training_plan_card], alignment=ft.MainAxisAlignment.CENTER
                    ),
                ]
            ),
            padding=20,
            bgcolor=ft.Colors.GREEN_50,
            border_radius=10,
            margin=ft.margin.only(bottom=20),
            visible=False,
        )

        self.sessions_section = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "بيانات الجلسات الفردية",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ORANGE_700,
                    ),
                    ft.Divider(),
                    ft.Row(
                        [
                            self.session_fee_field,
                            ft.Container(width=20),
                            self.monthly_sessions_count_field,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        [
                            self.attended_sessions_count_field,
                            ft.Container(width=20),
                            self.specialist_name_field,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ]
            ),
            padding=20,
            bgcolor=ft.Colors.ORANGE_50,
            border_radius=10,
            margin=ft.margin.only(bottom=20),
            visible=False,
        )

        # Files section
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
                            self.birth_certificate_card,
                            self.father_id_card_card,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True,
                    ),
                    ft.Container(height=20),
                    ft.Row(
                        [self.tests_applied_card, self.monthly_report_card],
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

        # Action buttons
        buttons = []
        if self.is_edit:
            buttons.append(
                ft.ElevatedButton(
                    "حفظ التغييرات",
                    icon=ft.Icons.SAVE,
                    on_click=self.save_changes,
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE,
                )
            )
        buttons.append(
            ft.ElevatedButton(
                "العودة",
                icon=ft.Icons.ARROW_BACK,
                on_click=self.go_back,
                bgcolor=ft.Colors.GREY_600,
                color=ft.Colors.WHITE,
            )
        )

        action_buttons = ft.Row(
            buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=20
        )

        # Main content
        content = ft.Column(
            [
                self.header,
                ft.Divider(height=20),
                common_section,
                self.full_day_section,
                self.sessions_section,
                files_section,
                action_buttons,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        return ft.Container(content=content, padding=30, expand=True)

    def load_existing_data(self):
        with db_session() as db:
            child = ChildService.get_child_by_id(db, self.child_id)
            if not child:
                return

            self.type_dropdown.value = (
                child.child_type.name
                if child.child_type != ChildTypeEnum.NONE
                else None
            )

            if child.child_type == ChildTypeEnum.FULL_DAY:
                program = FullDayProgramService.get_program_by_child_id(
                    db, self.child_id
                )
                if program:
                    self.load_full_day_data(program)
                    self.update_field_visibility(ChildTypeEnum.FULL_DAY.name)

            elif child.child_type == ChildTypeEnum.SESSIONS:
                session = IndividualSessionService.get_session_by_child_id(
                    db, self.child_id
                )
                if session:
                    self.load_sessions_data(session)
                    self.update_field_visibility(ChildTypeEnum.SESSIONS.name)

    def load_full_day_data(self, program):
        self.diagnosis_field.value = program.diagnosis or ""
        self.monthly_fee_field.value = (
            str(program.monthly_fee) if program.monthly_fee else ""
        )
        self.bus_fee_field.value = str(program.bus_fee) if program.bus_fee else ""
        self.attendance_status_field.value = program.attendance_status or ""
        self.notes_field.value = program.notes or ""

        # Load file paths
        self.birth_certificate_path = program.birth_certificate
        self.father_id_card_path = program.father_id_card
        self.tests_applied_file_path = program.tests_applied_file
        self.training_plan_file_path = program.training_plan_file
        self.monthly_report_file_path = program.monthly_report_file

        # Update file previews
        self.update_file_preview("birth_certificate", program.birth_certificate)
        self.update_file_preview("father_id_card", program.father_id_card)
        self.update_file_preview("tests_applied", program.tests_applied_file)
        self.update_file_preview("training_plan", program.training_plan_file)
        self.update_file_preview("monthly_report", program.monthly_report_file)

    def load_sessions_data(self, session):
        self.diagnosis_field.value = session.diagnosis or ""
        self.session_fee_field.value = (
            str(session.session_fee) if session.session_fee else ""
        )
        self.monthly_sessions_count_field.value = (
            str(session.monthly_sessions_count)
            if session.monthly_sessions_count
            else ""
        )
        self.attended_sessions_count_field.value = (
            str(session.attended_sessions_count)
            if session.attended_sessions_count
            else ""
        )
        self.specialist_name_field.value = session.specialist_name or ""
        self.notes_field.value = session.notes or ""

        # Load file paths
        self.birth_certificate_path = session.birth_certificate
        self.father_id_card_path = session.father_id_card
        self.tests_applied_file_path = session.tests_applied_file
        self.monthly_report_file_path = session.monthly_report_file

        # Update file previews
        self.update_file_preview("birth_certificate", session.birth_certificate)
        self.update_file_preview("father_id_card", session.father_id_card)
        self.update_file_preview("tests_applied", session.tests_applied_file)
        self.update_file_preview("monthly_report", session.monthly_report_file)

    def update_file_preview(self, file_type, file_path):
        preview_container = getattr(self, f"{file_type}_preview")
        actions_row = getattr(self, f"{file_type}_actions")

        if file_path and os.path.exists(file_path):
            filename = os.path.basename(file_path)
            file_ext = Path(file_path).suffix.lower()

            # Create preview based on file type
            if file_ext in [".jpg", ".jpeg", ".png"]:
                # Image preview
                preview_content = ft.Image(
                    src=file_path,
                    width=180,
                    height=130,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=5,
                )
            elif file_ext == ".pdf":
                preview_content = ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.PICTURE_AS_PDF, size=60, color=ft.Colors.RED_400
                        ),
                        ft.Text(
                            filename,
                            size=10,
                            text_align=ft.TextAlign.CENTER,
                            max_lines=2,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            else:
                preview_content = ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.DESCRIPTION, size=60, color=ft.Colors.BLUE_400
                        ),
                        ft.Text(
                            filename,
                            size=10,
                            text_align=ft.TextAlign.CENTER,
                            max_lines=2,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )

            preview_container.content = preview_content
            preview_container.bgcolor = ft.Colors.WHITE
            preview_container.border = ft.border.all(2, ft.Colors.GREEN_300)

            # Show action buttons
            for control in actions_row.controls:
                if control.icon in [ft.Icons.VISIBILITY, ft.Icons.DOWNLOAD]:
                    control.visible = True
                elif control.icon == ft.Icons.DELETE and self.is_edit:
                    control.visible = True
        else:
            # No file - show default
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
            preview_container.bgcolor = ft.Colors.GREY_50
            preview_container.border = ft.border.all(2, ft.Colors.GREY_300)

            # Hide view/download buttons
            for control in actions_row.controls:
                if control.icon in [
                    ft.Icons.VISIBILITY,
                    ft.Icons.DOWNLOAD,
                    ft.Icons.DELETE,
                ]:
                    control.visible = False

        self.page.update()

    def on_type_change(self, e):
        self.update_field_visibility(e.control.value)

    def update_field_visibility(self, selected_type):
        if selected_type == ChildTypeEnum.FULL_DAY.name:
            self.full_day_section.visible = True
            self.sessions_section.visible = False
        elif selected_type == ChildTypeEnum.SESSIONS.name:
            self.full_day_section.visible = False
            self.sessions_section.visible = True
        else:
            self.full_day_section.visible = False
            self.sessions_section.visible = False
        self.page.update()

    def pick_file(self, file_type):
        self.current_file_type = file_type
        self.file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
            dialog_title=f"اختر ملف {self.get_file_type_name(file_type)}",
        )

    def get_file_type_name(self, file_type):
        names = {
            "birth_certificate": "شهادة الميلاد",
            "father_id_card": "بطاقة الأب",
            "tests_applied": "الاختبارات المطبقة",
            "training_plan": "الخطة التدريبية",
            "monthly_report": "التقرير الشهري",
        }
        return names.get(file_type, "الملف")

    def handle_file_picker_result(self, e: ft.FilePickerResultEvent):
        if e.files and self.current_file_type:
            try:
                # Store the selected file temporarily without copying
                self._selected_file = e.files[0]

                # Update preview with temporary file path (original path)
                self.update_file_preview(
                    self.current_file_type, self._selected_file.path
                )
                self.show_snackbar(
                    f"تم اختيار {self.get_file_type_name(self.current_file_type)}",
                    ft.Colors.GREEN,
                )
            except Exception as ex:
                self.show_snackbar(f"خطأ في اختيار الملف: {str(ex)}", ft.Colors.RED)

    def view_file(self, file_type):
        file_path = getattr(self, f"{file_type}_path")
        if file_path and os.path.exists(file_path):
            # Open file with default system application
            import subprocess
            import platform

            try:
                if platform.system() == "Windows":
                    os.startfile(file_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.call(["open", file_path])
                else:  # Linux
                    subprocess.call(["xdg-open", file_path])
            except Exception as ex:
                self.show_snackbar(f"خطأ في فتح الملف: {str(ex)}", ft.Colors.RED)

    def download_file(self, file_type):
        file_path = getattr(self, f"{file_type}_path")
        if file_path and os.path.exists(file_path):
            # In a real application, you might want to save to Downloads folder
            self.show_snackbar("تم فتح الملف للتحميل", ft.Colors.BLUE)
            self.view_file(file_type)  # For now, just open the file

    def delete_file(self, file_type):
        def confirm_delete(e):
            setattr(self, f"{file_type}_path", None)
            self.update_file_preview(file_type, None)
            self.page.close(confirm_dialog)
            self.show_snackbar(
                f"تم حذف {self.get_file_type_name(file_type)}", ft.Colors.ORANGE
            )

        confirm_dialog = ft.AlertDialog(
            title=ft.Text("تأكيد الحذف"),
            content=ft.Text(f"هل تريد حذف {self.get_file_type_name(file_type)}؟"),
            actions=[
                ft.TextButton("نعم", on_click=confirm_delete),
                ft.TextButton("لا", on_click=lambda e: self.page.close(confirm_dialog)),
            ],
        )
        self.page.open(confirm_dialog)

    def save_changes(self, e):
        selected_type = self.type_dropdown.value
        if not selected_type:
            self.show_snackbar("يرجى اختيار نوع الطالب", ft.Colors.RED)
            return

        try:
            # If a file was selected, copy it now
            if (
                hasattr(self, "_selected_file")
                and self._selected_file
                and self.current_file_type
            ):
                dir_name = "child_documents"
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{timestamp}_{self._selected_file.name}"
                file_path = os.path.join(dir_name, new_filename)
                shutil.copy2(self._selected_file.path, file_path)

                # Update the corresponding file path
                setattr(self, f"{self.current_file_type}_path", file_path)

            with db_session() as db:
                # Update child type
                update_dto = UpdateChildDTO(child_type=ChildTypeEnum[selected_type])
                success = ChildService.update_child(db, self.child_id, update_dto)

                if not success:
                    self.show_snackbar("فشل في تحديث نوع الطالب", ft.Colors.RED)
                    return

                # Save type-specific data
                if selected_type == ChildTypeEnum.FULL_DAY.name:
                    self.save_full_day_program(db)
                elif selected_type == ChildTypeEnum.SESSIONS.name:
                    self.save_individual_session(db)

                self.show_snackbar("تم حفظ البيانات بنجاح", ft.Colors.GREEN)

                if self.update_callback:
                    self.update_callback()

        except Exception as ex:
            self.show_snackbar(f"خطأ في حفظ البيانات: {str(ex)}", ft.Colors.RED)

    def save_full_day_program(self, db):
        existing_program = FullDayProgramService.get_program_by_child_id(
            db, self.child_id
        )

        program_data = {
            "diagnosis": self.diagnosis_field.value or None,
            "monthly_fee": (
                float(self.monthly_fee_field.value)
                if self.monthly_fee_field.value
                else None
            ),
            "bus_fee": (
                float(self.bus_fee_field.value) if self.bus_fee_field.value else None
            ),
            "attendance_status": self.attendance_status_field.value or None,
            "notes": self.notes_field.value or None,
            "birth_certificate": self.birth_certificate_path,
            "father_id_card": self.father_id_card_path,
            "tests_applied_file": self.tests_applied_file_path,
            "training_plan_file": self.training_plan_file_path,
            "monthly_report_file": self.monthly_report_file_path,
        }

        if existing_program:
            update_dto = UpdateFullDayProgramDTO(**program_data)
            FullDayProgramService.update_program(db, existing_program.id, update_dto)
        else:
            create_dto = CreateFullDayProgramDTO(**program_data)
            FullDayProgramService.create_program(db, create_dto, self.child_id)

    def save_individual_session(self, db):
        existing_session = IndividualSessionService.get_session_by_child_id(
            db, self.child_id
        )

        session_data = {
            "diagnosis": self.diagnosis_field.value or None,
            "session_fee": (
                float(self.session_fee_field.value)
                if self.session_fee_field.value
                else None
            ),
            "monthly_sessions_count": (
                int(self.monthly_sessions_count_field.value)
                if self.monthly_sessions_count_field.value
                else None
            ),
            "attended_sessions_count": (
                int(self.attended_sessions_count_field.value)
                if self.attended_sessions_count_field.value
                else None
            ),
            "specialist_name": self.specialist_name_field.value or None,
            "notes": self.notes_field.value or None,
            "birth_certificate": self.birth_certificate_path,
            "father_id_card": self.father_id_card_path,
            "tests_applied_file": self.tests_applied_file_path,
            "monthly_report_file": self.monthly_report_file_path,
        }

        if existing_session:
            update_dto = UpdateIndividualSessionDTO(**session_data)
            IndividualSessionService.update_session(db, existing_session.id, update_dto)
        else:
            create_dto = CreateIndividualSessionDTO(**session_data)
            IndividualSessionService.create_session(db, create_dto, self.child_id)

    def show_snackbar(self, message, color):
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            duration=3000,
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()

    def go_back(self, e=None):
        # Navigate back to the previous view
        if self.update_callback:
            self.update_callback()
        # You might want to implement proper navigation here
        # For example: self.page.go("/children") or similar


def create_child_details_view(
    page: ft.Page, child_id: int, update_callback=None, is_edit=False
):
    """
    Create and return the child details view

    Args:
        page: Flet page object
        child_id: ID of the child to display/edit
        update_callback: Callback function to call when data is updated
        is_edit: Whether the view is in edit mode or view-only mode

    Returns:
        Container with the child details view
    """
    view = ChildDetailsView(page, child_id, update_callback, is_edit)
    return view.create_layout()


# Example usage functions
def open_child_edit_view(page: ft.Page, child_id: int, update_callback=None):
    """Open child details in edit mode"""
    page.clean()
    child_view = create_child_details_view(
        page, child_id, update_callback, is_edit=True
    )
    page.add(child_view)
    page.update()


def open_child_view_only(page: ft.Page, child_id: int, update_callback=None):
    """Open child details in view-only mode"""
    page.clean()
    child_view = create_child_details_view(
        page, child_id, update_callback, is_edit=False
    )
    page.add(child_view)
    page.update()


# Alternative: Use as a route in Flet routing system
def child_details_route(page: ft.Page, child_id: int, is_edit: bool = False):
    """
    Route handler for child details page
    Usage with Flet routing:
    page.route = f"/child/{child_id}/edit" or f"/child/{child_id}/view"
    """

    def handle_back():
        page.go("/child_ui")  # Navigate back to children list

    child_view = create_child_details_view(page, child_id, handle_back, is_edit)
    return child_view
