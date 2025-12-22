import flet as ft
import secrets
import string
from app.ui.app_state import state
from app.ui.components.game_card import PasswordCard
from app.core.database.opDB import Banco

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self._arquivoSelecionado)
        self.page.overlay.append(self.file_picker)
        self.banco = Banco()
        self.botao=False
        self.build_ui()
        self.page.on_resize = lambda e: self.page.update()
        
    def _arquivoSelecionado(self, e: ft.FilePickerResultEvent):
        if e.files:
            caminho = e.files[0].path
            self.processarArquivo(caminho)  # função futura
    
    def processarArquivo(self,caminho):
        arq = open(caminho,'r+')
        qtdAdd=0
        cursor=0
        linhas = arq.readlines()
        for linha in linhas:
            cursor+=1
            if linha == linhas[0]: continue
            try:
                linha=linha.strip().split(',')
                nome = linha[0]
                dominio = linha[1]
                login = linha[2]
                senha = linha[3]
                self.inserirNovoReg(nome,dominio,login,senha)
                qtdAdd+=1
            except:
                print(f'erro na linha {cursor} do arquivo!!!')
        arq.close()
        state.show_snackbar(f'{qtdAdd} registros foram adicionados')
    
    def exportarSenhas(self,e):
        arq = open('senhas.csv','w')
        senhas=self.banco.lerReg()
        arq.write('name,url,username,password,note\n')
        for senha in senhas:
            arq.write(f'{senha[1]},{senha[2]},{senha[3]},{senha[4]},\n')
        state.show_snackbar('senhas exportadas com sucesso, verifique a pasta do executavél')
    
    def gerarSenha(self,tamanho=16,maiusculas=True,minusculas=True,numeros=True,simbolos=True):
        caracteres = ""
        if maiusculas: caracteres += string.ascii_uppercase
        if minusculas: caracteres += string.ascii_lowercase
        if numeros: caracteres += string.digits
        if simbolos: caracteres += "!@#$%&*_-+=?"
        if not caracteres:
            raise ValueError("Selecione pelo menos um tipo de caractere")

        senha = ""
        for i in range(tamanho):
            caractere = secrets.choice(caracteres)
            senha += caractere

        return senha
    
    def toggleBotao(self, e='', detalhes=False):
        if not detalhes:
            self.botao = not self.botao
        else:
            self.botao=False
        
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
                on_click=lambda id, title,dominio, usuario, senha: self.abrirDetalhes(id, title, dominio, usuario, senha),
                delete=self.deletarRegistro
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
            on_click=self.toggleBotao,
            alignment=ft.alignment.center_right,
            tooltip='adicionar'
        )
        
        #botão logout
        self.logout_btn = ft.IconButton(
            icon=ft.icons.LOGOUT_OUTLINED,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.RED_700,
            on_click=self.logout,
            alignment=ft.alignment.center_left,
            tooltip='sair'
        )

        #botão lixeira
        self.lixeira = ft.Container(
            content=ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_color=ft.colors.GREY_200,
            bgcolor=ft.colors.GREY_700,
            on_click=self.historico,
            tooltip='ir para lixeira'
        ),margin=ft.margin.only(right=12),alignment=ft.alignment.center_right)
        
        #botão exportar
        self.exportar = ft.Container(
            content=ft.IconButton(
            icon=ft.icons.SAVE_ALT,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN_700,
            on_click=self.exportarSenhas,
            tooltip='exportar em csv'
        ),margin=ft.margin.only(right=12),alignment=ft.alignment.center_right)
        
        #conteudo
        self.content = ft.Container(
            content=ft.Column([
                ft.ResponsiveRow([self.barra_pesquisa],alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(f"Senhas de {self.banco.login}", size=28, weight="bold"),
                self.grid,
                ft.Row([self.logout_btn, ft.Container(expand=True), self.exportar, self.lixeira, self.adicionar_btn],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,spacing=40)
            ], expand=True),
            expand=True,
            padding=20,
            visible=True
        )
        
        self.popUpInserir()  # 1. Criar o popup
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
        
    def popUpInserir(self):
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
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True
        )
        
        self.pop_container = ft.Container(
            content=ft.Column([
                self.titulo_input,
                self.dominio_input,
                self.usuario_input,
                self.senha_input,

                ft.ElevatedButton(
                    "Inserir",
                    icon=ft.icons.UPLOAD,
                    width=250,
                    height=45,
                    on_click=lambda e: self.inserirNovoReg(
                        self.titulo_input.value,
                        self.dominio_input.value,
                        self.usuario_input.value,
                        self.senha_input.value
                    )
                ),
                
                ft.ElevatedButton(
                    "Gerar senha",
                    icon=ft.icons.AUTO_FIX_HIGH,
                    width=250,
                    height=45,
                    tooltip="Gerar senha segura automaticamente",
                    on_click=lambda e: self.gerarSenhaNoCampo()
                ),


                ft.ElevatedButton(
                    "Exportar do Google",
                    icon=ft.icons.ATTACH_FILE,
                    width=250,
                    height=45,
                    on_click=lambda e: self.file_picker.pick_files(
                        allow_multiple=False
                    )
                )
            ]),
            width=280,
            height=460,  # aumentei pra caber tudo
            right=15,
            bottom=80,
            bgcolor=ft.colors.SURFACE_VARIANT,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.OUTLINE),
            visible=self.botao
        )
    
    def gerarSenhaNoCampo(self):
        nova = self.gerarSenha()   # aquela função com secrets
        self.senha_input.value = nova
        self.page.update()
    
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
                    icon_color=ft.colors.GREEN,
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
                    icon_color=ft.colors.GREEN,
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
                    icon_color=ft.colors.GREEN,
                    icon_size=20,
                    on_click=lambda e, s=usuario: self.copiar(s)
                ),
                col={"sm": 1},
                width=120,
                height=40,
               
                padding=ft.padding.only(left=15),
            )
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.senhaStack_input = ft.ResponsiveRow(
            [
                ft.TextField(
                    label="Senha",
                    value=senha,
                    autofocus=True,
                    prefix_icon=ft.icons.LOCK,
                    col={"sm": 8, "md": 9},
                    password=True,
                    can_reveal_password=True,
                ),

                ft.IconButton(
                    icon=ft.icons.AUTO_FIX_HIGH,
                    tooltip="Gerar senha segura",
                    col={"sm": 2, "md": 1},
                    icon_color=ft.colors.BLUE,
                    on_click=lambda e: self.gerarAtualizarSenha(),
                ),

                ft.IconButton(
                    icon=ft.icons.CONTENT_COPY,
                    tooltip="Copiar senha",
                    col={"sm": 2, "md": 1},
                    icon_color=ft.colors.GREEN,
                    on_click=lambda e: self.copiar(
                        self.senhaStack_input.controls[0].value
                    ),
                ),
                
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        #botão de salvar
        self.salvar_btn = ft.ElevatedButton(
            "salvar",
            icon=ft.icons.SAVE,
            on_click=lambda e: self.salvarReg(e,id),
            bgcolor=ft.colors.GREEN_500,
            color=ft.colors.WHITE,
            icon_color=ft.colors.WHITE
        )
        
        
        self.botaoSair_btn = ft.IconButton(
            icon=ft.icons.ARROW_BACK_OUTLINED,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_700,
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
    
    def gerarAtualizarSenha(self):
        nova = self.gerarSenha()
        self.senhaStack_input.controls[0].value = nova
        self.page.update()

    def abrirDetalhes(self, id,titulo,dominio, usuario, senha):
        state.show_snackbar(f"Detalhes do {titulo}")
        overlay = self.criarStack(id, titulo,dominio, usuario=usuario, senha=senha,show=True)
        self.main_stack.controls.append(overlay)
        self.content.visible = False
        self.toggleBotao(detalhes=True)
        self.page.update()      

    def copiar(self, conteudo):
        self.page.set_clipboard(conteudo)
    
    def atualizarGrid(self,condicao=False,pesquisa=''):
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
                on_click=lambda id, title,dominio, usuario, senha: self.abrirDetalhes(id, title,dominio, usuario, senha),
                domain=f"{site['dominio'].lower()}",
                delete=self.deletarRegistro
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
            self.atualizarGrid()
            
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
        self.atualizarGrid()
        
    def sair(self, e):  
        self.content.visible = True
        # Remover o overlay da pilha
        if len(self.main_stack.controls) > 1:
            self.main_stack.controls.pop() 
        self.page.update()
    
    def deletarRegistro(self, registro_id):
        """Mandar para a lixeira um registro específico"""
        try:
            self.banco.deletarReg(registro_id)
            state.show_snackbar(f"'{registro_id}' foi para lixeira!")
            self.atualizarGrid() 
        except Exception as e:
            print(f"Erro: {e}")
            state.show_snackbar(f"Erro ao  mandar '{registro_id}' para a lixeira")
    
    def pesquisar(self,e):
        pesquisa = self.barra_pesquisa.value
        self.atualizarGrid(True,pesquisa)
        
    def logout(self,e):
        self.banco.logout()
        self.page.go("/")
        
    def historico(self,e):
        self.page.go('/lixeira')