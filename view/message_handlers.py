import flet as ft


def show_success_message(page: ft.Page, message: str, duration: int = 3000):
    """Display a success message using a snackbar"""
    snackbar = ft.SnackBar(
        content=ft.Text(message),
        bgcolor=ft.Colors.GREEN,
        duration=duration,
    )
    page.overlay.append(snackbar)
    page.update()
    snackbar.open = True
    snackbar.update()
    page.update()


def show_error_message(page: ft.Page, message: str, duration: int = 3000):
    """Display an error message using a snackbar"""
    snackbar = ft.SnackBar(
        content=ft.Text(message),
        bgcolor=ft.Colors.RED,
        duration=duration,
    )
    page.overlay.append(snackbar)
    page.update()
    snackbar.open = True
    snackbar.update()
    page.update()


def show_info_message(page: ft.Page, message: str, duration: int = 3000):
    """Display an informational message using a snackbar"""
    snackbar = ft.SnackBar(
        content=ft.Text(message),
        bgcolor=ft.Colors.BLUE,
        duration=duration,
    )
    page.overlay.append(snackbar)
    page.update()
    snackbar.open = True
    snackbar.update()
    page.update()


def show_warning_message(page: ft.Page, message: str, duration: int = 3000):
    """Display a warning message using a snackbar"""
    snackbar = ft.SnackBar(
        content=ft.Text(message),
        bgcolor=ft.Colors.ORANGE,
        duration=duration,
    )
    page.overlay.append(snackbar)
    page.update()
    snackbar.open = True
    snackbar.update()
    page.update()
