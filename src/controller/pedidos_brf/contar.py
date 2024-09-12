import tkinter as tk
from tkinter import messagebox
from imap_tools import MailBox, AND
from datetime import date, time as dt_time
import datetime as dt
from src.controller.pedidos_brf.emailpedidos import usuario, senha
import threading

def contar_pedidos(dia,hora_inicio):
    contador = 0
    data = date.today()
    nova_data = data.replace(day=dia)

    with MailBox('imap.terra.com').login(usuario, senha) as caixaEntrada:
        for email in caixaEntrada.fetch(AND(date=nova_data, seen=True), reverse=False, mark_seen=True):
            if email.date.time() >= hora_inicio:
                if len(email.attachments) > 0:
                    for anexo in email.attachments:
                        if "Novo Pedido" in anexo.filename:
                            contador += 1
    return contador
def contar_pedidos_thread(entry_dia, label_resultado,entry_hora_inicio):
    try:
        dia = int(entry_dia.get())
        if dia < 1 or dia > 31:
            raise ValueError("O dia deve estar entre 1 e 31.")
        pedidos = contar_pedidos(dia,entry_hora_inicio)
        label_resultado.config(text=f"Quantidade de pedidos: {pedidos}")
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
        
def on_click_contar_pedidos(entry_data, label_resultado, entry_hora_inicio):
    # Inicia uma nova thread para a função de contagem de pedidos
    label_resultado.config(text="Processando...")
    threading.Thread(target=contar_pedidos_thread, args=(entry_data, label_resultado, entry_hora_inicio), daemon=True).start()

