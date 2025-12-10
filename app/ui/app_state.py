import flet as ft
from typing import Optional, Dict, Any

class AppState:
    """SINGLETON"""
    
    _instance: Optional['AppState'] = None
    _page: Optional[ft.Page] = None
    
    # Dados da aplicação
    current_user: Optional[dict] = None
    games: list = []
    alerts: list = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @property
    def page(self) -> ft.Page:
        if self._page is None:
            raise ValueError("pagina não criada, chamar set_page antes!!!.")
        return self._page
    
    def set_page(self, page: ft.Page):
        """Define a página uma vez no início"""
        self._page = page
    
    # Métodos utilitários
    def show_snackbar(self, message: str, is_error: bool = False):
        """Mostra snackbar em qualquer lugar"""
        color = ft.colors.RED_400 if is_error else ft.colors.GREEN_400
        snack = ft.SnackBar(
            ft.Text(message, color=ft.colors.WHITE),
            bgcolor=color,
            duration=500
        )
        self.page.show_snack_bar(snack)
        self.page.update()
    
    def navigate_to(self, route: str):
        """Navega para uma rota"""
        self.page.go(route)
    
    def show_loading(self, show: bool = True):
        """Mostra/esconde loading"""
        # Implemente seu overlay de loading
        pass

# Instância global
state = AppState()