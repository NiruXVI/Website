import flet as ft

def main(page: ft.Page):
    page.title = "Flet Mobile App"
    page.window_width, page.window_height = 400, 800
    page.theme_mode = ft.ThemeMode.DARK

    titles = ["Home", "Chat", "Settings"]
    def make_page(title): return ft.Container(
        ft.Column([ft.Text(title, size=28, weight=ft.FontWeight.BOLD, color="white")],
                  alignment=ft.MainAxisAlignment.CENTER, expand=True),
        alignment=ft.alignment.center, expand=True, bgcolor="#181A20"
    )

    body = ft.Container(content=make_page(titles[0]), expand=True, bgcolor="#181A20")

    def on_nav_change(e):
        body.content = make_page(titles[e.control.selected_index])
        page.update()

    page.add(
        ft.Container(
            ft.Row([
                ft.CircleAvatar(
                    ft.Image(src="https://i.ibb.co/MD8mJstF/logos.png", width=40, height=40, fit=ft.ImageFit.COVER), radius=20),
                ft.Text("Ivan Paul A De La Peña", size=22, weight=ft.FontWeight.BOLD, color="white"),
            ], alignment=ft.MainAxisAlignment.START, spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.only(left=16, top=16, bottom=8), height=60, bgcolor="#23272F"
        ),
        body,
        ft.NavigationBar(
            destinations=[ft.NavigationBarDestination(icon=i.lower(), label=i) for i in titles],
            selected_index=0, on_change=on_nav_change, bgcolor="#23272F"
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER)