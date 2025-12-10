import flet as ft
from app.ui.app_state import state
from app.ui.components.game_card import PasswordCard
from app.core.database.opDB import Banco

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.banco = Banco()
        self.botao=False
        self.build_ui()
        self.page.on_resize = lambda e: self.grid.update()
    
    def toggle_botao(self, e):
        self.botao = not self.botao

        if self.botao:
            self.add_button.icon = ft.icons.REMOVE  
            self.add_button.bgcolor = ft.colors.RED_600 
        else:
            self.add_button.icon = ft.icons.ADD  
            self.add_button.bgcolor = ft.colors.BLUE_900  
        
        #mostrar/ocultar pop
        if hasattr(self, 'pop_container'):
            self.pop_container.visible = self.botao
        
        #atualiza o botão e pag
        self.add_button.update()  
        self.page.update() 
        
    def build_ui(self):
        self.sites = self.banco.lerReg()
        exibir = []
        for s in self.sites:
            reg = {'id': s[0],'titulo': f'{s[1]}','dominio': f'{s[2]}','usuario': f'{s[3]}','senha': f'{s[4]}','data_criacao': f'{s[5]}'}
            exibir.append(reg)
            
        #GRID
        self.grid = ft.GridView(
            expand=True,
            max_extent=300,   # largura máxima por card
            child_aspect_ratio=1,
            spacing=20,
            run_spacing=20,
        )
        
        #atribuindo cards
        for site in exibir:
            card = PasswordCard(
                id=site['id'],
                title=site["titulo"],
                on_click=lambda name: self.abrir_detalhes(name),domain=f"{site["dominio"].lower()}",
                delete=self.deletar_registro
            ).build()

            self.grid.controls.append(card)

        #barra pesquisar
        search_bar = ft.TextField(label="Pesquisar",
            enable_suggestions=True,
            width=800,
            prefix_icon=ft.icons.SEARCH,
            border_radius=10,
            border_color=ft.colors.WHITE
        )

        #botão adicionar
        self.add_button = ft.IconButton(
            icon=ft.icons.ADD,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_900,
            on_click=self.toggle_botao
        )


        #conteudo
        self.content = ft.Container(
            content=ft.Column([
                ft.ResponsiveRow([search_bar],alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Gerenciador de Senhas", size=28, weight="bold"),
                self.grid,
                ft.Row([self.add_button],alignment=ft.MainAxisAlignment.END)
            ], expand=True),
            
            expand=True,
            padding=30,
        )
        
        self.pop_up_inserir()  # 1. Criar o popup
        self.content.content.controls.insert(-1, self.pop_container)  # 2. Adicionar ao layout
    
    def build(self):
        """Retorna a view"""
        return ft.View(
            route="/home",
            controls=[
                ft.Stack([
                    ft.Row([self.content], expand=True),
                    self.pop_container  # Popup com posicionamento absoluto
                ], expand=True)
            ]
        )
        
    def pop_up_inserir(self):
        self.titulo_input = ft.TextField(
            label="Titulo",
            width=250,
            autofocus=True,
            prefix_icon=ft.icons.WORDPRESS_ROUNDED
        )
        self.dominio_input = ft.TextField(
            label="Dominio",
            width=250,
            autofocus=True,
            prefix_icon=ft.icons.LANGUAGE,
            hint_text='exemplo.com'
        )
        self.usuario_input = ft.TextField(
            label="Usuário",
            width=250,
            autofocus=True,
            prefix_icon=ft.icons.PERSON
        )
        self.senha_input = ft.TextField(
            label="Senha",
            width=250,
            autofocus=True,
            prefix_icon=ft.icons.LOCK
        )
        
        self.pop_container = ft.Container(
            content=ft.Column([
                self.titulo_input,
                self.dominio_input,
                self.usuario_input,
                self.senha_input,
                ft.ElevatedButton("inserir", 
                    icon=ft.icons.UPLOAD, 
                    on_click=lambda e: self.inserirNovoReg(
                        self.titulo_input.value,
                        self.dominio_input.value,
                        self.usuario_input.value,
                        self.senha_input.value
                    ), 
                    width=250, 
                    height=45,
                )
            ]),
            width=280,  
            height=350,
            right=15,
            bottom=80,
            bgcolor=ft.colors.SURFACE_VARIANT,  # COR SÓLIDA
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.OUTLINE),
            visible=self.botao
        )
    
    def abrir_detalhes(self, site):
        state.show_snackbar(f"Detalhes do {site}")
        #depois self.page.go(f"/senha/{site_id}")
    
    def atualizar_grid(self):
        """Atualiza o grid com os dados do banco"""
        # 1. Limpar os cards atuais
        self.grid.controls.clear()
        
        sites = self.banco.lerReg()
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
                title=site["titulo"],
                on_click=lambda name: self.abrir_detalhes(name),
                domain=f"{site['dominio'].lower()}",
                delete=self.deletar_registro
            ).build()
            self.grid.controls.append(card)
        
        self.grid.update()
        
    def inserirNovoReg(self, titulo, dominio, usuario, senha):
        """Insere novo registro e atualiza a interface"""
        sucesso = self.banco.inserirReg(titulo, dominio, usuario, senha)
        
        if sucesso:
            state.show_snackbar('Login Salvo!!!')
            
            self.titulo_input.value = ""
            self.dominio_input.value = ""
            self.usuario_input.value = ""
            self.senha_input.value = ""
            
            # Fechar o popup
            self.botao = False
            self.pop_container.visible = False
            self.add_button.icon = ft.icons.ADD
            self.add_button.bgcolor=ft.colors.BLUE_900
            self.add_button.update()
            self.atualizar_grid()
            
            self.page.update()
        else:
            state.show_snackbar('Erro ao salvar login!')

    def deletar_registro(self, registro_id):
        """Deleta um registro específico"""
        try:
            self.banco.deletarReg(registro_id)
            state.show_snackbar(f"'{registro_id}' deletado com sucesso!")
            self.atualizar_grid() 
        except Exception as e:
            print(f"Erro: {e}")
            state.show_snackbar(f"Erro ao deletar '{registro_id}'")