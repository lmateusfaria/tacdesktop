import tkinter as tk
from tkinter import messagebox
from src.controller.usuario import controller 

class CadastroWindow(tk.Frame):
    def __init__(self, parent, session, return_to_dashboard):
        super().__init__(parent)
        self.session = session
        self.return_to_dashboard = return_to_dashboard
        
        # Elementos da interface de cadastro
        self.label_username = tk.Label(self, text="Nome de Usuário")
        self.label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = tk.Label(self, text="Senha")
        self.label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.label_funcoes_acesso = tk.Label(self, text="Funções de Acesso (opcional)")
        self.label_funcoes_acesso.grid(row=2, column=0, padx=10, pady=10)
        self.entry_funcoes_acesso = tk.Entry(self)
        self.entry_funcoes_acesso.grid(row=2, column=1, padx=10, pady=10)

        self.btn_cadastrar = tk.Button(self, text="Cadastrar", command=self.cadastrar)
        self.btn_cadastrar.grid(row=3, column=1, pady=20)
        
        self.back_button = tk.Button(self, text="Voltar", command=self.return_to_dashboard)
        self.back_button.grid(row=3, column=0)

    def cadastrar(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        funcoes_acesso = self.entry_funcoes_acesso.get() or 'usuario'
        
        if not username or not password:
            messagebox.showerror("Erro", "Nome de usuário e senha são obrigatórios!")
            return

        try:
            # Não passe a sessão aqui, apenas os parâmetros necessários
            if controller.create_user(username, password, funcoes_acesso):
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.entry_username.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
                self.entry_funcoes_acesso.delete(0, tk.END)
            else:
                messagebox.showerror("Erro", "Usuário já existe!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")
