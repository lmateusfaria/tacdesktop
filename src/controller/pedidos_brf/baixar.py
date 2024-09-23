import os
from pathlib import Path
from datetime import date, datetime
import re
import threading
from tkinter import messagebox, Toplevel, Text, Scrollbar
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
    contador = 1
    while (base_path / f"{ano}/{mes:02}/{dia:02}/{contador}x").exists():
        diretorio_anterior = base_path / f"{ano}/{mes:02}/{dia:02}/{contador}x"
        if (diretorio_anterior / nome_arquivo).exists():
            return True
        contador += 1
    return False

# Função para criar o diretório de pedidos
def criar_diretorio_pedidos(ano, mes, dia):
    base_path = Path('tacdesktop/data/pdf_pedidos_brf')
    contador, diretorio_pedidos, contador_path = gerenciar_contador_diario(base_path, ano, mes, dia)
    return diretorio_pedidos, contador_path, base_path

# Função para baixar os pedidos
# Função para baixar os pedidos
# Função para baixar os pedidos
def baixar_pedidos(dia, hora_inicio):
    nova_data = date.today().replace(day=dia)
    caminho, contador_path, base_path = criar_diretorio_pedidos(nova_data.year, nova_data.month, nova_data.day)
    
    log_file = caminho / "download_log.txt"
    arquivos_baixados = False  # Variável para verificar se houve algum download

    with open(log_file, "w") as log:
        bp = 0
        with MailBox('imap.terra.com').login(usuario, senha) as caixaEntrada:
            for email in caixaEntrada.fetch(AND(date=nova_data, seen=True), reverse=False, mark_seen=True):
                if email.date.time() >= hora_inicio:
                    for anexo in email.attachments:
                        if "Novo Pedido" in anexo.filename:
                            nome_arquivo = re.sub(':', '', anexo.filename)
                            
                            # Verificar se o arquivo já existe em pastas anteriores
                            if arquivo_ja_existe(nome_arquivo, base_path, nova_data.year, nova_data.month, nova_data.day):
                                log.write(f"Arquivo '{nome_arquivo}' já foi baixado anteriormente. Pulando download.\n")
                                continue
                            
                            # Realizar o download do arquivo
                            caminho_completo = caminho / nome_arquivo
                            with open(caminho_completo, "wb") as arquivo_pdf:
                                arquivo_pdf.write(anexo.payload)
                            
                            log.write(f"Arquivo '{nome_arquivo}' baixado com sucesso.\n")
                            arquivos_baixados = True  # Indica que houve um download
                            bp += 1

        # Se nenhum arquivo foi baixado, registrar uma mensagem no log
        if not arquivos_baixados:
            log.write("Nenhum arquivo já baixado teve o download realizado novamente!\n")

        # Mover o arquivo de contagem para a pasta de pedidos
        contador_novo_path = caminho / contador_path.name
        contador_path.rename(contador_novo_path)

    return bp, log_file

# Função para exibir relatório de download
def exibir_relatorio(log_file):
    with open(log_file, "r") as log:
        conteudo = log.read()

    # Criar uma janela para exibir o relatório
    janela_relatorio = Toplevel()
    janela_relatorio.title("Relatório de Download")
    
    # Caixa de texto com scroll para exibir o conteúdo do log
    text_area = Text(janela_relatorio, wrap="word", height=20, width=60)
    scrollbar = Scrollbar(janela_relatorio, command=text_area.yview)
    text_area.config(yscrollcommand=scrollbar.set)
    
    text_area.insert("1.0", conteudo)
    text_area.config(state="disabled")  # Tornar o texto somente leitura
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


# Função que será executada em uma thread para evitar congelar a interface
def baixar_pedidos_thread(entry_dia, label_resultado, entry_hora_inicio):
    try:
        dia = int(entry_dia.get())
        if not (1 <= dia <= 31):
            raise ValueError("O dia deve estar entre 1 e 31.")
        
        pedidos_baixados, log_file = baixar_pedidos(dia, entry_hora_inicio)
        label_resultado.config(text=f"Pedidos baixados: {pedidos_baixados}")
        
        # Exibir o relatório de download ao final
        exibir_relatorio(log_file)
    
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

# Função para iniciar o download de pedidos em uma nova thread
def on_click_baixar_pedidos(entry_data, label_resultado, entry_hora_inicio):
    label_resultado.config(text="Baixando pedidos...")
    threading.Thread(target=baixar_pedidos_thread, args=(entry_data, label_resultado, entry_hora_inicio), daemon=True).start()

#teste branch tac