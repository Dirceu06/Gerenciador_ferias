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
            self.adicionar_btn.icon = ft.icons.REMOVE  
            self.adicionar_btn.bgcolor = ft.colors.RED_600 
        else:
            self.adicionar_btn.icon = ft.icons.ADD  
            self.adicionar_btn.bgcolor = ft.colors.BLUE_900  
        
        #mostrar/ocultar pop
        if hasattr(self, 'pop_container'):
            self.pop_container.visible = self.botao
        
        #atualiza o botão e pag
        self.adicionar_btn.update()  
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
            
            max_extent=265,   # largura máxima por card
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
                on_click=lambda id, title,dominio, usuario, senha: self.abrir_detalhes(id, title, dominio, usuario, senha),
                delete=self.deletar_registro
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

        #botão adicionar
        self.adicionar_btn = ft.IconButton(
            icon=ft.icons.ADD,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_900,
            on_click=self.toggle_botao
        )

        
        #conteudo
        self.content = ft.Container(
            content=ft.Column([
                ft.ResponsiveRow([self.barra_pesquisa],alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Gerenciador de Senhas", size=28, weight="bold"),
                self.grid,
                ft.Row([self.adicionar_btn],alignment=ft.MainAxisAlignment.END)
            ], expand=True),
            expand=True,
            padding=30,
            visible=True
        )
        
        
        self.pop_up_inserir()  # 1. Criar o popup
        self.content.content.controls.insert(-1, self.pop_container)  # 2. Adicionar ao layout
        
        self.main_stack = ft.Stack([
            self.content,
            self.pop_container,
        ], expand=True)
    
    def build(self):
        """Retorna a view"""
        return ft.View(
            route="/home",
            controls=[
                self.main_stack
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
    
    def criarStack(self, id='', titulo='', dominio='', usuario='', senha='',show=False):
        self.tituloStack_input = ft.ResponsiveRow([
            ft.TextField(
                label="titulo",
                value=f'{titulo}',
                autofocus=True,
                prefix_icon=ft.icons.TITLE,
                col={"sm": 9, "md": 11},
                width=None,
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.CONTENT_COPY,
                    bgcolor=ft.colors.GREY_600,
                    icon_color=ft.colors.WHITE,
                    icon_size=20,
                    on_click=lambda e, s=titulo: self.copiar(s)
                ),
                col={"sm": 1},
                width=120,
                height=40,
               
                padding=ft.padding.only(left=15),
            )
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.dominioStack_input = ft.ResponsiveRow([
            ft.TextField(
                label="dominio",
                value=f'{dominio}',
                autofocus=True,
                prefix_icon=ft.icons.LANGUAGE,
                col={"sm": 9, "md": 11},
                width=None,
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.CONTENT_COPY,
                    bgcolor=ft.colors.GREY_600,
                    icon_color=ft.colors.WHITE,
                    icon_size=20,
                    on_click=lambda e, s=dominio: self.copiar(s)
                ),
                col={"sm": 1},
                width=120,
                height=40,
               
                padding=ft.padding.only(left=15),
            )
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.usuarioStack_input = ft.ResponsiveRow([
            ft.TextField(
                label="usuario",
                value=f'{usuario}',
                autofocus=True,
                prefix_icon=ft.icons.PERSON,
                col={"sm": 9, "md": 11},
                width=None,
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.CONTENT_COPY,
                    bgcolor=ft.colors.GREY_600,
                    icon_color=ft.colors.WHITE,
                    icon_size=20,
                    on_click=lambda e, s=usuario: self.copiar(s)
                ),
                col={"sm": 1},
                width=120,
                height=40,
               
                padding=ft.padding.only(left=15),
            )
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.senhaStack_input = ft.ResponsiveRow([
            ft.TextField(
                label="senha",
                value=f'{senha}',
                autofocus=True,
                prefix_icon=ft.icons.LOCK,
                col={"sm": 9, "md": 11},
                width=None,
                password=True,
                can_reveal_password=True
            ),
            ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.CONTENT_COPY,
                    bgcolor=ft.colors.GREY_600,
                    icon_color=ft.colors.WHITE,
                    icon_size=20,
                    on_click=lambda e, s=senha: self.copiar(s)
                ),
                col={"sm": 1},
                width=120,
                height=40,
               
                padding=ft.padding.only(left=15),
            )
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        #botão de salvar
        self.salvar_btn = ft.ElevatedButton(
            "salvar",
            icon=ft.icons.SAVE,
            on_click=lambda e: self.salvarReg(e,id),
            bgcolor=ft.colors.GREEN_300,
            color=ft.colors.WHITE,
            icon_color=ft.colors.WHITE
        )
        
        
        self.botaoSair_btn = ft.IconButton(
            icon=ft.icons.LOGOUT,
            icon_color=ft.colors.WHITE,
            on_click=self.sair,
            alignment=ft.alignment.top_left
        )
        # Container do card
        pilha = ft.Container(
          
            margin=40,
            padding=20,
            border_radius=15,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            content=ft.Column(
                [
                    ft.Row([
                        self.botaoSair_btn,
                        ft.Text("Dados", 
                           size=24, 
                           weight=ft.FontWeight.BOLD,
                           text_align=ft.TextAlign.CENTER)]),
                    
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    
                    self.tituloStack_input,
                    self.dominioStack_input,
                    self.usuarioStack_input,
                    self.senhaStack_input,
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    
                    self.salvar_btn,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            visible=show,
            alignment=ft.alignment.center,  
            width=float("inf"),
            
        )
        return pilha
    
    def abrir_detalhes(self, id,titulo,dominio, usuario, senha):
        state.show_snackbar(f"Detalhes do {titulo}")
        overlay = self.criarStack(id, titulo,dominio, usuario=usuario, senha=senha,show=True)
        self.main_stack.controls.append(overlay)
        self.content.visible = False
        self.page.update()      

    def copiar(self, conteudo):
        self.page.set_clipboard(conteudo)
    
    def atualizar_grid(self,condicao=False,pesquisa=''):
        """Atualiza o grid com os dados do banco"""
        # 1. Limpar os cards atuais
        self.grid.controls.clear()
        
        sites = self.banco.lerReg(condicao,pesquisa)
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
                on_click=lambda id, title,dominio, usuario, senha: self.abrir_detalhes(id, title,dominio, usuario, senha),
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
            self.adicionar_btn.icon = ft.icons.ADD
            self.adicionar_btn.bgcolor=ft.colors.BLUE_900
            self.adicionar_btn.update()
            self.atualizar_grid()
            
            self.page.update()
        else:
            state.show_snackbar('Erro ao salvar login!')

    def salvarReg(self,e,id):
        novo_titulo=self.tituloStack_input.controls[0].value
        novo_dominio=self.dominioStack_input.controls[0].value
        novo_usuario=self.usuarioStack_input.controls[0].value
        novo_senha=self.senhaStack_input.controls[0].value
        self.banco.update(titulo=novo_titulo,dominio=novo_dominio,usuario=novo_usuario,senha=novo_senha,id=id)
        self.sair(e)
        state.show_snackbar('Registro salvo!!!')
        self.atualizar_grid()
        
    def sair(self, e):  
        self.content.visible = True
        # Remover o overlay da pilha
        if len(self.main_stack.controls) > 1:
            self.main_stack.controls.pop() 
        self.page.update()
    
    def deletar_registro(self, registro_id):
        """Deleta um registro específico"""
        try:
            self.banco.deletarReg(registro_id)
            state.show_snackbar(f"'{registro_id}' deletado com sucesso!")
            self.atualizar_grid() 
        except Exception as e:
            print(f"Erro: {e}")
            state.show_snackbar(f"Erro ao deletar '{registro_id}'")
    
    def pesquisar(self,e):
        pesquisa = self.barra_pesquisa.value
        self.atualizar_grid(True,pesquisa)