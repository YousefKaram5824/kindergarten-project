import datetime
import os
import shutil
import flet as ft
from typing import Optional
from view.message_handlers import show_success_message, show_error_message

# Local imports
from database import db_session
from logic.training_tool_logic import TrainingToolService
from DTOs.training_tool_dto import CreateTrainingToolDTO
from view.add_inventory_dialog import create_add_inventory_dialog

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8
DELETE_BUTTON_COLOR = ft.Colors.RED_700
TABLE_BORDER_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.BLACK45)


def create_inventory_tab(page: ft.Page):
    """Create and return the inventory management tab"""

    # Search field for filtering tools
    def on_search_change(e):
        search_query = search_field.value or ""
        update_inventory_table(search_query)

    search_field = ft.TextField(
        label="بحث",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        hint_text="ابحث بالاسم، رقم الأداة، القسم، أو الملاحظات",
        on_change=on_search_change,
        suffix_icon=ft.Icons.SEARCH,
    )

    # DataTable for inventory - matching child page style
    inventory_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("اسم الأداة")),
            ft.DataColumn(ft.Text("رقم الأداة")),
            ft.DataColumn(ft.Text("القسم")),
            ft.DataColumn(ft.Text("تاريخ الشراء")),
            ft.DataColumn(ft.Text("ملاحظات")),
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

    def update_inventory_table(search_query: Optional[str] = None):
        with db_session() as db:
            if search_query:
                tools = TrainingToolService.search_tools(db, search_query)
            else:
                tools = TrainingToolService.get_all_tools(db)
            if inventory_table.rows is None:
                inventory_table.rows = []
            else:
                inventory_table.rows.clear()
            for tool in tools:
                # Action icons for each tool
                action_icons = ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=ft.Colors.ORANGE,
                            tooltip="تعديل",
                            on_click=lambda e, tool_id=tool.id: open_edit_dialog(
                                tool_id
                            ),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=DELETE_BUTTON_COLOR,
                            tooltip="حذف",
                            on_click=lambda e, tool_id=tool.id: confirm_delete_tool(
                                tool_id
                            ),
                        ),
                    ],
                    spacing=5,
                )
                inventory_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(tool.id))),
                            ft.DataCell(ft.Text(tool.tool_name or "")),
                            ft.DataCell(ft.Text(tool.tool_number or "")),
                            ft.DataCell(ft.Text(tool.department or "")),
                            ft.DataCell(
                                ft.Text(
                                    str(tool.purchase_date)
                                    if tool.purchase_date
                                    else ""
                                )
                            ),
                            ft.DataCell(ft.Text(tool.notes or "")),
                            ft.DataCell(action_icons),
                        ]
                    )
                )
        page.update()

    # Create add inventory dialog and button
    add_inventory_dialog, open_add_inventory_dialog = create_add_inventory_dialog(page, update_inventory_table)

    # Add inventory button
    add_inventory_btn = ft.ElevatedButton(
        "إضافة أداة جديدة", icon=ft.Icons.ADD, on_click=open_add_inventory_dialog
    )

    # Edit dialog variables
    current_edit_tool_id = None
    edit_item_name = ft.TextField(
        label="اسم الأداة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_item_number = ft.TextField(
        label="رقم الأداة",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_department = ft.TextField(
        label="القسم",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_purchase_date = ft.TextField(
        label="تاريخ الشراء",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        width=210,
    )
    edit_selected_purchase_date = None
    edit_notes = ft.TextField(
        label="ملاحظات",
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

    def handle_edit_date_picker(e):
        nonlocal edit_selected_purchase_date
        if e.control.value:
            edit_selected_purchase_date = e.control.value
            edit_purchase_date.value = edit_selected_purchase_date.strftime("%Y-%m-%d")
            page.update()

    def open_edit_date_picker(e):
        page.open(edit_date_picker)

    edit_date_picker_btn = ft.ElevatedButton(
        "اختر التاريخ", on_click=open_edit_date_picker
    )

    def pick_edit_photo(e):
        edit_file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png", "gif"],
            dialog_title="اختر صورة الأداة",
        )

    edit_photo_upload_btn = ft.ElevatedButton(
        "رفع صورة الأداة", icon=ft.Icons.UPLOAD_FILE, on_click=pick_edit_photo
    )

    def handle_edit_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal edit_photo_path
        if e.files:
            # Create tool_photos directory if it doesn't exist
            photos_dir = "tool_photos"
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)

            # Copy the file to tool_photos directory
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

    # Edit file picker
    edit_file_picker = ft.FilePicker(on_result=handle_edit_file_picker_result)
    page.overlay.append(edit_file_picker)

    # Edit date picker
    edit_date_picker = ft.DatePicker(
        on_change=handle_edit_date_picker,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
    )
    page.overlay.append(edit_date_picker)

    # Edit inventory Dialog
    edit_inventory_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("تعديل الأداة", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                edit_item_name,
                edit_item_number,
                edit_department,
                ft.Row(
                    [edit_date_picker_btn, edit_purchase_date],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                edit_notes,
                ft.Container(
                    ft.Text(
                        "صورة الأداة:",
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
            height=500,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: close_edit_dialog()),
            ft.TextButton("حفظ", on_click=lambda e: update_inventory_item()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_edit_dialog(tool_id):
        nonlocal current_edit_tool_id
        with db_session() as db:
            tool = TrainingToolService.get_tool(db, tool_id)
            if tool:
                current_edit_tool_id = tool_id
                edit_item_name.value = tool.tool_name or ""
                edit_item_number.value = tool.tool_number or ""
                edit_department.value = tool.department or ""
                edit_purchase_date.value = (
                    str(tool.purchase_date) if tool.purchase_date else ""
                )
                edit_notes.value = tool.notes or ""
                edit_photo_path = tool.tool_image
                if edit_photo_path and os.path.exists(edit_photo_path):
                    edit_photo_preview.src = edit_photo_path
                    edit_photo_preview.visible = True
                    edit_photo_status.value = "صورة موجودة"
                    edit_photo_status.color = ft.Colors.GREEN
                else:
                    edit_photo_preview.visible = False
                    edit_photo_status.value = "لم يتم اختيار صورة"
                    edit_photo_status.color = ft.Colors.GREY
                page.open(edit_inventory_dialog)

    def close_edit_dialog():
        page.close(edit_inventory_dialog)

    def update_inventory_item():
        # This would need the tool_id - we'll need to store it when opening edit dialog
        # For now, just close the dialog
        close_edit_dialog()
        update_inventory_table()
        show_success_message(page, "تم تحديث الأداة بنجاح!")

    def confirm_delete_tool(tool_id):
        with db_session() as db:
            tool = TrainingToolService.get_tool(db, tool_id)
            if tool:

                def confirm_delete(e):
                    try:
                        success = TrainingToolService.delete_tool(db, tool_id)
                        if success:
                            update_inventory_table()
                            show_success_message(page, f"تم حذف الأداة: {tool.tool_name}")
                        else:
                            show_error_message(page, "فشل في حذف الأداة")
                        page.close(dialog)
                    except Exception as ex:
                        show_error_message(page, f"خطأ في الحذف: {str(ex)}")

                def cancel_delete(e):
                    page.close(dialog)

                dialog = ft.AlertDialog(
                    title=ft.Text("تأكيد الحذف"),
                    content=ft.Text(f"هل تريد حذف الأداة {tool.tool_name}؟"),
                    actions=[
                        ft.TextButton("نعم", on_click=confirm_delete),
                        ft.TextButton("لا", on_click=cancel_delete),
                    ],
                )
                page.open(dialog)

    # Load initial data
    update_inventory_table()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("إدارة المخزون", size=24, weight=ft.FontWeight.BOLD),
                    add_inventory_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.Row(
                [
                    search_field,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            ft.Text("عناصر المخزون:", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([inventory_table], scroll=ft.ScrollMode.AUTO),
                height=500,
                padding=10,
                alignment=ft.alignment.center,
                margin=10,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
