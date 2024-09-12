import tkinter as tk
from src.view.usuario.login_window import LoginFrame
from src.view.dashboard_window import DashboardWindow
from src.view.loading_screen import LoadingScreen

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill="both", expand=True)
        self.show_login_frame()

    def show_login_frame(self):
        """Exibe o frame de login."""
        self.clear_screen()
        login_frame = LoginFrame(self, self.show_loading_screen)
        login_frame.pack(fill="both", expand=True)

    def show_loading_screen(self, username, funcoes_acesso, session):
        """Exibe a tela de carregamento antes de redirecionar para o dashboard."""
        self.clear_screen()  # Remove o conteúdo atual da tela
        loading_screen = LoadingScreen(self, lambda: self.show_dashboard(username, funcoes_acesso, session))
        loading_screen.pack(fill="both", expand=True)

    def show_dashboard(self, username, funcoes_acesso, session):
        """Mostra a tela de dashboard e maximiza a janela."""
        self.clear_screen()  # Remove a tela de carregamento
        dashboard = DashboardWindow(self, session, username, funcoes_acesso, self.show_login_frame)
        dashboard.pack(fill="both", expand=True)

        # Configurações para maximizar e permitir redimensionamento
        self.parent.geometry("600x400")  # Tamanho padrão para o dashboard
        self.parent.title("TAC Etiquetas")  # Titulo do App
        self.parent.resizable(True, True)  # Permite redimensionamento
        self.parent.update_idletasks()  # Atualiza a janela para aplicar as mudanças

    def clear_screen(self):
        """Remove todos os widgets da tela."""
        for widget in self.winfo_children():
            widget.destroy()

    def return_to_main_menu(self):
        """Volta para a tela de login e restaura configurações da janela principal."""
        self.clear_screen()  # Limpa a tela atual
        self.show_login_frame()  # Exibe o frame de login

        # Configurações para restaurar a janela principal
        self.parent.geometry("350x200")  # Tamanho fixo para a tela de login
        self.parent.resizable(False, False)  # Não permite redimensionamento
        self.parent.update_idletasks()  # Atualiza a janela para aplicar as mudanças
