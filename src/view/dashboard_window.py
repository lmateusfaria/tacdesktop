import tkinter as tk
from src.view.usuario.cadastro_window import CadastroWindow
from src.view.pedidos_brf.index import PedidosBrfWindow


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
        # Configura a grid para expandir adequadamente
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Título do Dashboard (centralizado)
        self.title_label = tk.Label(self, text=f"Bem-vindo, {self.username.title()}!", font=("Arial", 18))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="ew")
        
        # Botões de funcionalidades baseados nas permissões
        button_width = 20  # Define uma largura padrão para os botões
        
        if 'admin' in self.funcoes_acesso:
            self.function1_button = tk.Button(self, text="Cadastrar Usuário", command=self.show_cadastro_window, width=button_width)
            self.function1_button.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        if 'user' in self.funcoes_acesso or 'admin' in self.funcoes_acesso:
            self.function2_button = tk.Button(self, text="Pedidos BRF", command=self.function2, width=button_width)
            self.function2_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        if 'luis' in self.funcoes_acesso or 'admin' in self.funcoes_acesso:
            self.function3_button = tk.Button(self, text="Pedidos GS", command=self.function3, width=button_width)
            self.function3_button.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        
        # Botão de logout (centralizado)
        self.logout_button = tk.Button(self, text="Logout", command=self.return_to_main_menu, width=button_width)
        self.logout_button.grid(row=3, column=0, columnspan=2, padx=20, pady=(30, 10), sticky="ew")

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
        """Exibe a tela de Pedidos BRF."""
        print("Imprimir Pedidos BRF")
        self.clear_screen()  # Remove o conteúdo atual da tela
        pedidos_brf_window = PedidosBrfWindow(self, self.session, self.return_to_dashboard)  # Passa a sessão aqui
        pedidos_brf_window.grid(row=0, column=0, sticky="nsew")
        
    def function3(self):
        """Exibe a tela de Pedidos GS."""
        print("Imprimir Pedidos GS")
        self.clear_screen()  # Remove o conteúdo atual da tela
        pedidos_brf_window = PedidosBrfWindow(self, self.session, self.return_to_dashboard)  # Passa a sessão aqui
        pedidos_brf_window.grid(row=0, column=0, sticky="nsew")
        
    def clear_screen(self):
        """Remove todos os widgets da tela."""
        for widget in self.winfo_children():
            widget.destroy()
