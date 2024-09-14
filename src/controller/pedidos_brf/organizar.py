import os
import re
import shutil
import logging
from pypdf import PdfReader
from datetime import datetime
from tkinter import Toplevel, Text, Scrollbar,messagebox
import threading

# Configurando o logging
logging.basicConfig(filename="organizacao_pdfs.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Lista de materiais e medidas
material = ["NA", "NA01", "NA02", "AA01", "AA07", "AA08", "AA13", "ADESIVA"]
medidas_brf = ["45X230", "230X45", "250X100", "100X250", "240X170", "100X230", 
               "220X100", "100X220", "100X210", "210X100", "210X70", "70X210", 
               "200X104", "200X85", "85X200", "180X70", "95X60", "60X95", "45X60", 
               "190X90", "240X75", "75X75", "100X220", "148X110"]

# Dicionário de cidades e CNPJs
cidades = {
    ("BURITI ALEGRE/GO", "01.838.723/0350-01"): "BRF/Buriti Alegre(Up391)",
    ("CAMPOS NOVOS/SC", "01.838.723/0309-72"): "BRF/C. Novos(Up316)160",
    # Adicione as outras cidades conforme necessário...
}

# Funções auxiliares
def encontrar_material(descricao):
    """Busca materiais na descrição usando regex."""
    padrao_material = re.compile(r'\b(?:' + '|'.join(material) + r')\b')
    return padrao_material.findall(descricao)

def encontrar_medidas(descricao):
    """Busca medidas na descrição usando regex."""
    padrao_medidas = re.compile(r'\b(?:' + '|'.join(medidas_brf) + r')\b')
    return padrao_medidas.findall(descricao)

def listar_pdfs(caminho):
    """Listar todos os arquivos PDF no diretório."""
    return [f for f in os.listdir(caminho) if f.lower().endswith('.pdf')]

def encontrar_padrao_numerico(texto, padrao):
    """Encontrar padrões numéricos como CPP ou número de pedido."""
    padrao_re = re.compile(padrao)
    return padrao_re.findall(texto)

def mover_arquivo(origem, destino):
    """Mover arquivo para a pasta destino, criando-a se necessário."""
    if not os.path.exists(destino):
        os.makedirs(destino)
    shutil.move(origem, destino)

def ajustar_nome_cidade(cidade_cliente):
    """Ajusta os nomes de cidades conforme necessário."""
    substituicoes = {
        "OESTE/SC": "HERVAL D'OESTE/SC",
        "NOVOS/SC": "CAMPOS NOVOS/SC",
        "CORREA/RS": "SERAFINA CORRÊA/RS",
        "VERDE/MT": "LUCAS DO RIO VERDE/MT",
        "VERDE/GO": "RIO VERDE/GO",
        "BELTRAO/PR": "FRANCISCO BELTRAO/PR"
        # Adicione outras substituições se necessário
    }
    return substituicoes.get(cidade_cliente, cidade_cliente)

def formatar_data(data):
    """Formatar a data DD.MM.AAAA para AAAA-MM-DD."""
    dia, mes, ano = data.split(".")
    return f"{ano}-{mes}-{dia}"

def definir_pasta_destino(material_pedido, medida_pedido):
    """Define a pasta de destino baseada no material e medida."""
    if any(mat in material_pedido for mat in ["AA01", "ADESIVA"]):
        if "250X100" in medida_pedido:
            return "./TRANST 250X100"
        elif "240X170" in medida_pedido:
            return "./TRANST 240X170"
        # Adicione outras condições conforme necessário
    return "./OUTROS"

# Função principal de organização
def organizar_pedidos(caminho_pdfs, entry_dia):
    """Organiza os PDFs na pasta fornecida de acordo com o conteúdo."""
    lista_pedidos = listar_pdfs(caminho_pdfs)
    padrao_data = r'\b\d{2}\.\d{2}\.\d{4}\b'
    linha0010 = "0010  "
    total_processados = 0
    log_retorno = []
    
    for pedido in lista_pedidos:
        try:
            pdf_pedido = PdfReader(os.path.join(caminho_pdfs, pedido))
            pagina0 = pdf_pedido.pages[0]
            texto_pedido = pagina0.extract_text(extraction_mode="layout")

            descricao_curta = encontrar_material(texto_pedido)
            numero_pedido = encontrar_padrao_numerico(texto_pedido, r'\b\d{9}\b')[0]
            cnpj_cliente = encontrar_padrao_numerico(texto_pedido, r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}')
            cidade_cliente = encontrar_padrao_numerico(texto_pedido, r'[A-ZÀ-ÿa-z]+/[A-Z]{2}')
            medida_pedido = encontrar_medidas(texto_pedido)

            # Verificação e ajustes em cidades
            cidade_cliente = ajustar_nome_cidade(cidade_cliente)

            # Montagem do novo nome de arquivo
            data_pedido = encontrar_padrao_numerico(texto_pedido, padrao_data)[0]
            data_formatada = formatar_data(data_pedido)
            novo_nome_pedido = f"{cidade_cliente}_{numero_pedido}_{data_formatada}.pdf"
            caminho_novo_arquivo = os.path.join(caminho_pdfs, novo_nome_pedido)

            # Mover arquivo para nova pasta com base no material/medida
            pasta_destino = definir_pasta_destino(material, medida_pedido)
            mover_arquivo(os.path.join(caminho_pdfs, pedido), os.path.join(pasta_destino, novo_nome_pedido))

            # Log do sucesso
            logging.info(f"Arquivo '{pedido}' processado com sucesso e movido para {pasta_destino}")
            log_retorno.append(f"Processado: {novo_nome_pedido} -> {pasta_destino}")
            total_processados += 1

        except Exception as e:
            # Log do erro
            logging.error(f"Erro ao processar '{pedido}': {str(e)}")
            log_retorno.append(f"Erro ao processar '{pedido}': {str(e)}")

    # Resumo do processamento
    relatorio = f"Total de arquivos processados: {total_processados}/{len(lista_pedidos)}"
    log_retorno.append(relatorio)
    logging.info(relatorio)

    return log_retorno

# Função para exibir relatório de organização
def exibir_relatorio(log_retorno):
    """Exibe o relatório de organização dos PDFs em uma nova janela."""
    janela_relatorio = Toplevel()
    janela_relatorio.title("Relatório de Organização")

    text_area = Text(janela_relatorio, wrap="word", height=20, width=60)
    scrollbar = Scrollbar(janela_relatorio, command=text_area.yview)
    text_area.config(yscrollcommand=scrollbar.set)

    for log in log_retorno:
        text_area.insert("end", log + "\n")
    text_area.config(state="disabled")  # Tornar o texto somente leitura
    text_area.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Função para organizar os pedidos em uma thread
def organizar_pedidos_thread(entry_data, label_resultado):
    try:
        data_atual = datetime.now()
        data_atual.day = entry_data
        dia = datetime.strptime(entry_data.get(), "%d/%m/%Y").day
        caminho_pdfs = f"./pdfs_a_organizar/{dia}"
        1
        # Organizar os PDFs e obter o log de retorno
        log_retorno = organizar_pedidos(caminho_pdfs, data_atual)
        label_resultado.config(text="Organização concluída.")
        
        # Exibir o relatório de organização ao final
        exibir_relatorio(log_retorno)
    
    except ValueError as e:
        messagebox.showerror("Erro", f"Data inválida: {str(e)}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

# Função que será chamada pelo botão de organizar
def on_click_organizar_pedidos(entry_data, label_resultado):
    label_resultado.config(text="Organizando pedidos...")
    threading.Thread(target=organizar_pedidos_thread, args=(entry_data, label_resultado), daemon=True).start()
