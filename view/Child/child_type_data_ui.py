import flet as ft

# Local imports
from database import db_session
from models import ChildTypeEnum
from logic.child_logic import ChildService
from logic.full_day_program_logic import FullDayProgramService
from logic.individual_session_logic import IndividualSessionService


def show_child_type_data_page(page: ft.Page, child_id: int, current_user=None):
    """Show page for child type-specific data"""
    # Fetch child data
    with db_session() as db:
        child = ChildService.get_child_by_id(db, child_id)
        if not child:
            # Show error and return to child table
            snackbar = ft.SnackBar(
                content=ft.Text("لم يتم العثور على الطالب"),
                bgcolor=ft.Colors.RED,
                duration=3000,
            )
            page.overlay.append(snackbar)
            page.update()
            snackbar.open = True
            snackbar.update()
            page.update()
            return

    # Clear the page
    page.clean()

    # Create back button
    def go_back_to_child_table(e):
        """Navigate back to child table"""
        page.clean()
        # Import here to avoid circular imports
        from view.Child.child_ui import create_child_registration_tab
        from view.dashboard_ui import create_back_button

        child_tab = create_child_registration_tab(page, current_user)
        page.add(create_back_button(page, current_user))
        page.add(child_tab)
        page.update()

    back_button = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=24,
                tooltip="العودة إلى قائمة الطلاب",
                on_click=go_back_to_child_table,
            ),
            ft.Text("العودة إلى قائمة الطلاب", size=16),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Child basic info
    basic_info = ft.Container(
        ft.Column(
            [
                ft.Text(
                    "معلومات الطالب الأساسية",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Container(
                    ft.Row(
                        [
                            ft.Text(
                                "الاسم:",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.RIGHT,
                                width=120,
                            ),
                            ft.Text(
                                child.name,
                                size=16,
                                text_align=ft.TextAlign.RIGHT,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=ft.padding.symmetric(vertical=5),
                ),
                ft.Container(
                    ft.Row(
                        [
                            ft.Text(
                                "العمر:",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.RIGHT,
                                width=120,
                            ),
                            ft.Text(
                                str(child.age) if child.age else "-",
                                size=16,
                                text_align=ft.TextAlign.RIGHT,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=ft.padding.symmetric(vertical=5),
                ),
                ft.Container(
                    ft.Row(
                        [
                            ft.Text(
                                "نوع الطالب:",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.RIGHT,
                                width=120,
                            ),
                            ft.Text(
                                child.child_type.value if child.child_type else "-",
                                size=16,
                                text_align=ft.TextAlign.RIGHT,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=ft.padding.symmetric(vertical=5),
                ),
            ]
        ),
        padding=ft.padding.all(15),
        border=ft.border.all(1, ft.Colors.BLUE_100),
        border_radius=ft.border_radius.all(8),
        bgcolor=ft.Colors.BLUE_50,
        margin=ft.margin.only(bottom=10),
    )

    # Type-specific data
    type_data_column = ft.Column(
        [
            ft.Text(
                "بيانات النوع",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREEN_700,
            ),
        ]
    )
    type_data = ft.Container(
        type_data_column,
        padding=ft.padding.all(15),
        border=ft.border.all(1, ft.Colors.GREEN_100),
        border_radius=ft.border_radius.all(8),
        bgcolor=ft.Colors.GREEN_50,
        margin=ft.margin.only(bottom=10),
    )

    with db_session() as db:
        if child.child_type == ChildTypeEnum.FULL_DAY:
            program = FullDayProgramService.get_program_by_child_id(db, child_id)
            if program:
                type_data_column.controls.extend([
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "التشخيص:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=120,
                                ),
                                ft.Text(
                                    program.diagnosis or "-",
                                    size=16,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "قيمة الاشتراك الشهري:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=120,
                                ),
                                ft.Text(
                                    str(program.monthly_fee) if program.monthly_fee else "-",
                                    size=16,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "قيمة اشتراك الباص:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=120,
                                ),
                                ft.Text(
                                    str(program.bus_fee) if program.bus_fee else "-",
                                    size=16,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "حالة الحضور:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=120,
                                ),
                                ft.Text(
                                    program.attendance_status or "-",
                                    size=16,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    ft.Container(
                        ft.Column(
                            [
                                ft.Text(
                                    "الملاحظات:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                                ft.Container(
                                    ft.Text(
                                        program.notes or "-",
                                        size=14,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                    padding=ft.padding.all(10),
                                    border=ft.border.all(1, ft.Colors.GREY_300),
                                    border_radius=ft.border_radius.all(5),
                                    bgcolor=ft.Colors.WHITE,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                ])
            else:
                type_data_column.controls.append(
                    ft.Text("لا توجد بيانات للبرنامج اليومي الكامل")
                )
        elif child.child_type == ChildTypeEnum.SESSIONS:
            session = IndividualSessionService.get_session_by_child_id(db, child_id)
            if session:
                type_data_column.controls.extend([
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "التشخيص:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=120,
                                ),
                                ft.Text(
                                    session.diagnosis or "-",
                                    size=16,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "قيمة الجلسة:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=120,
                                ),
                                ft.Text(
                                    str(session.session_fee) if session.session_fee else "-",
                                    size=16,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "عدد الجلسات الشهرية:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=120,
                                ),
                                ft.Text(
                                    str(session.monthly_sessions_count) if session.monthly_sessions_count else "-",
                                    size=16,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "عدد الجلسات المحضورة:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=120,
                                ),
                                ft.Text(
                                    str(session.attended_sessions_count) if session.attended_sessions_count else "-",
                                    size=16,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    ft.Container(
                        ft.Row(
                            [
                                ft.Text(
                                    "اسم المتخصص:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                    width=120,
                                ),
                                ft.Text(
                                    session.specialist_name or "-",
                                    size=16,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                    ft.Container(
                        ft.Column(
                            [
                                ft.Text(
                                    "الملاحظات:",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.RIGHT,
                                ),
                                ft.Container(
                                    ft.Text(
                                        session.notes or "-",
                                        size=14,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                    padding=ft.padding.all(10),
                                    border=ft.border.all(1, ft.Colors.GREY_300),
                                    border_radius=ft.border_radius.all(5),
                                    bgcolor=ft.Colors.WHITE,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.symmetric(vertical=5),
                    ),
                ])
            else:
                type_data_column.controls.append(
                    ft.Text("لا توجد بيانات للجلسات الفردية")
                )
        else:
            type_data_column.controls.append(
                ft.Text("نوع الطالب غير محدد")
            )

    # Main layout
    main_content = ft.Column(
        [
            back_button,
            ft.Divider(),
            ft.Text(
                f"بيانات الطالب: {child.name}",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Divider(),
            basic_info,
            type_data,
        ],
        spacing=20,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    # Add to page
    page.add(main_content)
    page.update()
