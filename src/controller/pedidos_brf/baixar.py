import os
from pathlib import Path
from datetime import date, datetime
import re
import threading
from tkinter import messagebox
from imap_tools import MailBox, AND
from src.controller.pedidos_brf.emailpedidos import usuario, senha

# Função para gerenciar o contador de cliques diários
def gerenciar_contador_diario():
    contador_path = Path('tacdesktop') / 'data' / f'contador.txt'
    
    # Se o arquivo de contagem não existir, cria e inicializa com o dia de hoje e contador 0
    if not contador_path.exists():
        with open(contador_path, 'w') as f:
            f.write(f"{date.today()},1")
        return 1
    
    # Se o arquivo existir, lê os dados
    with open(contador_path, 'r') as f:
        conteudo = f.read()
        data_salva, contagem = conteudo.split(',')
        data_salva = datetime.strptime(data_salva, "%Y-%m-%d").date()
        contagem = int(contagem)
        
        # Se for um novo dia, zera o contador
        if data_salva != date.today():
            contagem = 0
    
    # Incrementa a contagem e salva novamente no arquivo
    contagem += 1
    with open(contador_path, 'w') as f:
        f.write(f"{date.today()},{contagem}")
    
    return contagem

# Função para baixar os pedidos
def baixar_pedidos(dia, hora_inicio):
    data = date.today()
    nova_data = data.replace(day=dia)
    ano_atual = nova_data.year
    mes_atual = nova_data.month
    dia_atual = nova_data.day
    
    # Gerenciar o contador diário
    qnt_vezes = gerenciar_contador_diario()

    caminho = criar_diretorio_pedidos(ano_atual, mes_atual, dia_atual, qnt_vezes)
    bp = 0

    # Entrando na caixa de email via IMAP
    with MailBox('imap.terra.com').login(usuario, senha) as caixaEntrada:
        # Buscar e-mails recebidos na data especificada
        for email in caixaEntrada.fetch(AND(date=nova_data, seen=True), reverse=False, mark_seen=True):
            # Verificar se o e-mail foi recebido após a hora de início
            if email.date.time() >= hora_inicio:
                # Verificar se o email possui anexo maior que 0 byte
                if len(email.attachments) > 0:
                    # Percorre os anexos do email
                    for anexo in email.attachments:
                        # Verificar se o nome do anexo contém "Novo Pedido"
                        if "Novo Pedido" in anexo.filename:
                            informações_anexo = anexo.payload
                            nomeArquivo = anexo.filename
                            nomeArquivoPDF = re.sub(':', '', nomeArquivo)
                            
                            # Aqui corrigimos para salvar no caminho completo
                            caminho_completo = caminho / nomeArquivoPDF
                            
                            # Salva o arquivo na pasta correta
                            with open(caminho_completo, "wb") as arquivo_pdf:
                                arquivo_pdf.write(informações_anexo)
                            bp += 1
                        
    return bp

# Função que será executada em uma thread para evitar congelar a interface
def baixar_pedidos_thread(entry_dia, label_resultado, entry_hora_inicio):
    try:
        # Validação do dia
        dia = int(entry_dia.get())
        if dia < 1 or dia > 31:
            raise ValueError("O dia deve estar entre 1 e 31.")
        
        # Chama a função de baixar pedidos
        pedidos_baixados = baixar_pedidos(dia, entry_hora_inicio)
        
        # Atualiza o label de resultado com a quantidade de pedidos baixados
        label_resultado.config(text=f"Pedidos baixados: {pedidos_baixados}")
    
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

# Função que será chamada ao clicar no botão de baixar pedidos
def on_click_baixar_pedidos(entry_data, label_resultado, entry_hora_inicio):
    # Atualiza a interface indicando que o processo está em andamento
    label_resultado.config(text="Baixando pedidos...")
    
    # Inicia uma nova thread para não congelar a interface
    threading.Thread(target=baixar_pedidos_thread, args=(entry_data, label_resultado, entry_hora_inicio), daemon=True).start()

# Função para criar o diretório de pedidos
def criar_diretorio_pedidos(ano, mes, dia, qnt_vezes):
    # Define o caminho base
    base_path = Path('tacdesktop') / 'data' / 'pdf_pedidos_brf'
    
    # Define o caminho completo com ano, mês, dia e quantidade de cliques
    diretorio_pedidos = base_path / str(ano) / str(mes).zfill(2) / str(dia).zfill(2) / f"{qnt_vezes}x"
    
    # Verifica se o diretório existe, se não, cria
    if not diretorio_pedidos.exists():
        diretorio_pedidos.mkdir(parents=True, exist_ok=True)
        print(f'Diretório criado: {diretorio_pedidos}')
    else:
        print(f'Diretório já existe: {diretorio_pedidos}')
    
    return diretorio_pedidos
