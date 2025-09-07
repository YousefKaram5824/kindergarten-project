import flet as ft

# Local imports
from database import db_session
from logic.child_logic import ChildService


def create_reports_tab(page: ft.Page, financial_records, inventory_items):
    """Create and return the reports tab"""
    report_content = ft.TextField(
        multiline=True,
        read_only=True,
        expand=True,
        border=ft.InputBorder.NONE,
        text_align=ft.TextAlign.RIGHT,
    )

    def generate_report(e):
        with db_session() as db:
            childs_data = ChildService.get_all_children(db)
            total_childs = len(childs_data)
            total_financial = sum(
                float(record.monthly_fee) + float(record.bus_fee or 0)
                for record in financial_records
            )
            total_inventory = sum(
                float(item.quantity) * float(item.purchase_price or 0)
                for item in inventory_items
            )

            report_content.value = f"""
            تقرير نظام إدارة رياض الأطفال
            =============================
            
            إجمالي الطلاب: {total_childs}
            القيمة المالية الإجمالية: ${total_financial:,.2f}
            قيمة المخزون الإجمالية: ${total_inventory:,.2f}
            
            الطلاب:
            {chr(10).join([f"- {s.name} (العمر: {s.age or 'غير محدد'})" for s in childs_data])}
            
            السجلات المالية:
            {chr(10).join([f"- {r.child_name}: شهري ${r.monthly_fee}, باص ${r.bus_fee or 0}" for r in financial_records])}
            
            عناصر المخزون:
            {chr(10).join([f"- {i.item_name}: {i.quantity} وحدة @ ${i.purchase_price or 0} لكل" for i in inventory_items])}
            """
            page.update()

    generate_report_btn = ft.ElevatedButton("إنشاء تقرير", on_click=generate_report)

    return ft.Column(
        [
            ft.Text(
                "التقارير",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.RIGHT,
            ),
            ft.Divider(),
            ft.Row([generate_report_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            report_content,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )
