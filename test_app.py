import flet as ft

def main(page: ft.Page):
    page.title = "Test App"
    page.add(ft.Text("Hello, Flet!"))
    
if __name__ == "__main__":
    ft.app(target=main)
