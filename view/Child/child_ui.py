import flet as ft

# Local imports
from database import db_session
from models import ChildTypeEnum
from logic.child_logic import ChildService
from DTOs.child_dto import UpdateChildDTO
from view.Child.child_details_ui import show_child_details_page
from view.Child.add_child_ui import create_add_child_dialog
from view.Child.edit_child_ui import create_edit_child_dialog


# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8
DELETE_BUTTON_COLOR = ft.Colors.RED_700
TABLE_BORDER_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.BLACK45)


def create_child_registration_tab(page: ft.Page, current_user=None):
    """Create and return the child registration tab"""

    # Current filter state
    current_filter: dict = {"search_query": "", "child_type": None}

    # Search field for filtering childs
    def on_search_change(e):
        current_filter["search_query"] = search_field.value or ""
        current_filter["child_type"] = None  # Clear type filter on search
        update_child_table()
        update_full_day_table()
        update_sessions_table()

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

    # Current table to display
    current_table = child_data_table

    # Container for the table
    table_container = ft.Container(
        content=ft.Column([current_table], scroll=ft.ScrollMode.AUTO),
        height=500,
        padding=10,
        alignment=ft.alignment.center,
        margin=10,
    )

    # Buttons for switching tables
    def show_full_day_children(e):
        current_filter["child_type"] = ChildTypeEnum.FULL_DAY
        current_filter["search_query"] = ""
        search_field.value = ""
        search_field.update()
        update_full_day_table()
        table_container.content = ft.Column(
            [full_day_data_table], scroll=ft.ScrollMode.AUTO
        )
        page.update()

    def show_sessions_children(e):
        current_filter["child_type"] = ChildTypeEnum.SESSIONS
        current_filter["search_query"] = ""
        search_field.value = ""
        search_field.update()
        update_sessions_table()
        table_container.content = ft.Column(
            [sessions_data_table], scroll=ft.ScrollMode.AUTO
        )
        page.update()

    def show_all_children(e):
        # Stay on current page, just refresh
        current_filter["child_type"] = None
        current_filter["search_query"] = ""
        search_field.value = ""
        search_field.update()
        update_child_table()
        update_full_day_table()
        update_sessions_table()
        table_container.content = ft.Column(
            [child_data_table], scroll=ft.ScrollMode.AUTO
        )
        page.update()

    full_day_button = ft.ElevatedButton(
        text=ChildTypeEnum.FULL_DAY.value,
        on_click=show_full_day_children,
    )
    sessions_button = ft.ElevatedButton(
        text=ChildTypeEnum.SESSIONS.value,
        on_click=show_sessions_children,
    )
    all_button = ft.ElevatedButton(
        text="الكل",
        on_click=show_all_children,
    )

    # Full day children table
    full_day_data_table = ft.DataTable(
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

    # Sessions children table
    sessions_data_table = ft.DataTable(
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

    def create_type_cell(child):
        if child.child_type == ChildTypeEnum.NONE:
            return ft.DataCell(
                ft.ElevatedButton(
                    text="اختر النوع",
                    on_click=lambda e, cid=child.id: open_type_dialog(cid)
                )
            )
        else:
            return ft.DataCell(ft.Text(child.child_type.value))

    def open_type_dialog(child_id):
        def save_type(e):
            selected_type = type_dropdown.value
            if selected_type:
                with db_session() as db:
                    update_dto = UpdateChildDTO(child_type=ChildTypeEnum[selected_type])
                    success = ChildService.update_child(db, child_id, update_dto)
                    if success:
                        update_all_tables()
                        snackbar = ft.SnackBar(
                            content=ft.Text("تم تحديث نوع الطالب"),
                            bgcolor=ft.Colors.GREEN,
                            duration=3000,
                        )
                        page.overlay.append(snackbar)
                        page.update()
                        snackbar.open = True
                        snackbar.update()
            page.close(dialog)

        type_dropdown = ft.Dropdown(
            label="اختر نوع الطالب",
            options=[
                ft.dropdown.Option(ChildTypeEnum.FULL_DAY.name, ChildTypeEnum.FULL_DAY.value),
                ft.dropdown.Option(ChildTypeEnum.SESSIONS.name, ChildTypeEnum.SESSIONS.value),
            ]
        )

        dialog = ft.AlertDialog(
            title=ft.Text("اختيار نوع الطالب"),
            content=type_dropdown,
            actions=[
                ft.TextButton("حفظ", on_click=save_type),
                ft.TextButton("إلغاء", on_click=lambda e: page.close(dialog)),
            ],
        )
        page.open(dialog)

    def update_child_table():
        # Get childs from database using ChildService with search and type filter
        with db_session() as db:
            if current_filter["child_type"]:
                children_dto = ChildService.get_children_by_type(
                    db, current_filter["child_type"]
                )
            elif current_filter["search_query"]:
                children_dto = ChildService.search_children(
                    db, current_filter["search_query"]
                )
            else:
                children_dto = ChildService.get_all_children(db)

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
                            create_type_cell(child),
                            ft.DataCell(action_icons),
                        ]
                    )
                )
            page.update()

    def update_full_day_table():
        # Get full day children from database
        with db_session() as db:
            if current_filter["search_query"]:
                # If search query, get all children and filter by type and search
                all_children = ChildService.search_children(
                    db, current_filter["search_query"]
                )
                children_dto = [
                    c for c in all_children if c.child_type == ChildTypeEnum.FULL_DAY
                ]
            else:
                children_dto = ChildService.get_children_by_type(
                    db, ChildTypeEnum.FULL_DAY
                )

            if full_day_data_table.rows is None:
                full_day_data_table.rows = []
            else:
                full_day_data_table.rows.clear()

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

                full_day_data_table.rows.append(
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
                            create_type_cell(child),
                            ft.DataCell(action_icons),
                        ]
                    )
                )
            page.update()

    def update_sessions_table():
        # Get sessions children from database
        with db_session() as db:
            if current_filter["search_query"]:
                # If search query, get all children and filter by type and search
                all_children = ChildService.search_children(
                    db, current_filter["search_query"]
                )
                children_dto = [
                    c for c in all_children if c.child_type == ChildTypeEnum.SESSIONS
                ]
            else:
                children_dto = ChildService.get_children_by_type(
                    db, ChildTypeEnum.SESSIONS
                )

            if sessions_data_table.rows is None:
                sessions_data_table.rows = []
            else:
                sessions_data_table.rows.clear()

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

                sessions_data_table.rows.append(
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
                            create_type_cell(child),
                            ft.DataCell(action_icons),
                        ]
                    )
                )
            page.update()

    def update_all_tables():
        update_child_table()
        update_full_day_table()
        update_sessions_table()

    # Action handlers for the icons
    def display_child(child_id):
        """Display child details"""
        show_child_details_page(page, child_id, current_user)

    # Edit child dialog and function from the new module
    edit_child_dialog, open_edit_dialog = create_edit_child_dialog(
        page, update_all_tables
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
                            update_full_day_table()
                            update_sessions_table()
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
                    ft.Text("إدارة الطلاب", size=24, weight=ft.FontWeight.BOLD),
                    add_child_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.Row(
                [
                    all_button,
                    full_day_button,
                    sessions_button,
                    search_field,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            ft.Text("الطلاب المسجلين:", size=18, weight=ft.FontWeight.BOLD),
            table_container,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def create_back_button(page, current_user):
    """Create back button to return to dashboard"""

    def back_to_dashboard(e):
        from view.dashboard_ui import show_dashboard

        show_dashboard(page, current_user)

    return ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=24,
                tooltip="العودة إلى لوحة التحكم",
                on_click=back_to_dashboard,
            ),
            ft.Text("العودة إلى لوحة التحكم", size=16),
        ]
    )
