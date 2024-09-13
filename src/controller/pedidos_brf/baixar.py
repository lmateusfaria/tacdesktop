import os
from pathlib import Path
from datetime import date, datetime
import re
import threading
from tkinter import messagebox
from imap_tools import MailBox, AND
from src.controller.pedidos_brf.emailpedidos import usuario, senha

# Função para gerenciar o contador diário e criar a pasta subsequente
def gerenciar_contador_diario(diretorio_base, ano, mes, dia):
    contador_path = diretorio_base / f'contador-{date.today()}.txt'
    
    # Verificar a existência das pastas 1x, 2x, 3x e assim por diante
    contador = 1
    while (diretorio_base / f"{ano}/{mes:02}/{dia:02}/{contador}x").exists():
        contador += 1
    
    diretorio_pedidos = diretorio_base / f"{ano}/{mes:02}/{dia:02}/{contador}x"
    diretorio_pedidos.mkdir(parents=True, exist_ok=True)

    # Criar o arquivo de contagem e armazenar contagem + caminho da pasta
    with open(contador_path, 'w') as f:
        f.write(f"{date.today()},{contador}\n")
        f.write(f"{diretorio_pedidos}")

    return contador, diretorio_pedidos, contador_path

# Função para verificar se o arquivo já foi baixado
def arquivo_ja_existe(nome_arquivo, base_path, ano, mes, dia):
    # Verificar nas pastas anteriores da mesma data (1x, 2x, etc.)
    contador = 1
    while (base_path / f"{ano}/{mes:02}/{dia:02}/{contador}x").exists():
        diretorio_anterior = base_path / f"{ano}/{mes:02}/{dia:02}/{contador}x"
        if (diretorio_anterior / nome_arquivo).exists():
            print(f"Arquivo '{nome_arquivo}' já existe em: {diretorio_anterior}")
            return True
        contador += 1
    return False

# Função para criar o diretório de pedidos
def criar_diretorio_pedidos(ano, mes, dia):
    # Define o caminho base
    base_path = Path('tacdesktop/data/pdf_pedidos_brf')
    
    # Gerenciar o contador diário e criar a pasta adequada
    contador, diretorio_pedidos, contador_path = gerenciar_contador_diario(base_path, ano, mes, dia)
    
    return diretorio_pedidos, contador_path, base_path

# Função para baixar os pedidos
def baixar_pedidos(dia, hora_inicio):
    nova_data = date.today().replace(day=dia)
    
    # Criar o diretório de pedidos com a contagem correta
    caminho, contador_path, base_path = criar_diretorio_pedidos(nova_data.year, nova_data.month, nova_data.day)
    
    bp = 0
    with MailBox('imap.terra.com').login(usuario, senha) as caixaEntrada:
        for email in caixaEntrada.fetch(AND(date=nova_data, seen=True), reverse=False, mark_seen=True):
            if email.date.time() >= hora_inicio:
                for anexo in email.attachments:
                    if "Novo Pedido" in anexo.filename:
                        nome_arquivo = re.sub(':', '', anexo.filename)

                        # Verificar se o arquivo já existe em pastas anteriores
                        if arquivo_ja_existe(nome_arquivo, base_path, nova_data.year, nova_data.month, nova_data.day):
                            print(f"Arquivo '{nome_arquivo}' já foi baixado anteriormente. Pulando download.")
                            continue  # Pula o download se o arquivo já existir

                        caminho_completo = caminho / nome_arquivo
                        with open(caminho_completo, "wb") as arquivo_pdf:
                            arquivo_pdf.write(anexo.payload)
                        bp += 1
    
    # Mover o arquivo de contagem para a pasta de pedidos
    contador_novo_path = caminho / contador_path.name
    contador_path.rename(contador_novo_path)
    
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
