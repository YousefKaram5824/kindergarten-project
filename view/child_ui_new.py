import datetime
import os
import shutil
import flet as ft

# Local imports
from database import get_db, db_session
from DTOs.child_dto import CreateChildDTO
from models import ChildTypeEnum
from logic.child_logic import ChildService
from view.child_details_ui import show_child_details_page

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8
DELETE_BUTTON_COLOR = ft.Colors.RED_700
TABLE_BORDER_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.BLACK45)


def create_child_registration_tab(page: ft.Page, current_user=None):
    """Create and return the child registration tab"""

    # Search field for filtering childs
    def on_search_change(e):
        update_child_table(search_field.value or "")

    search_field = ft.TextField(
        label="بحث",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        hint_text="ابحث بالاسم، رقم الهاتف، وظيفة الأب، وظيفة الأم، أو الملاحظات",
        on_change=on_search_change,
        suffix_icon=ft.Icons.SEARCH,
    )

    # child table with database integration
    child_data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("الاسم")),
            ft.DataColumn(ft.Text("العمر")),
            ft.DataColumn(ft.Text("رقم التليفون")),
            ft.DataColumn(ft.Text("وظيفة الأب")),
            ft.DataColumn(ft.Text("وظيفة الأم")),
            ft.DataColumn(ft.Text("نوع الطالب")),
            ft.DataColumn(ft.Text("الإجراءات")),
        ],
        rows=[],
        border=ft.border.all(1, TABLE_BORDER_COLOR),
        border_radius=ft.border_radius.all(BORDER_RADIUS),
        vertical_lines=ft.border.BorderSide(1, TABLE_BORDER_COLOR),
        horizontal_lines=ft.border.BorderSide(1, TABLE_BORDER_COLOR),
        heading_row_color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK12),
        heading_row_height=45,
        data_row_max_height=55,
        column_spacing=20,
    )

    def update_child_table(search_query: str = ""):
        # Get childs from database using ChildService with search
        with db_session() as db:
            children_dto = ChildService.search_children(db, search_query)

            if child_data_table.rows is None:
                child_data_table.rows = []
            else:
                child_data_table.rows.clear()

            for child in children_dto:
                # Create action icons for each child
                action_icons = ft.Row(
                    [
                        # Display icon
                        ft.IconButton(
                            icon=ft.Icons.VISIBILITY,
                            icon_color=ft.Colors.BLUE,
                            tooltip="عرض",
                            on_click=lambda e, child_id=child.id: display_child(
                                child_id
                            ),
                        ),
                        # Edit icon
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=ft.Colors.ORANGE,
                            tooltip="تعديل",
                            on_click=lambda e, child_id=child.id: edit_child(child_id),
                        ),
                        # Delete icon
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            tooltip="حذف",
                            on_click=lambda e, child_id=child.id: delete_child(
                                child_id
                            ),
                        ),
                    ],
                    spacing=5,
                )

                child_data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(child.name)),
                            ft.DataCell(ft.Text(str(child.age) if child.age else "-")),
                            ft.DataCell(
                                ft.Text(
                                    child.phone_number if child.phone_number else "-"
                                )
                            ),
                            ft.DataCell(
                                ft.Text(child.father_job if child.father_job else "-")
                            ),
                            ft.DataCell(
                                ft.Text(child.mother_job if child.mother_job else "-")
                            ),
                            ft.DataCell(
                                ft.Text(
                                    child.child_type.value if child.child_type else "-"
                                )
                            ),
                            ft.DataCell(action_icons),
                        ]
                    )
                )
            page.update()

    # Action handlers for the icons
    def display_child(child_id):
        """Display child details"""
        show_child_details_page(page, child_id, current_user)

    current_edit_child_id = None

    def edit_child(child_id):
        """Edit child details"""
        nonlocal current_edit_child_id
        with db_session() as db:
            child = ChildService.get_child_by_id(db, child_id)
            if child:
                current_edit_child_id = child_id
                # Populate edit form with child data
                edit_child_name.value = child.name
                edit_age_counter = child.age or 3
                edit_child_age.value = str(edit_age_counter)
                edit_birth_date.value = (
                    child.birth_date.strftime("%Y-%m-%d") if child.birth_date else ""
                )
                edit_selected_date = child.birth_date if child.birth_date else None
                edit_phone.value = child.phone_number or ""
                edit_dad_job.value = child.father_job or ""
                edit_mum_job.value = child.mother_job or ""
                edit_problem.value = child.notes or ""
                edit_additional_notes.value = ""
                edit_photo_path = child.child_image
                if edit_photo_path and os.path.exists(edit_photo_path):
                    edit_photo_preview.src = edit_photo_path
                    edit_photo_preview.visible = True
                    edit_photo_status.value = (
                        f"تم اختيار: {os.path.basename(edit_photo_path)}"
                    )
                    edit_photo_status.color = ft.Colors.GREEN
                else:
                    edit_photo_preview.src = ""
                    edit_photo_preview.visible = False
                    edit_photo_status.value = "لم يتم اختيار صورة"
                    edit_photo_status.color = ft.Colors.GREY
                edit_selected_child_type = child.child_type or ChildTypeEnum.FULL_DAY
                edit_child_type_dropdown.value = edit_selected_child_type.name

                # Open edit dialog
                page.open(edit_child_dialog)

    def delete_child(child_id):
        """Delete child"""
        with db_session() as db:
            child = ChildService.get_child_by_id(db, child_id)
            if child:
                # Show confirmation dialog
                def confirm_delete(e):
                    try:
                        success = ChildService.delete_child(db, child_id)
                        if success:
                            update_child_table()
                            snackbar = ft.SnackBar(
                                content=ft.Text(f"تم حذف الطالب: {child.name}"),
                                bgcolor=ft.Colors.GREEN,
                                duration=3000,
                            )
                        else:
                            snackbar = ft.SnackBar(
                                content=ft.Text("فشل في حذف الطالب"),
                                bgcolor=ft.Colors.RED,
                                duration=3000,
                            )
                        page.overlay.append(snackbar)
                        page.update()
                        snackbar.open = True
                        snackbar.update()
                        page.update()
                        page.close(dialog)
                    except Exception as ex:
                        snackbar = ft.SnackBar(
                            content=ft.Text(f"خطأ في الحذف: {str(ex)}"),
                            bgcolor=ft.Colors.RED,
                            duration=3000,
                        )
                        page.overlay.append(snackbar)
                        page.update()
                        snackbar.open = True
                        snackbar.update()
                        page.update()

                def cancel_delete(e):
                    page.close(dialog)

                dialog = ft.AlertDialog(
                    title=ft.Text("تأكيد الحذف"),
                    content=ft.Text(f"هل تريد حذف الطالب {child.name}؟"),
                    actions=[
                        ft.TextButton("نعم", on_click=confirm_delete),
                        ft.TextButton("لا", on_click=cancel_delete),
                    ],
                )
                page.open(dialog)

    # Form fields
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
        width=200,
    )
    selected_date = None
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
    selected_child_type = ChildTypeEnum.FULL_DAY
    child_type_dropdown = ft.Dropdown(
        label="نوع الطالب",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        value=ChildTypeEnum.FULL_DAY.name,
        options=[
            ft.dropdown.Option(
                key=ChildTypeEnum.FULL_DAY.name, text=ChildTypeEnum.FULL_DAY.value
            ),
            ft.dropdown.Option(
                key=ChildTypeEnum.SESSIONS.name, text=ChildTypeEnum.SESSIONS.value
            ),
        ],
        on_change=lambda e: update_selected_child_type(e),
    )

    def update_selected_child_type(e):
        nonlocal selected_child_type
        if e.control.value == ChildTypeEnum.FULL_DAY.name:
            selected_child_type = ChildTypeEnum.FULL_DAY
        elif e.control.value == ChildTypeEnum.SESSIONS.name:
            selected_child_type = ChildTypeEnum.SESSIONS

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

    def pick_photo(e):
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الطالب",
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
                phone,
                dad_job,
                mum_job,
                child_type_dropdown,
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
            ],
            width=400,
            height=550,
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

    def handle_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal photo_path
        if e.files:
            # Create child_photos directory if it doesn't exist
            photos_dir = "child_photos"
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)

            # Copy the file to child_photos directory
            uploaded_file = e.files[0]
            file_extension = os.path.splitext(uploaded_file.name)[1]
            new_filename = (
                f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
            )
            photo_path = os.path.join(photos_dir, new_filename)

            # Copy the file
            shutil.copy2(uploaded_file.path, photo_path)

            # Update UI
            photo_preview.src = photo_path
            photo_preview.visible = True
            photo_status.value = f"تم اختيار: {uploaded_file.name}"
            photo_status.color = ft.Colors.GREEN
            page.update()

    # Photo upload functionality
    file_picker = ft.FilePicker(on_result=handle_file_picker_result)
    page.overlay.append(file_picker)

    # Edit form fields (similar to add form)
    edit_child_name = ft.TextField(
        label="اسم الطالب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_child_age = ft.TextField(
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
    edit_age_counter = 3
    edit_birth_date = ft.TextField(
        label="تاريخ الميلاد",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=200,
    )
    edit_selected_date = None
    edit_phone = ft.TextField(
        label="رقم التليفون",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_dad_job = ft.TextField(
        label="وظيفة الأب",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_mum_job = ft.TextField(
        label="وظيفة الأم",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_problem = ft.TextField(
        label="المشكلة",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_additional_notes = ft.TextField(
        label="ملاحظات إضافية",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_photo_path = None
    edit_photo_preview = ft.Image(
        src="", width=100, height=100, fit=ft.ImageFit.COVER, visible=False
    )
    edit_photo_status = ft.Text(
        "لم يتم اختيار صورة",
        size=12,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.RIGHT,
    )

    # Edit child type dropdown
    edit_selected_child_type = ChildTypeEnum.FULL_DAY
    edit_child_type_dropdown = ft.Dropdown(
        label="نوع الطالب",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        value=ChildTypeEnum.FULL_DAY.name,
        options=[
            ft.dropdown.Option(
                key=ChildTypeEnum.FULL_DAY.name, text=ChildTypeEnum.FULL_DAY.value
            ),
            ft.dropdown.Option(
                key=ChildTypeEnum.SESSIONS.name, text=ChildTypeEnum.SESSIONS.value
            ),
        ],
        on_change=lambda e: update_edit_selected_child_type(e),
    )

    def update_edit_selected_child_type(e):
        nonlocal edit_selected_child_type
        if e.control.value == ChildTypeEnum.FULL_DAY.name:
            edit_selected_child_type = ChildTypeEnum.FULL_DAY
        elif e.control.value == ChildTypeEnum.SESSIONS.name:
            edit_selected_child_type = ChildTypeEnum.SESSIONS

    def edit_increment_age(e):
        nonlocal edit_age_counter
        edit_age_counter += 1
        edit_child_age.value = str(edit_age_counter)
        page.update()

    def edit_decrement_age(e):
        nonlocal edit_age_counter
        if edit_age_counter > 0:
            edit_age_counter -= 1
            edit_child_age.value = str(edit_age_counter)
        page.update()

    edit_age_controls = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.REMOVE,
                on_click=edit_decrement_age,
                icon_size=20,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.BLUE,
                    shape=ft.RoundedRectangleBorder(
                        radius=ft.border_radius.all(BORDER_RADIUS)
                    ),
                ),
            ),
            edit_child_age,
            ft.IconButton(
                icon=ft.Icons.ADD,
                on_click=edit_increment_age,
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

    def edit_handle_date_picker(e):
        nonlocal edit_selected_date
        if e.control.value:
            edit_selected_date = e.control.value
            edit_birth_date.value = edit_selected_date.strftime("%Y-%m-%d")
            page.update()

    def edit_open_date_picker(e):
        page.open(edit_date_picker)

    edit_date_picker_btn = ft.ElevatedButton(
        "اختر التاريخ", on_click=edit_open_date_picker
    )

    def edit_pick_photo(e):
        edit_file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الطالب",
        )

    edit_photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الطالب", icon=ft.Icons.UPLOAD_FILE, on_click=edit_pick_photo
    )

    # Edit child Dialog
    edit_child_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("تعديل بيانات الطالب", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                edit_child_name,
                ft.Container(
                    ft.Text("العمر:", size=16, text_align=ft.TextAlign.RIGHT),
                    padding=ft.padding.only(bottom=5),
                ),
                edit_age_controls,
                ft.Row(
                    [edit_date_picker_btn, edit_birth_date],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                edit_phone,
                edit_dad_job,
                edit_mum_job,
                edit_child_type_dropdown,
                edit_problem,
                edit_additional_notes,
                ft.Container(
                    ft.Text(
                        "صورة الطالب:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    padding=ft.padding.only(top=10, bottom=5),
                ),
                edit_photo_upload_btn,
                ft.Container(
                    ft.Row([edit_photo_preview], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(top=5, bottom=5),
                ),
                ft.Container(edit_photo_status, padding=ft.padding.only(bottom=10)),
            ],
            width=400,
            height=550,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: close_edit_dialog()),
            ft.TextButton("حفظ", on_click=lambda e: save_edit_child()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Edit Date picker
    edit_date_picker = ft.DatePicker(
        on_change=edit_handle_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(edit_date_picker)

    def edit_handle_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal edit_photo_path
        if e.files:
            # Create child_photos directory if it doesn't exist
            photos_dir = "child_photos"
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)

            # Copy the file to child_photos directory
            uploaded_file = e.files[0]
            file_extension = os.path.splitext(uploaded_file.name)[1]
            new_filename = (
                f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
            )
            edit_photo_path = os.path.join(photos_dir, new_filename)

            # Copy the file
            shutil.copy2(uploaded_file.path, edit_photo_path)

            # Update UI
            edit_photo_preview.src = edit_photo_path
            edit_photo_preview.visible = True
            edit_photo_status.value = f"تم اختيار: {uploaded_file.name}"
            edit_photo_status.color = ft.Colors.GREEN
            page.update()

    # Edit Photo upload functionality
    edit_file_picker = ft.FilePicker(on_result=edit_handle_file_picker_result)
    page.overlay.append(edit_file_picker)

    def save_edit_child():
        nonlocal current_edit_child_id
        if not current_edit_child_id:
            show_error("لم يتم العثور على الطالب المراد تعديله!")
            return

        # Validate required fields
        if not edit_child_name.value:
            show_error("يجب إدخال اسم الطالب!")
            return

        if not edit_child_age.value or int(edit_child_age.value) <= 0:
            show_error("يجب إدخال عمر صحيح للطالب!")
            return

        if not edit_birth_date.value:
            show_error("يجب اختيار تاريخ الميلاد!")
            return

        # Create child DTO with updated data
        child_data = CreateChildDTO(
            name=str(edit_child_name.value),
            age=int(edit_child_age.value),
            birth_date=datetime.datetime.strptime(
                edit_birth_date.value, "%Y-%m-%d"
            ).date(),
            phone_number=str(edit_phone.value) if edit_phone.value else None,
            father_job=str(edit_dad_job.value) if edit_dad_job.value else None,
            mother_job=str(edit_mum_job.value) if edit_mum_job.value else None,
            notes=str(edit_problem.value) if edit_problem.value else None,
            child_image=edit_photo_path,
            created_at=datetime.datetime.now(),  # Keep original created_at or update?
            child_type=edit_selected_child_type,
        )

        # Update child in database using ChildService
        with db_session() as db:
            try:
                child_dto = ChildService.update_child(
                    db, current_edit_child_id, child_data
                )

                if child_dto:
                    # Close dialog and refresh table
                    close_edit_dialog()
                    update_child_table()
                    show_success("تم تعديل بيانات الطالب بنجاح!")
                else:
                    show_error("فشل في تعديل بيانات الطالب!")
            except Exception as ex:
                show_error(f"خطأ في تعديل بيانات الطالب: {str(ex)}")

    def close_edit_dialog():
        page.close(edit_child_dialog)

    def add_child():
        # Validate required fields
        if not child_name.value:
            show_error("يجب إدخال اسم الطالب!")
            return

        if not child_age.value or int(child_age.value) <= 0:
            show_error("يجب إدخال عمر صحيح للطالب!")
            return

        if not birth_date.value:
            show_error("يجب اختيار تاريخ الميلاد!")
            return

        # Create child DTO with current timestamp
        child_data = CreateChildDTO(
            name=str(child_name.value),
            age=int(child_age.value),
            birth_date=datetime.datetime.strptime(birth_date.value, "%Y-%m-%d").date(),
            phone_number=str(phone.value),
            father_job=str(dad_job.value),
            mother_job=str(mum_job.value),
            notes=str(problem.value),
            child_image=photo_path,
            created_at=datetime.datetime.now(),
            child_type=selected_child_type,
        )

        # Add child to database with photo path using ChildService
        with db_session() as db:
            try:
                child_dto = ChildService.create_child(db, child_data)

                if child_dto:
                    # Clear form and close dialog
                    reset_form()
                    close_dialog()

                    # Refresh child table
                    update_child_table()

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
        nonlocal age_counter, photo_path, selected_date, selected_child_type
        child_name.value = ""
        age_counter = 3
        child_age.value = "3"
        birth_date.value = ""
        selected_date = None
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
        selected_child_type = ChildTypeEnum.FULL_DAY
        child_type_dropdown.value = ChildTypeEnum.FULL_DAY.name

    def open_add_child_dialog(e):
        page.open(add_child_dialog)

    def close_dialog():
        page.close(add_child_dialog)

    # Add child button
    add_child_btn = ft.ElevatedButton(
        "إضافة طالب جديد", icon=ft.Icons.ADD, on_click=open_add_child_dialog
    )

    # Load initial child data
    update_child_table()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("إدارة الطلاب", size=24, weight=ft.FontWeight.BOLD),
                    add_child_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.Row(
                [
                    search_field,
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Text("الطلاب المسجلين:", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([child_data_table], scroll=ft.ScrollMode.AUTO),
                height=500,
                padding=10,
                alignment=ft.alignment.center,
                margin=10,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
