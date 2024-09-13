import os
from pathlib import Path
from datetime import date, datetime
import re
import threading
from tkinter import messagebox
from imap_tools import MailBox, AND
from src.controller.pedidos_brf.emailpedidos import usuario, senha

# Função para gerenciar o contador diário
def gerenciar_contador_diario(diretorio_pedidos):
    contador_path = diretorio_pedidos / f'contador-{date.today()}.txt'
    diretorio_pedidos.mkdir(parents=True, exist_ok=True)

    if not contador_path.exists():
        contagem = 1
    else:
        with open(contador_path, 'r') as f:
            data_salva, contagem = f.read().split(',')
            if datetime.strptime(data_salva, "%Y-%m-%d").date() != date.today():
                contagem = 0
        contagem = int(contagem) + 1

    with open(contador_path, 'w') as f:
        f.write(f"{date.today()},{contagem}")
    
    return contagem

# Função para criar o diretório de pedidos
def criar_diretorio_pedidos(ano, mes, dia, qnt_vezes):
    diretorio_pedidos = Path('tacdesktop/data/pdf_pedidos_brf') / f"{ano}/{mes:02}/{dia:02}/{qnt_vezes}x"
    diretorio_pedidos.mkdir(parents=True, exist_ok=True)
    return diretorio_pedidos

# Função para baixar os pedidos
def baixar_pedidos(dia, hora_inicio):
    nova_data = date.today().replace(day=dia)
    caminho = criar_diretorio_pedidos(nova_data.year, nova_data.month, nova_data.day, gerenciar_contador_diario(Path('tacdesktop/data/pdf_pedidos_brf')))
    
    bp = 0
    with MailBox('imap.terra.com').login(usuario, senha) as caixaEntrada:
        for email in caixaEntrada.fetch(AND(date=nova_data, seen=True), reverse=False, mark_seen=True):
            if email.date.time() >= hora_inicio:
                for anexo in email.attachments:
                    if "Novo Pedido" in anexo.filename:
                        nome_arquivo = re.sub(':', '', anexo.filename)
                        caminho_completo = caminho / nome_arquivo
                        with open(caminho_completo, "wb") as arquivo_pdf:
                            arquivo_pdf.write(anexo.payload)
                        bp += 1
    return bp

# Função para rodar a thread de baixar pedidos
def baixar_pedidos_thread(entry_dia, label_resultado, entry_hora_inicio):
    try:
        dia = int(entry_dia.get())
        if not (1 <= dia <= 31):
            raise ValueError("O dia deve estar entre 1 e 31.")
        
        pedidos_baixados = baixar_pedidos(dia, entry_hora_inicio)
        label_resultado.config(text=f"Pedidos baixados: {pedidos_baixados}")
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

# Função para iniciar o download de pedidos em uma nova thread
def on_click_baixar_pedidos(entry_data, label_resultado, entry_hora_inicio):
    label_resultado.config(text="Baixando pedidos...")
    threading.Thread(target=baixar_pedidos_thread, args=(entry_data, label_resultado, entry_hora_inicio), daemon=True).start()
