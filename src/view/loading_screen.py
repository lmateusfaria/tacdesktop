import tkinter as tk
from tkinter import ttk

class LoadingScreen(tk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.create_widgets()
        self.after(3000, self.finish_loading)  # Chama a função de callback após 3 segundos

    def create_widgets(self):
        tk.Label(self, text="Aguarde, carregando...").pack(pady=50)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="indeterminate")
        self.progress.pack(pady=0)
        self.progress.start()

    def finish_loading(self):
        self.progress.stop()  # Para a animação da barra de progresso
        self.callback()  # Chama a função de callback após o carregamento
