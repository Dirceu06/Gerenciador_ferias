import flet as ft
from app.ui.app_state import state  # Importa o estado global

class LoginPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.build_ui()
    
    def build_ui(self):
        """Constrói a interface de login"""
        # Campos de entrada
        self.user_input = ft.TextField(
            label="Usuário",
            width=250,
            autofocus=True,
            prefix_icon=ft.icons.PERSON
        )
        
        self.pass_input = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            width=250,
            prefix_icon=ft.icons.LOCK
        )
        
        # Botão de login
        self.login_btn = ft.ElevatedButton(
            "Entrar",
            icon=ft.icons.LOGIN,
            on_click=self.tentar_login,  # Método separado!
            width=250,
            height=45
        )
        
        # Container do card
        self.card_login = ft.Container(
            width=350,
            margin=40,
            padding=20,
            border_radius=15,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            content=ft.Column(
                [
                    ft.Text("Login", 
                           size=24, 
                           weight=ft.FontWeight.BOLD,
                           text_align=ft.TextAlign.CENTER),
                    
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    
                    self.user_input,
                    self.pass_input,
                    
                    ft.Container(height=10),
                    
                    self.login_btn,
                    
                    # Link para "esqueci senha" (futuro)
                    ft.TextButton(
                        "Esqueci a senha",
                        on_click=lambda e: state.show_snackbar("Funcionalidade em desenvolvimento!"),
                        icon=ft.icons.HELP_OUTLINE
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )
        
        # View completa
        self.view = ft.View(
            route="/",
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    expand=True,
                    content=self.card_login)
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    def build(self):
        """Retorna a view pronta"""
        return self.view
    
    def tentar_login(self, e):
        usuario = self.user_input.value
        senha = self.pass_input.value
        
        #print(f"DEBUG: Tentando login - Usuário: {usuario}, Senha: {senha}")
        
        # Lógica simples de validação (igual você tinha)
        if usuario == "admin" and senha == "123":
            state.show_snackbar("✅ Login realizado com sucesso!")
            
            # Navega para a próxima página
            self.page.go("/home")
        else:
            state.show_snackbar("❌ Usuário ou senha incorretos!", is_error=True)
            
            # Limpa os campos de senha
            self.pass_input.value = ""
            self.pass_input.update()