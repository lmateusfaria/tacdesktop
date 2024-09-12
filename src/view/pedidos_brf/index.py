import tkinter as tk
from tkinter import messagebox
from src.controller.pedidos_brf.contar import on_click_contar_pedidos
from src.controller.pedidos_brf.baixar import on_click_baixar_pedidos
from src.controller.components.placeholderentry import PlaceholderEntry
from datetime import datetime, date, time as dt_time

class PedidosBrfWindow(tk.Frame):
    def __init__(self, parent, session, callback):
        super().__init__(parent)
        self.session = session
        self.callback = callback
        self.create_widgets()

    def create_widgets(self):
        # Configurações da grade para centralizar os elementos
        self.grid_columnconfigure(0, weight=1)  # Esquerda
        self.grid_columnconfigure(1, weight=2)  # Centro (expandido)
        self.grid_columnconfigure(2, weight=1)  # Direita

        # Título centralizado
        self.label_titulo = tk.Label(self, text="Download dos Pedidos da BRF", font=("Arial", 16))
        self.label_titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=25, sticky="nsew")

        # Data e hora (entrada de dados)
        self.label_data = tk.Label(self, text="Selecione a data:")
        self.label_data.grid(row=1, column=1, pady=(0, 5))

        self.entry_data = tk.Entry(self)
        self.entry_data.grid(row=2, column=1, pady=(0, 20))

        self.label_horario = tk.Label(self, text="Selecione a hora inicial:")
        self.label_horario.grid(row=3, column=1, pady=(0, 5))

        # Entradas de hora, minutos e segundos
        self.entry_horas = PlaceholderEntry(self, placeholder="Horas")
        self.entry_horas.grid(row=4, column=0, padx=5, pady=(0, 20))

        self.entry_minutos = PlaceholderEntry(self, placeholder="Minutos")
        self.entry_minutos.grid(row=4, column=1, padx=5, pady=(0, 20))

        self.entry_segundos = PlaceholderEntry(self, placeholder="Segundos")
        self.entry_segundos.grid(row=4, column=2, padx=5, pady=(0, 20))

        # Resultados e botões
        self.label_resultado = tk.Label(self, text="Quantidade de pedidos:")
        self.label_resultado.grid(row=5, column=1, pady=(0, 10))

        self.btn_contar = tk.Button(self, text="Contar Pedidos", command=lambda: self.validate_inputs("contar"))
        self.btn_contar.grid(row=5, column=0, pady=(5, 10))

        self.label_baixados = tk.Label(self, text="Baixados:")
        self.label_baixados.grid(row=6, column=1, pady=(0, 10))

        self.btn_baixar = tk.Button(self, text="Baixar Pedidos", command=lambda: self.validate_inputs("baixar"))
        self.btn_baixar.grid(row=6, column=0, pady=(5, 10))

        self.label_organizados = tk.Label(self, text="Organizados NOT")
        self.label_organizados.grid(row=7, column=1, pady=(0, 10))

        self.btn_organizar = tk.Button(self, text="Organizar Pedidos", command=lambda: self.validate_inputs("organizar"))
        self.btn_organizar.grid(row=7, column=0, pady=(5, 10))

        self.label_impressos = tk.Label(self, text="Impressos: 0")
        self.label_impressos.grid(row=8, column=1, pady=(0, 10))

        self.btn_imprimir = tk.Button(self, text="Imprimir Pedidos", command=lambda: self.validate_inputs("imprimir"))
        self.btn_imprimir.grid(row=8, column=0, pady=(5, 20))

        # Botão de voltar
        self.back_button = tk.Button(self, text="Voltar", command=self.callback)
        self.back_button.grid(row=10, column=0, pady=(20, 10), padx=(20, 10), sticky="w")

    def validate_inputs(self, btn_type):
        """Valida as entradas de data e horário, diferenciando o botão que foi clicado."""
        # Validação da data e horário
        horas = self.entry_horas.get()
        minutos = self.entry_minutos.get()
        segundos = self.entry_segundos.get()

        if not self.validate_time_input(horas, 0, 23, "Horas"):
            return
        if not self.validate_time_input(minutos, 0, 59, "Minutos"):
            return
        if not self.validate_time_input(segundos, 0, 59, "Segundos"):
            return

        self.entry_hora_inicio = dt_time(int(horas), int(minutos), int(segundos))
        
        # Executa ação dependendo do botão clicado
        if btn_type == "contar":
            on_click_contar_pedidos(self.entry_data, self.label_resultado, self.entry_hora_inicio)
        elif btn_type == "baixar":
            on_click_baixar_pedidos(self.entry_data, self.label_baixados, self.entry_hora_inicio)
        #elif btn_type == "organizar":
            #on_click_organizar_pedidos()
        #elif btn_type == "imprimir":
            #on_click_imprimir_pedidos()
            

    def validate_time_input(self, value, min_value, max_value, field_name):
        """Valida se a entrada de tempo está dentro dos limites especificados."""
        if not value.isdigit():
            messagebox.showerror("Erro", f"{field_name} inválido. Insira um número.")
            return False
        int_value = int(value)
        if not (min_value <= int_value <= max_value):
            messagebox.showerror("Erro", f"{field_name} inválido. Insira um valor entre {min_value} e {max_value}.")
            return False
        return True
