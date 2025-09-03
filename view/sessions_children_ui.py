import datetime
import os
import shutil
import flet as ft

# Local imports
from database import db_session
from DTOs.child_dto import CreateChildDTO
from models import ChildTypeEnum
from logic.child_logic import ChildService
from view.child_details_ui import show_child_details_page
from view.add_child_ui import create_add_child_dialog
from view.edit_child_ui import create_edit_child_dialog

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8
DELETE_BUTTON_COLOR = ft.Colors.RED_700
TABLE_BORDER_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.BLACK45)


def create_sessions_children_tab(page: ft.Page, current_user=None):
    """Create and return the sessions children tab"""

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
            ft.DataColumn(ft.Text("ID")),
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
        # Get sessions children from database using ChildService
        with db_session() as db:
            if search_query:
                # If search query, get all children and filter by type and search
                all_children = ChildService.search_children(db, search_query)
                children_dto = [
                    c for c in all_children if c.child_type == ChildTypeEnum.SESSIONS
                ]
            else:
                children_dto = ChildService.get_children_by_type(
                    db, ChildTypeEnum.SESSIONS
                )

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
                            ft.DataCell(ft.Text(str(child.id))),
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

    # Edit child dialog and function from the new module
    edit_child_dialog, open_edit_dialog = create_edit_child_dialog(
        page, update_child_table
    )

    def edit_child(child_id):
        """Edit child details"""
        open_edit_dialog(child_id)

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

    # Add child dialog and button from the new module
    add_child_dialog, add_child_btn = create_add_child_dialog(page, update_child_table)

    # Load initial child data
    update_child_table()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("طلاب الجلسات", size=24, weight=ft.FontWeight.BOLD),
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
            ft.Text(
                "الطلاب المسجلين في برنامج الجلسات:", size=18, weight=ft.FontWeight.BOLD
            ),
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
