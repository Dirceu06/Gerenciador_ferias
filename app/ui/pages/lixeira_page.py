import flet as ft
from app.ui.app_state import state
from app.ui.components.game_card import PasswordCard
from app.core.database.opDB import Banco

class Historico:
    def __init__(self, page: ft.Page):
        self.page = page
        self.banco = Banco()
        self.botao=False
        self.build_ui()
        self.page.on_resize = lambda e: self.page.update()
    
    def build_ui(self):
        self.sites = self.banco.lerReg(banco='reg_deletados')
        exibir = []
        for s in self.sites:
            reg = {'id': s[0],'titulo': f'{s[1]}','dominio': f'{s[2]}','usuario': f'{s[3]}','senha': f'{s[4]}','data_exclusão': f'{s[5]}'}
            exibir.append(reg)
            
        #GRID
        self.grid = ft.GridView(
            expand=True,
            
            max_extent=265,
            child_aspect_ratio=0.88,
            spacing=10,
            run_spacing=10,
        )
        
        #atribuindo cards
        for site in exibir:
            card = PasswordCard(
                id=site['id'],
                senha=site['senha'],
                usuario=site['usuario'],
                title=site["titulo"],
                domain=f"{site["dominio"].lower()}",
                on_click=lambda id: self.restaurar(id),
                delete=self.apagarCOMPLETAMENTEreg,
                lixo=True
            ).build()
            self.grid.controls.append(card)

        #barra pesquisar
        self.barra_pesquisa = ft.TextField(label="Pesquisar",
            enable_suggestions=True,
            width=800,
            prefix_icon=ft.icons.SEARCH,
            border_radius=10,
            border_color=ft.colors.WHITE,
            on_change=self.pesquisar
        )
        
        #botão logout
        self.logout_btn = ft.IconButton(
            icon=ft.icons.LOGOUT_OUTLINED,
            icon_color=ft.colors.RED_700,
            bgcolor=ft.colors.BLACK38,
            on_click=self.logout,
            alignment=ft.alignment.center_left
        )

        #botão voltar para home
        self.lixeira = ft.Container(
            content=ft.IconButton(
            icon=ft.icons.ARROW_BACK_OUTLINED,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_500,
            on_click=self.voltarHome,
        ),margin=ft.margin.only(right=12),alignment=ft.alignment.center_right)
        
        #conteudo
        self.content = ft.Container(
            content=ft.Column([
                ft.ResponsiveRow([self.barra_pesquisa],alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(f"LIXEIRA de {self.banco.login}", size=28, weight="bold"),
                self.grid,
                ft.Row([self.logout_btn, ft.Container(expand=True), self.lixeira],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,spacing=40)
            ], expand=True),
            expand=True,
            padding=20,
            visible=True
        )
        
        self.main_stack = ft.Stack([
            self.content
        ], expand=True)
        
    def build(self):
        return ft.View(
            route="/home",
            controls=[
                self.main_stack
            ]
        )
    
    def atualizar_grid(self,condicao=False,pesquisa=''):
        """Atualiza o grid com os dados do banco"""
        # 1. Limpar os cards atuais
        self.grid.controls.clear()
        
        sites = self.banco.lerReg(condicao,pesquisa,banco='reg_deletados')
        exibir = []
        for s in sites:
            reg = {
                'id': s[0],
                'titulo': f'{s[1]}',
                'dominio': f'{s[2]}',
                'usuario': f'{s[3]}',
                'senha': f'{s[4]}',
                'data_criacao': f'{s[5]}'
            }
            exibir.append(reg)
        
        for site in exibir:
            card = PasswordCard(
                id=site['id'],
                usuario=site['usuario'],
                senha=site['senha'],
                title=site["titulo"],
                domain=f"{site['dominio'].lower()}",
                on_click=lambda id: self.restaurar(id),
                delete=self.apagarCOMPLETAMENTEreg,
                lixo=True
            ).build()
            self.grid.controls.append(card)
        
        self.grid.update()
    
    def restaurar(self,id):
        self.banco.restaurar(id=id)
        state.show_snackbar(f"'{id}' restaurado com sucesso!")
        self.atualizar_grid()
        
    def apagarCOMPLETAMENTEreg(self,id):
        """Deleta um registro específico"""
        try:
            self.banco.deletarReg(id=id,banco='reg_deletados')
            state.show_snackbar(f"'{id}' deletado com sucesso!")
            self.atualizar_grid() 
        except Exception as e:
            print(f"Erro: {e}")
            state.show_snackbar(f"Erro ao deletar '{id}'")

    def voltarHome(self,e):
        self.page.go("/home")
    
    def pesquisar(self,e):
        pesquisa = self.barra_pesquisa.value
        self.atualizar_grid(True,pesquisa)

    def logout(self,e):
        self.banco.logout()
        self.page.go("/")