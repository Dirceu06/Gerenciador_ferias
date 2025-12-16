import flet as ft
from app.ui.app_state import state

def main(page: ft.Page):
    page.title = "Gerenciador de senhas"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.maximized=True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.min_width = 800 
    page.window.min_height = 600
    #configura o estado globala
    state.set_page(page)
    
    #rotas
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
        elif e.route == "/lixeira":
            from app.ui.pages.lixeira_page import Historico
            lixo = Historico(page)
            page.views.append(lixo.build())
        
        page.update()
    page.on_resized = lambda e: page.update()
    page.on_route_change = route_change

    page.go("/")
    #route_change(ft.RouteChangeEvent(route="/", data="/"))

if __name__ == "__main__":
    ft.app(target=main)
