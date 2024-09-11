import tkinter as tk
from src.controller.pedidos_brf.index import on_click_contar_pedidos

class PedidosBrfWindow(tk.Frame):
    def __init__(self, parent, session, callback):
        super().__init__(parent)
        self.session = session
        self.callback = callback
        self.create_widgets()

    def create_widgets(self):
        # Define 3 colunas no grid e expande a coluna do meio
        self.grid_columnconfigure(0, weight=1)  # Esquerda
        self.grid_columnconfigure(1, weight=1)  # Meio
        self.grid_columnconfigure(2, weight=1)  # Direita
        
        # Label centralizado com columnspan e sticky
        self.label_titulo = tk.Label(self, text="Download dos Pedidos da BRF", font=("Arial", 16))
        self.label_titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=25, sticky="nsew")

        self.label_data = tk.Label(self, text="Selecione a data:")
        self.label_data.grid(row=1, column=1, padx=0, pady=0)
        
        self.entry_data = tk.Entry(self, takefocus=True)
        self.entry_data.grid(row=2, column=1, padx=0, pady=0)
        
        self.label_resultado = tk.Label(self, text="Quantidade de pedidos: ")
        self.label_resultado.grid(row=3,column=1,pady=10)
        
        self.btn_contar = tk.Button(self, text="Contar Pedidos", command=lambda:on_click_contar_pedidos(self.entry_data,self.label_resultado))
        self.btn_contar.grid(pady=10)
        
        