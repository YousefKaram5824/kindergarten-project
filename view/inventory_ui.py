import flet as ft
from view.message_handlers import show_success_message, show_error_message

# Local imports
from database import db_session
from logic.tool_for_sale_logic import ToolForSaleService
from logic.book_for_sale_logic import BookForSaleService
from logic.uniform_for_sale_logic import UniformForSaleService
from view.add_tool_dialog import create_add_inventory_dialog
from view.add_book_dialog import create_add_book_dialog
from view.add_uniform_dialog import create_add_uniform_dialog

# Color constants
INPUT_BGCOLOR = ft.Colors.WHITE
BORDER_RADIUS = 8
DELETE_BUTTON_COLOR = ft.Colors.RED_700
TABLE_BORDER_COLOR = ft.Colors.with_opacity(0.5, ft.Colors.BLACK45)


def create_inventory_tab(page: ft.Page):
    """Create and return the inventory management tab"""

    # Current filter state
    current_filter: dict = {"search_query": "", "category": "all"}

    # Search field for filtering items
    def on_search_change(e):
        current_filter["search_query"] = search_field.value or ""
        update_current_table()

    search_field = ft.TextField(
        label="بحث",
        width=300,
        text_align=ft.TextAlign.RIGHT,
        hint_text="ابحث بالاسم، رقم الأداة، القسم، أو الملاحظات",
        on_change=on_search_change,
        suffix_icon=ft.Icons.SEARCH,
    )

    # Tables for each category
    inventory_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("اسم الأداة")),
            ft.DataColumn(ft.Text("رقم الأداة")),
            ft.DataColumn(ft.Text("الكمية")),
            ft.DataColumn(ft.Text("سعر الشراء")),
            ft.DataColumn(ft.Text("سعر البيع")),
            ft.DataColumn(ft.Text("المتبقي")),
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

    books_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("اسم الكتاب")),
            ft.DataColumn(ft.Text("الكمية")),
            ft.DataColumn(ft.Text("سعر الشراء")),
            ft.DataColumn(ft.Text("سعر البيع")),
            ft.DataColumn(ft.Text("المتبقي")),
            ft.DataColumn(ft.Text("ملاحظات")),
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

    uniforms_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("الكمية")),
            ft.DataColumn(ft.Text("سعر الشراء")),
            ft.DataColumn(ft.Text("سعر البيع")),
            ft.DataColumn(ft.Text("المتبقي")),
            ft.DataColumn(ft.Text("ملاحظات")),
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

    # Container for the table
    table_container = ft.Container(
        content=ft.Column([inventory_table], scroll=ft.ScrollMode.AUTO),
        height=500,
        padding=10,
        alignment=ft.alignment.center,
        margin=10,
    )

    # Update functions for each table
    def update_inventory_table():
        with db_session() as db:
            if current_filter["search_query"]:
                tools = ToolForSaleService.get_all_tools(db)
                tools = [
                    t
                    for t in tools
                    if current_filter["search_query"].lower()
                    in (t.tool_name or "").lower()
                    or current_filter["search_query"].lower()
                    in (t.tool_number or "").lower()
                    or current_filter["search_query"].lower() in (t.notes or "").lower()
                ]
            else:
                tools = ToolForSaleService.get_all_tools(db)
            if inventory_table.rows is None:
                inventory_table.rows = []
            else:
                inventory_table.rows.clear()
            for tool in tools:
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
                            ft.DataCell(
                                ft.Text(
                                    str(tool.quantity)
                                    if tool.quantity is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(tool.buy_price)
                                    if tool.buy_price is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(tool.sell_price)
                                    if tool.sell_price is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(tool.remaining)
                                    if tool.remaining is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(ft.Text(tool.notes or "")),
                            ft.DataCell(action_icons),
                        ]
                    )
                )
        page.update()

    def update_books_table():
        with db_session() as db:
            if current_filter["search_query"]:
                books = BookForSaleService.get_all_books(db)
                books = [
                    b
                    for b in books
                    if current_filter["search_query"].lower()
                    in (b.book_name or "").lower()
                ]
            else:
                books = BookForSaleService.get_all_books(db)
            if books_table.rows is None:
                books_table.rows = []
            else:
                books_table.rows.clear()
            for book in books:
                books_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(book.id))),
                            ft.DataCell(ft.Text(book.book_name or "")),
                            ft.DataCell(
                                ft.Text(
                                    str(book.quantity)
                                    if book.quantity is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(book.buy_price)
                                    if book.buy_price is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(book.sell_price)
                                    if book.sell_price is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(book.remaining)
                                    if book.remaining is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(ft.Text(book.notes or "")),
                        ]
                    )
                )
        page.update()

    def update_uniforms_table():
        with db_session() as db:
            if current_filter["search_query"]:
                uniforms = UniformForSaleService.get_all_uniforms(db)
                uniforms = [
                    u
                    for u in uniforms
                    if current_filter["search_query"].lower() in (u.notes or "").lower()
                ]
            else:
                uniforms = UniformForSaleService.get_all_uniforms(db)
            if uniforms_table.rows is None:
                uniforms_table.rows = []
            else:
                uniforms_table.rows.clear()
            for uniform in uniforms:
                uniforms_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(uniform.id))),
                            ft.DataCell(
                                ft.Text(
                                    str(uniform.quantity)
                                    if uniform.quantity is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(uniform.buy_price)
                                    if uniform.buy_price is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(uniform.sell_price)
                                    if uniform.sell_price is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    str(uniform.remaining)
                                    if uniform.remaining is not None
                                    else ""
                                )
                            ),
                            ft.DataCell(ft.Text(uniform.notes or "")),
                        ]
                    )
                )
        page.update()

    def update_current_table():
        if current_filter["category"] == "all" or current_filter["category"] == "tools":
            update_inventory_table()
            table_container.content = ft.Column(
                [inventory_table], scroll=ft.ScrollMode.AUTO
            )
        elif current_filter["category"] == "books":
            update_books_table()
            table_container.content = ft.Column(
                [books_table], scroll=ft.ScrollMode.AUTO
            )
        elif current_filter["category"] == "uniforms":
            update_uniforms_table()
            table_container.content = ft.Column(
                [uniforms_table], scroll=ft.ScrollMode.AUTO
            )
        page.update()

    # Buttons for switching tables
    def show_all(e):
        current_filter["category"] = "all"
        current_filter["search_query"] = ""
        search_field.value = ""
        search_field.update()
        update_current_table()

    def show_tools(e):
        current_filter["category"] = "tools"
        current_filter["search_query"] = ""
        search_field.value = ""
        search_field.update()
        update_current_table()

    def show_books(e):
        current_filter["category"] = "books"
        current_filter["search_query"] = ""
        search_field.value = ""
        search_field.update()
        update_current_table()

    def show_uniforms(e):
        current_filter["category"] = "uniforms"
        current_filter["search_query"] = ""
        search_field.value = ""
        search_field.update()
        update_current_table()

    all_button = ft.ElevatedButton(text="الكل", on_click=show_all)
    tools_button = ft.ElevatedButton(text="الأدوات", on_click=show_tools)
    books_button = ft.ElevatedButton(text="الكتب", on_click=show_books)
    uniforms_button = ft.ElevatedButton(text="الزي", on_click=show_uniforms)

    # Create add dialogs and buttons
    add_inventory_dialog, open_add_inventory_dialog = create_add_inventory_dialog(
        page, update_inventory_table
    )
    add_book_dialog, open_add_book_dialog = create_add_book_dialog(
        page, update_books_table
    )
    add_uniform_dialog, open_add_uniform_dialog = create_add_uniform_dialog(
        page, update_uniforms_table
    )

    # Add buttons
    add_inventory_btn = ft.ElevatedButton(
        "إضافة أداة جديدة", icon=ft.Icons.ADD, on_click=open_add_inventory_dialog
    )
    add_book_btn = ft.ElevatedButton(
        "إضافة كتاب جديد", icon=ft.Icons.ADD, on_click=open_add_book_dialog
    )
    add_uniform_btn = ft.ElevatedButton(
        "إضافة زي جديد", icon=ft.Icons.ADD, on_click=open_add_uniform_dialog
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
    edit_quantity = ft.TextField(
        label="الكمية",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_buy_price = ft.TextField(
        label="سعر الشراء",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_sell_price = ft.TextField(
        label="سعر البيع",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_remaining = ft.TextField(
        label="المتبقي",
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )
    edit_notes = ft.TextField(
        label="ملاحظات",
        multiline=True,
        text_align=ft.TextAlign.RIGHT,
        width=300,
    )

    # Edit inventory Dialog
    edit_inventory_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("تعديل الأداة", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                edit_item_name,
                edit_item_number,
                edit_quantity,
                edit_buy_price,
                edit_sell_price,
                edit_remaining,
                edit_notes,
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
            tool = ToolForSaleService.get_tool(db, tool_id)
            if tool:
                current_edit_tool_id = tool_id
                edit_item_name.value = tool.tool_name or ""
                edit_item_number.value = tool.tool_number or ""
                edit_quantity.value = (
                    str(tool.quantity) if tool.quantity is not None else ""
                )
                edit_buy_price.value = (
                    str(tool.buy_price) if tool.buy_price is not None else ""
                )
                edit_sell_price.value = (
                    str(tool.sell_price) if tool.sell_price is not None else ""
                )
                edit_remaining.value = (
                    str(tool.remaining) if tool.remaining is not None else ""
                )
                edit_notes.value = tool.notes or ""
                page.open(edit_inventory_dialog)

    def close_edit_dialog():
        page.close(edit_inventory_dialog)

    def update_inventory_item():
        if current_edit_tool_id is None:
            show_error_message(page, "لم يتم العثور على الأداة المراد تعديلها")
            return

        try:
            from DTOs.tool_for_sale_dto import CreateToolForSaleDTO

            # Parse the values
            quantity = int(edit_quantity.value) if edit_quantity.value else None
            buy_price = float(edit_buy_price.value) if edit_buy_price.value else None
            sell_price = float(edit_sell_price.value) if edit_sell_price.value else None
            remaining = int(edit_remaining.value) if edit_remaining.value else None

            tool_data = CreateToolForSaleDTO(
                tool_name=(
                    edit_item_name.value if edit_item_name.value is not None else ""
                ),
                tool_number=(
                    edit_item_number.value
                    if edit_item_number.value is not None
                    else None
                ),
                quantity=quantity,
                buy_price=buy_price,
                sell_price=sell_price,
                remaining=remaining,
                notes=edit_notes.value if edit_notes.value is not None else None,
            )

            with db_session() as db:
                updated_tool = ToolForSaleService.update_tool(
                    db,
                    current_edit_tool_id,
                    tool_data,
                )

                if updated_tool:
                    close_edit_dialog()
                    update_inventory_table()
                    show_success_message(page, "تم تحديث الأداة بنجاح!")
                else:
                    show_error_message(page, "فشل في تحديث الأداة")

        except ValueError as e:
            show_error_message(page, f"خطأ في البيانات المدخلة: {str(e)}")
        except Exception as e:
            show_error_message(page, f"خطأ غير متوقع: {str(e)}")

    def confirm_delete_tool(tool_id):
        with db_session() as db:
            tool = ToolForSaleService.get_tool(db, tool_id)
            if tool:

                def confirm_delete(e):
                    try:
                        success = ToolForSaleService.delete_tool(db, tool_id)
                        if success:
                            update_inventory_table()
                            show_success_message(
                                page, f"تم حذف الأداة: {tool.tool_name}"
                            )
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
    update_current_table()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("إدارة المخزون", size=24, weight=ft.FontWeight.BOLD),
                    add_inventory_btn,
                    add_book_btn,
                    add_uniform_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.Row(
                [
                    all_button,
                    tools_button,
                    books_button,
                    uniforms_button,
                    search_field,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
            ft.Text("عناصر المخزون:", size=18, weight=ft.FontWeight.BOLD),
            table_container,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
