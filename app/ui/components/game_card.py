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

        self.card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Image(
                        src=icon_url,
                        width=120,
                        height=120,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Text(
                        self.title,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.TextButton("Detalhes", on_click=self._on_card_click),
                            ft.FilledButton(
                                "Excluir",
                                icon=ft.icons.DELETE,
                                on_click=self.deletarCard,
                                bgcolor=ft.colors.RED_600,
                                color=ft.colors.WHITE
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            width=300,
        ),
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