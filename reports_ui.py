import flet as ft

# Local imports
from database import db

def create_reports_tab(page: ft.Page, financial_records, inventory_items):
    """Create and return the reports tab"""
    report_content = ft.TextField(
        multiline=True,
        read_only=True,
        expand=True,
        border=ft.InputBorder.NONE
    )

    def generate_report(e):
        students_data = db.get_all_students()
        total_students = len(students_data)
        total_financial = sum(float(record.monthly_fee) + float(record.bus_fee or 0) for record in financial_records)
        total_inventory = sum(float(item.quantity) * float(item.purchase_price or 0) for item in inventory_items)
        
        report_content.value = f"""
        تقرير نظام إدارة رياض الأطفال
        =============================
        
        إجمالي الطلاب: {total_students}
        القيمة المالية الإجمالية: ${total_financial:,.2f}
        قيمة المخزون الإجمالية: ${total_inventory:,.2f}
        
        الطلاب:
        {chr(10).join([f"- {s['name']} (العمر: {s['age']})" for s in students_data])}
        
        السجلات المالية:
        {chr(10).join([f"- {r.student_name}: شهري ${r.monthly_fee}, باص ${r.bus_fee or 0}" for r in financial_records])}
        
        عناصر المخزون:
        {chr(10).join([f"- {i.item_name}: {i.quantity} وحدة @ ${i.purchase_price or 0} لكل" for i in inventory_items])}
        """
        page.update()

    generate_report_btn = ft.ElevatedButton("إنشاء تقرير", on_click=generate_report)

    return ft.Column(
        [
            ft.Text("التقارير", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            generate_report_btn,
            ft.Divider(),
            report_content
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
