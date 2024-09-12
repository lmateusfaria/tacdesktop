import tkinter as tk
import socket
from src.controller.usuario.controller import LoginController
from src.model.database import get_session

class LoginFrame(tk.Frame):
    def __init__(self, parent, show_loading_screen):
        super().__init__(parent)
        self.show_loading_screen = show_loading_screen

        # Configuração do layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Label e entrada para usuário
        self.username_label = tk.Label(self, text="Usuário")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.username_entry = tk.Entry(self, takefocus=False)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w",)

        # Label e entrada para senha
        self.password_label = tk.Label(self, text="Senha")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Botão de login
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, column=1, sticky="n")
        
        # Label de mensagem
        self.message_label = tk.Label(self, text="")
        self.message_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="n")

        # Centraliza o Frame dentro do Container
        self.place(relx=0.5, rely=0.5, anchor="center")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Obter o IP local do usuário
        ip_login = socket.gethostbyname(socket.gethostname())
        
        controller = LoginController()  # Cria uma instância do controlador
        success, funcoes_acesso = controller.verify_user(username, password, ip_login)
        
        if success:
            self.message_label.config(text="Login realizado com sucesso!")
            
            # Obter uma nova sessão do banco de dados
            session = get_session()

            # Passar a session junto com os outros parâmetros
            self.after(1000, lambda: self.show_loading_screen(username, funcoes_acesso, session))  # Exibe a tela de carregamento
        else:
            self.message_label.config(text="Usuário ou senha incorretos.")
