import flet as ft
from datetime import date
from sqlalchemy.orm import Session
from functools import partial

from logic.training_tool_logic import TrainingToolService
from DTOs.training_tool_dto import CreateTrainingToolDTO, UpdateTrainingToolDTO


def create_custody_tab(page: ft.Page, db: Session):
    """
    UI Tab for managing custody (training tools) with enhanced design.
    """

    # ---------- Helpers ----------
    def show_message(message: str, success=True):
        """Show notification using SnackBar with enhanced styling"""
        page.snack_bar = ft.SnackBar(
            content=ft.Row(
                [
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE if success else ft.Icons.ERROR,
                        color="white",
                        size=20
                    ),
                    ft.Text(message, color="white", weight=ft.FontWeight.W_500),
                ],
                tight=True,
            ),
            bgcolor=ft.Colors.GREEN_600 if success else ft.Colors.RED_600,
            duration=3000,
            elevation=8,
        )
        page.snack_bar.open = True
        page.update()

    def load_tools(search_query: str = ""):
        try:
            tools = (
                TrainingToolService.search_tools(db, search_query)
                if search_query
                else TrainingToolService.get_all_tools(db)
            )
            update_table(tools)
        except Exception as ex:
            show_message(f"خطأ في تحميل البيانات: {ex}", success=False)

    def update_table(tools):
        data_table.rows.clear()
        for i, t in enumerate(tools):
            # تناوب الألوان للصفوف
            row_color = ft.Colors.BLUE_GREY_50 if i % 2 == 0 else ft.Colors.WHITE
            
            data_table.rows.append(
                ft.DataRow(
                    color=row_color,
                    cells=[
                        ft.DataCell(
                            ft.Container(
                                ft.Text(
                                    str(t.id), 
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_800
                                ),
                                padding=8,
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                ft.Text(
                                    t.tool_name,
                                    weight=ft.FontWeight.W_500,
                                    size=14
                                ),
                                padding=8,
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                ft.Chip(
                                    label=ft.Text(t.department or "غير محدد", size=12),
                                    bgcolor=ft.Colors.BLUE_100,
                                    color=ft.Colors.BLUE_800,
                                ) if t.department else ft.Text("غير محدد", color=ft.Colors.GREY_600),
                                padding=8,
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                ft.Text(
                                    str(t.purchase_date) if t.purchase_date else "غير محدد",
                                    color=ft.Colors.GREY_700
                                ),
                                padding=8,
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                ft.Text(
                                    t.notes[:30] + "..." if t.notes and len(t.notes) > 30 else t.notes or "لا توجد ملاحظات",
                                    color=ft.Colors.GREY_600,
                                    size=12
                                ),
                                padding=8,
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                ft.Container(
                                    ft.Image(
                                        src=t.tool_image, 
                                        width=40, 
                                        height=40,
                                        fit=ft.ImageFit.COVER,
                                        border_radius=8,
                                    ) if t.tool_image else ft.Icon(
                                        ft.Icons.BUILD_CIRCLE,
                                        color=ft.Colors.BLUE_400,
                                        size=35
                                    ),
                                    bgcolor=ft.Colors.GREY_100,
                                    border_radius=8,
                                    padding=4,
                                ),
                                padding=8,
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT_OUTLINED,
                                            tooltip="تعديل الأداة",
                                            icon_color=ft.Colors.BLUE_600,
                                            bgcolor=ft.Colors.BLUE_50,
                                            on_click=partial(open_edit_dialog, t.id),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE_OUTLINE,
                                            tooltip="حذف الأداة",
                                            icon_color=ft.Colors.RED_600,
                                            bgcolor=ft.Colors.RED_50,
                                            on_click=partial(confirm_delete, t.id, t.tool_name),
                                        ),
                                    ],
                                    tight=True,
                                ),
                                padding=8,
                            )
                        ),
                    ]
                )
            )
        page.update()

    def add_tool(tool_data: CreateTrainingToolDTO):
        try:
            TrainingToolService.create_tool(db, tool_data)
            load_tools()
            show_message("✅ تمت إضافة الأداة بنجاح")
        except Exception as ex:
            show_message(f"فشل في إضافة الأداة: {ex}", success=False)

    def edit_tool(tool_id: int, tool_data: UpdateTrainingToolDTO):
        try:
            TrainingToolService.update_tool(db, tool_id, tool_data)
            load_tools()
            show_message("✏️ تم تعديل الأداة بنجاح")
        except Exception as ex:
            show_message(f"فشل في تعديل الأداة: {ex}", success=False)

    def delete_tool(tool_id: int):
        try:
            success = TrainingToolService.delete_tool(db, tool_id)
            if success:
                load_tools()
                show_message("🗑️ تم حذف الأداة بنجاح")
            else:
                show_message("❌ الأداة غير موجودة", success=False)
        except Exception as ex:
            show_message(f"خطأ أثناء الحذف: {ex}", success=False)

    # ---------- Confirmation Dialog ----------
    def confirm_delete(tool_id: int, tool_name: str, e=None):
        def delete_confirmed(e):
            delete_tool(tool_id)
            close_dialog()

        confirm_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING, color=ft.Colors.ORANGE_600),
                ft.Text("تأكيد الحذف", weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_600)
            ]),
            content=ft.Text(f"هل أنت متأكد من حذف الأداة '{tool_name}'؟\nلا يمكن التراجع عن هذا الإجراء."),
            actions=[
                ft.TextButton(
                    "إلغاء", 
                    on_click=lambda e: close_dialog(),
                    style=ft.ButtonStyle(
                        color=ft.Colors.GREY_600,
                    )
                ),
                ft.ElevatedButton(
                    "حذف", 
                    on_click=delete_confirmed,
                    bgcolor=ft.Colors.RED_600,
                    color=ft.Colors.WHITE,
                    icon=ft.Icons.DELETE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = confirm_dlg
        confirm_dlg.open = True
        page.update()

    # ---------- Tool Form Dialog ----------
    def open_add_dialog(e):
        open_tool_form("إضافة أداة جديدة", None)

    def open_edit_dialog(tool_id: int, e=None):
        open_tool_form("تعديل أداة", tool_id)

    def open_tool_form(title: str, tool_id: int | None):
        # Get tool data if editing
        tool = TrainingToolService.get_tool(db, tool_id) if tool_id else None

        # Create form fields with enhanced styling
        name_field = ft.TextField(
            label="اسم الأداة",
            value=tool.tool_name if tool else "",
            border=ft.InputBorder.OUTLINE,
            focused_border_color=ft.Colors.BLUE_600,
            prefix_icon=ft.Icons.BUILD,
            hint_text="أدخل اسم الأداة...",
        )
        
        dept_field = ft.TextField(
            label="القسم",
            value=tool.department if tool else "",
            border=ft.InputBorder.OUTLINE,
            focused_border_color=ft.Colors.BLUE_600,
            prefix_icon=ft.Icons.BUSINESS,
            hint_text="أدخل اسم القسم...",
        )
        
        purchase_field = ft.TextField(
            label="تاريخ الشراء",
            value=str(tool.purchase_date) if tool and tool.purchase_date else "",
            border=ft.InputBorder.OUTLINE,
            focused_border_color=ft.Colors.BLUE_600,
            prefix_icon=ft.Icons.CALENDAR_TODAY,
            hint_text="YYYY-MM-DD",
        )
        
        notes_field = ft.TextField(
            label="ملاحظات",
            value=tool.notes if tool else "",
            border=ft.InputBorder.OUTLINE,
            focused_border_color=ft.Colors.BLUE_600,
            prefix_icon=ft.Icons.NOTES,
            hint_text="أضف ملاحظات إضافية...",
            multiline=True,
            max_lines=3,
        )
        
        image_field = ft.TextField(
            label="رابط الصورة",
            value=tool.tool_image if tool else "",
            border=ft.InputBorder.OUTLINE,
            focused_border_color=ft.Colors.BLUE_600,
            prefix_icon=ft.Icons.IMAGE,
            hint_text="أدخل رابط الصورة...",
        )

        def submit_form(e):
            # Validate required fields
            if not name_field.value.strip():
                show_message("يرجى إدخال اسم الأداة", success=False)
                return

            try:
                if tool_id:  # Edit mode
                    edit_tool(
                        tool_id,
                        UpdateTrainingToolDTO(
                            tool_name=name_field.value.strip(),
                            department=dept_field.value.strip() or None,
                            purchase_date=date.fromisoformat(purchase_field.value)
                            if purchase_field.value.strip()
                            else None,
                            notes=notes_field.value.strip() or None,
                            tool_image=image_field.value.strip() or None,
                        ),
                    )
                else:  # Add mode
                    add_tool(
                        CreateTrainingToolDTO(
                            tool_name=name_field.value.strip(),
                            department=dept_field.value.strip() or None,
                            purchase_date=date.fromisoformat(purchase_field.value)
                            if purchase_field.value.strip()
                            else None,
                            notes=notes_field.value.strip() or None,
                            tool_image=image_field.value.strip() or None,
                        )
                    )

                close_dialog()
            except ValueError as ve:
                show_message("تنسيق التاريخ غير صحيح. استخدم YYYY-MM-DD", success=False)
            except Exception as ex:
                show_message(f"خطأ: {ex}", success=False)

        # Create dialog with enhanced styling
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(
                    ft.Icons.ADD_CIRCLE if not tool_id else ft.Icons.EDIT,
                    color=ft.Colors.BLUE_600
                ),
                ft.Text(
                    title, 
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_800
                )
            ]),
            content=ft.Container(
                ft.Column([
                    name_field,
                    dept_field,
                    purchase_field,
                    notes_field,
                    image_field
                ], tight=True, spacing=10),
                width=400,
                padding=10,
            ),
            actions=[
                ft.TextButton(
                    "إلغاء",
                    on_click=lambda e: close_dialog(),
                    style=ft.ButtonStyle(
                        color=ft.Colors.GREY_600,
                    )
                ),
                ft.ElevatedButton(
                    "حفظ",
                    on_click=submit_form,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    icon=ft.Icons.SAVE
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = dlg
        dlg.open = True
        page.update()

    def close_dialog():
        if page.dialog:
            page.dialog.open = False
            page.update()

    # ---------- Enhanced UI Layout ----------
    
    # Header section with search and add button
    header = ft.Container(
        ft.Row([
            ft.Container(
                ft.Row([
                    ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLUE_600),
                    ft.TextField(
                        hint_text="ابحث عن أداة...",
                        on_submit=lambda e: load_tools(e.control.value),
                        border=ft.InputBorder.NONE,
                        expand=True,
                        text_size=14,
                    ),
                ], tight=True),
                bgcolor=ft.Colors.WHITE,
                border_radius=25,
                padding=ft.padding.symmetric(horizontal=15, vertical=5),
                border=ft.border.all(1, ft.Colors.GREY_300),
                expand=True,
            ),
            ft.ElevatedButton(
                "إضافة أداة جديدة",
                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                on_click=open_add_dialog,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(
                    elevation=4,
                    padding=ft.padding.symmetric(horizontal=20, vertical=15),
                ),
            ),
        ], spacing=15),
        bgcolor=ft.Colors.GREY_50,
        padding=20,
        border_radius=10,
        margin=ft.margin.only(bottom=20),
    )

    # Enhanced data table with styling
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text("ID", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
            ),
            ft.DataColumn(
                ft.Text("اسم الأداة", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
            ),
            ft.DataColumn(
                ft.Text("القسم", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
            ),
            ft.DataColumn(
                ft.Text("تاريخ الشراء", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
            ),
            ft.DataColumn(
                ft.Text("ملاحظات", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
            ),
            ft.DataColumn(
                ft.Text("صورة", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
            ),
            ft.DataColumn(
                ft.Text("إجراءات", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
            ),
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
    )

    # Table container with shadow effect
    table_container = ft.Container(
        ft.Column([
            data_table
        ], scroll=ft.ScrollMode.AUTO),
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        padding=10,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.GREY_300,
            offset=ft.Offset(0, 2),
        ),
    )

    # Main content layout
    content = ft.Container(
        ft.Column([
            header,
            table_container,
        ], spacing=0),
        padding=20,
        bgcolor=ft.Colors.GREY_100,
        expand=True,
    )

    # Load initial data
    load_tools()

    return content