import flet as ft
from app.ui.app_state import state

def main(page: ft.Page):
    # Configuração da página
    page.title = "Tracker de preços"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.maximized=True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.min_width = 800 
    page.window.min_height = 600
    page.window.width=1000
    page.window.height=600
    
    # Configura o estado global
    state.set_page(page)
    
    # Sistema de rotas
    def route_change(e):
        #print(f"DEBUG: Navegando para {e.route}")
        page.views.clear()
        
        if e.route == "/":
            from app.ui.pages.login_page import LoginPage
            login_page = LoginPage(page)
            page.views.append(login_page.build())
        elif e.route == "/home":
            from app.ui.pages.home_page import HomePage
            home_page = HomePage(page)
            page.views.append(home_page.build())
        
        page.update()
    page.on_resized = lambda e: page.update()
    page.on_route_change = route_change

    page.go("/")
    #route_change(ft.RouteChangeEvent(route="/", data="/"))

if __name__ == "__main__":
    ft.app(target=main)
