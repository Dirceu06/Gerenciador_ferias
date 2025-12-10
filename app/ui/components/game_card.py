import flet as ft

class PasswordCard:
    def __init__(self, title, domain, on_click=None, width=260, height=300):
        self.title = title
        self.domain = domain
        self.on_click = on_click
        self.width = width
        self.height = height
        self._build_card()

    def _build_card(self):
        icon_url = f"https://img.logo.dev/{self.domain}?token=pk_ZOpB240VSUGBfZoBNrGjHQ&theme=dark&format=png&size=500"

        self.card = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Image(
                    src=icon_url,
                    width=float("inf"),   # ← IMPORTANTE
                    height=150,
                    fit=ft.ImageFit.CONTAIN,
                ),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                margin=10
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(self.title, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(self.domain, size=12, color=ft.colors.GREY_600),
                    ft.TextButton("Detalhes", on_click=self._on_card_click)
                ], spacing=8),
                padding=15,
            )
        ], spacing=0),
        width=float("inf"),
        border_radius=10,
        bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
        on_click=self._on_card_click,
        
    )


    def _on_card_click(self, e):
        if self.on_click:
            self.on_click(self.title)

    def build(self):
        return self.card
