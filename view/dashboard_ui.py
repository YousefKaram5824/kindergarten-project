import flet as ft
import time

# Local imports
from view.auth_ui import set_show_main_system_callback, show_login_page
from database import db
from view.financial_ui import create_financial_tab
from view.inventory_ui import create_inventory_tab
from view.reports_ui import create_reports_tab
from view.student_ui import create_student_registration_tab


class HoverNavigationRail(ft.Container):
    def __init__(self, destinations, on_change, **kwargs):
        super().__init__(**kwargs)
        self.destinations = destinations
        self.on_change = on_change
        self.is_expanded = False

        # Create the navigation rail
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.NONE,
            min_width=60,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=destinations,
            on_change=on_change,
        )

        # Set initial content
        self.content = self.nav_rail
        self.width = 60
        self.bgcolor = ft.Colors.GREY_100
        self.padding = 0
        self.margin = 0
        self.border_radius = 0

        # Add hover functionality
        self.on_hover = self.handle_hover

    def handle_hover(self, e):
        if e.data == "true":
            # Mouse entered - expand
            self.expand_rail()
        else:
            # Mouse left - collapse after delay
            self.collapse_rail()

    def expand_rail(self):
        if not self.is_expanded:
            self.is_expanded = True
            self.nav_rail.label_type = ft.NavigationRailLabelType.ALL
            self.width = 200
            self.animate = ft.Animation(
                duration=300, curve=ft.AnimationCurve.EASE_IN_OUT
            )
            self.update()

    def collapse_rail(self):
        if self.is_expanded:
            self.is_expanded = False
            self.nav_rail.label_type = ft.NavigationRailLabelType.NONE
            self.width = 60
            self.animate = ft.Animation(
                duration=300, curve=ft.AnimationCurve.EASE_IN_OUT
            )
            self.update()

    def did_mount(self):
        # Store page reference when control is mounted
        self._page = self.page


def create_dashboard(page: ft.Page, current_user):
    """Create and return the main dashboard"""
    # Clear login page
    page.clean()

    # Set page title with current user info
    if current_user:
        page.title = f"لوحة تحكم نظام إدارة رياض الأطفال - {current_user.username}"
    else:
        page.title = "لوحة تحكم نظام إدارة رياض الأطفال - غير مسجل الدخول"

    # Data storage
    financial_records = []
    inventory_items = []

    # Create navigation destinations
    nav_destinations = [
        ft.NavigationRailDestination(
            icon=ft.Icons.HOME, selected_icon=ft.Icons.HOME, label="الرئيسية"
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.PERSON, selected_icon=ft.Icons.PERSON, label="الطلاب"
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.ACCOUNT_BALANCE,
            selected_icon=ft.Icons.ACCOUNT_BALANCE,
            label="المالية",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.INVENTORY, selected_icon=ft.Icons.INVENTORY, label="المخزون"
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.ANALYTICS, selected_icon=ft.Icons.ANALYTICS, label="التقارير"
        ),
    ]

    # Create custom hover navigation rail
    nav_rail = HoverNavigationRail(
        destinations=nav_destinations,
        on_change=lambda e: handle_navigation_change(
            e, page, current_user, financial_records, inventory_items
        ),
    )

    # Dashboard header with user info
    header = ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=24,
                tooltip="العودة إلى تسجيل الدخول",
                on_click=lambda e: back_to_login(page),
            ),
            ft.Text(
                "لوحة تحكم نظام إدارة رياض الأطفال",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Container(expand=True),
            ft.Text(
                f"مرحباً: {current_user.username if current_user else 'زائر'}",
                size=16,
                color=ft.Colors.GREY_600,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Dashboard statistics cards
    stats_row = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.PEOPLE, size=40, color=ft.Colors.BLUE),
                        ft.Text("0", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("الطلاب المسجلين", size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=160,
                height=160,
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_50,
                border=ft.border.all(1, ft.Colors.BLUE_100),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.ACCOUNT_BALANCE_WALLET,
                            size=40,
                            color=ft.Colors.GREEN,
                        ),
                        ft.Text("0", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("الإيرادات الشهرية", size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=160,
                height=160,
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.GREEN_50,
                border=ft.border.all(1, ft.Colors.GREEN_100),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.INVENTORY_2, size=40, color=ft.Colors.ORANGE),
                        ft.Text("0", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("عناصر المخزون", size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=160,
                height=160,
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.ORANGE_50,
                border=ft.border.all(1, ft.Colors.ORANGE_100),
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.SECURITY, size=40, color=ft.Colors.PURPLE),
                        ft.Text("1", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("المستخدمين النشطين", size=14),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=160,
                height=160,
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.PURPLE_50,
                border=ft.border.all(1, ft.Colors.PURPLE_100),
            ),
        ],
        spacing=20,
    )

    # Main content area - restructured to have content at the top
    content_area = ft.Column(
        [
            ft.Text("مرحباً بك في لوحة التحكم", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("هنا يمكنك إدارة جميع جوانب رياض الأطفال بسهولة", size=16),
            ft.Divider(),
            ft.Text("الإجراءات السريعة:", size=18, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "تسجيل طالب جديد",
                        icon=ft.Icons.PERSON_ADD,
                        on_click=lambda e: show_student_tab(
                            page, current_user, financial_records, inventory_items
                        ),
                    ),
                    ft.ElevatedButton(
                        "إضافة سجل مالي",
                        icon=ft.Icons.ADD_BUSINESS,
                        on_click=lambda e: show_financial_tab(
                            page, current_user, financial_records, inventory_items
                        ),
                    ),
                    ft.ElevatedButton(
                        "إدارة المخزون",
                        icon=ft.Icons.INVENTORY,
                        on_click=lambda e: show_inventory_tab(
                            page, current_user, financial_records, inventory_items
                        ),
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(),
            stats_row,
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    # Main layout
    main_layout = ft.Row(
        [
            nav_rail,
            ft.Container(
                content=ft.Column(
                    [header, ft.Divider(), content_area], scroll=ft.ScrollMode.AUTO
                ),
                expand=True,
                padding=20,
            ),
        ],
        expand=True,
    )

    # Update statistics
    update_dashboard_stats(stats_row)

    return main_layout


def update_dashboard_stats(stats_row):
    """Update dashboard statistics with real data"""
    try:
        # Get students count
        students = db.get_all_students()
        students_count = len(students)

        # Get inventory count
        inventory = db.get_all_inventory()
        inventory_count = len(inventory)

        # Update stats cards
        stats_row.controls[0].content.controls[1].value = str(students_count)
        stats_row.controls[2].content.controls[1].value = str(inventory_count)

    except Exception as e:
        print(f"Error updating dashboard stats: {e}")


def handle_navigation_change(e, page, current_user, financial_records, inventory_items):
    """Handle navigation rail selection changes"""
    index = e.control.selected_index
    if index == 0:  # Home
        show_dashboard(page, current_user)
    elif index == 1:  # Students
        show_student_tab(page, current_user, financial_records, inventory_items)
    elif index == 2:  # Financial
        show_financial_tab(page, current_user, financial_records, inventory_items)
    elif index == 3:  # Inventory
        show_inventory_tab(page, current_user, financial_records, inventory_items)
    elif index == 4:  # Reports
        show_reports_tab(page, current_user, financial_records, inventory_items)


def show_dashboard(page, current_user):
    """Show the main dashboard"""
    page.clean()
    dashboard = create_dashboard(page, current_user)
    page.add(dashboard)
    page.update()


def show_student_tab(page, current_user, financial_records, inventory_items):
    """Show student registration tab"""
    page.clean()
    student_tab = create_student_registration_tab(page)
    page.add(create_back_button(page, current_user))
    page.add(student_tab)
    page.update()


def show_financial_tab(page, current_user, financial_records, inventory_items):
    """Show financial management tab"""
    page.clean()
    financial_tab = create_financial_tab(page)
    page.add(create_back_button(page, current_user))
    page.add(financial_tab)
    page.update()


def show_inventory_tab(page, current_user, financial_records, inventory_items):
    """Show inventory management tab"""
    page.clean()
    inventory_tab = create_inventory_tab(page)
    page.add(create_back_button(page, current_user))
    page.add(inventory_tab)
    page.update()


def show_reports_tab(page, current_user, financial_records, inventory_items):
    """Show reports tab"""
    page.clean()
    reports_tab = create_reports_tab(page, financial_records, inventory_items)
    page.add(create_back_button(page, current_user))
    page.add(reports_tab)
    page.update()


def create_back_button(page, current_user):
    """Create back button to return to dashboard"""
    return ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_size=24,
                tooltip="العودة إلى لوحة التحكم",
                on_click=lambda e: show_dashboard(page, current_user),
            ),
            ft.Text("العودة إلى لوحة التحكم", size=16),
        ]
    )


def back_to_login(page: ft.Page):
    """Return to login page"""
    page.clean()
    show_login_page(page)


def show_main_system(page: ft.Page, current_user):
    """Show the main system with dashboard"""
    show_dashboard(page, current_user)


# Set the callback for showing main system
set_show_main_system_callback(show_main_system)
