# dashboard_window.py
import tkinter as tk
from src.view.usuario.cadastro_window import CadastroWindow

class DashboardWindow(tk.Frame):
    def __init__(self, parent, session, username, funcoes_acesso, return_to_main_menu):
        super().__init__(parent)
        self.username = username
        self.funcoes_acesso = funcoes_acesso
        self.return_to_main_menu = return_to_main_menu
        self.session = session  # Armazena a sessão

        self.create_widgets()

    def create_widgets(self):
        """Cria todos os widgets do dashboard."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Título do Dashboard
        self.title_label = tk.Label(self, text=f"Bem-vindo, {self.username.title()}!", font=("Arial", 16))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Botões de funcionalidades baseados nas permissões
        if 'admin' in self.funcoes_acesso:
            self.function1_button = tk.Button(self, text="Cadastrar Usuário", command=self.show_cadastro_window)
            self.function1_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        if 'user' in self.funcoes_acesso:
            self.function2_button = tk.Button(self, text="Funcionalidade 2", command=self.function2)
            self.function2_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Botão de logout
        self.logout_button = tk.Button(self, text="Logout", command=self.return_to_main_menu)
        self.logout_button.grid(row=2, column=0, columnspan=2, pady=20)

    def show_cadastro_window(self):
        """Exibe a tela de cadastro de usuário."""
        self.clear_screen()  # Remove o conteúdo atual da tela
        cadastro_window = CadastroWindow(self, self.session, self.return_to_dashboard)  # Passa a sessão aqui
        cadastro_window.grid(row=0, column=0, sticky="nsew")


    def return_to_dashboard(self):
        """Volta para a tela de dashboard."""
        self.clear_screen()  # Remove a tela de cadastro
        self.create_widgets()  # Recria todos os widgets do dashboard

    def function2(self):
        # Implementar a lógica para a funcionalidade 2
        print("Funcionalidade 2")

    def clear_screen(self):
        """Remove todos os widgets da tela."""
        for widget in self.winfo_children():
            widget.destroy()
