import flet as ft
from app.core.database.opDB import Banco
class PasswordCard:
    def __init__(self, title, domain, id, on_click=None, width=260, height=300,delete=None):
        self.title = title
        self.domain = domain
        self.id=id
        self.on_click = on_click
        self.delete = delete
        self.width = width
        self.height = height
        self.key = retirarKeys()[0]
        self._build_card()

    def _build_card(self):
        icon_url = f"https://img.logo.dev/{self.domain}?token={self.key}&theme=dark&format=png&size=500"

        self.card = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Image(
                    src=icon_url,
                    width=float("inf"),
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
                    ft.ResponsiveRow(controls=[ft.TextButton("Excluir", on_click=self.deletarCard),ft.TextButton("Detalhes", on_click=self._on_card_click)])
                ], spacing=8),
                padding=15,
            )
        ], spacing=0),
        width=float("inf"),
        border_radius=10,
        bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE)
    )


    def _on_card_click(self, e):
        if self.on_click:
            self.on_click(self.title)
            
    def deletarCard(self, e):
        self.banco = Banco()
        self.delete(self.id)
        
    def build(self):
        return self.card
    
def retirarKeys():
    arq = open("keys.txt", 'r')
    linhas = arq.readlines()
    keys=[]
    for l in linhas:
        l = l.strip().split(':')
        keys.append(l[1].strip())
    return keys