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

medidas_brf = [
    "45X230","230X45","230X45MM",
    #ADESIVAS
    "250X100", "100X250",
    "240X170",
    "100X230", "230X100",
    "220X100","100X220"
    "100X210", "210X100",
    
    "210X70", "70X210",
    "200X104",
    "200X85", "85X200",
    "200X75", "75X200",
    "180X70",
    "180X80",
    
    "95X60", "60X95",
    "165X85", "85X165",
    "110X85", "85X110","85X110MM",
    "140X50",
    "70X50",
    "70X80",
    "60X61",
    "45X60", "60X45",
    "30X40",
    "190X90",
    "240X75",
    "150X70",
    "280X220",
    "75X75",
    
    
    #PEAD
    "100X220",
    "148X110",
    "125X80", "80X125",
    "125X65", "65X125",
    "045X232",
    "26X28",
]

# Dicionário de cidades e CNPJs
cidades = {
    ("BURITI ALEGRE/GO", "01.838.723/0350-01"): "BRF/Buriti Alegre(Up391)",
    ("CAMPOS NOVOS/SC", "01.838.723/0309-72"): "BRF/C. Novos(Up316)160",
    ("CAPINZAL/SC", "01.838.723/0154-00"): "BRF/Capinzal (Up312)466",
    ("CARAMBEI/PR", "01.838.723/0118-38"): "BRF/Carambei (Up350) 424",
    ("CHAPECO/SC", "01.838.723/0339-98"): "BRF/Chapecó(Up358)104",
    ("CONCORDIA/SC", "01.838.723/0338-07"): "BRF/ Concórdia(Up343)",
    ("DOIS VIZINHOS/PR", "01.838.723/0370-47"): "BRF/Dois Vizinhos(382)1985",
    ("DOURADOS/MS", "01.838.723/0067-53"): "BRF/Dourados(Up 380)18",
    ("DUQUE DE CAXIAS/RJ", "01.838.723/0413-11"): "BRF/Duque Caxias (Up1625)",
    ("DUQUE DE CAXIAS/RJ", "01.838.723/0334-83"): "BRF/Duque Caxias (Up876)",
    ("FRANCISCO BELTRAO/PR", "01.838.723/0369-03"): "BRF/Fsco Beltrao(Up378)2518",
    ("FRANCISCO BELTRAO/PR", "01.838.723/0112-42"): "BRF/Fsco Beltrao(Up202)",
    ("GARIBALDI/RS", "01.838.723/0349-60"): "BRF/Garibaldi (Up386)",
    ("HERVAL D'OESTE/SC", "01.838.723/0153-10"): "BRF/Herval D Oeste (Up 310)140",
    ("JATAI/GO", "01.838.723/0188-40"): "BRF/Jatai (Up349)4011",
    ("LAJEADO/RS", "01.838.723/0425-55"): "BRF/Lajeado Min (Up383) 1661",
    ("LAJEADO/RS", "01.838.723/0047-00"): "BRF/Lajeado (Up328) 1449/3975",
    ("LUCAS DO RIO VERDE/MT", "01.838.723/0394-14"): "BRF/ Lucas R. Verde(387)3515",
    ("MARAU/RS", "01.838.723/0248-16"): "BRF/Marau Holding(Up323)",
    ("MARAU/RS", "01.838.723/0251-11"): "BRF/Marau(Up321)2014",
    ("MARAU/RS", "01.838.723/0241-40"): "BRF/Marau Suinos(Up320)",
    ("MINEIROS/GO", "01.838.723/0182-55"): "BRF/Mineiros(Up335)1010",
    ("NOVA MARILANDIA/MT", "01.838.723/0286-41"): "BRF/Marilandia(Up381)2675",
    ("NOVA MUTUM/MT", "01.838.723/0494-87"): "BRF/Mutum (Up879)",
    ("PONTA GROSSA/PR", "01.838.723/0362-37"): "BRF/Ponta Grossa(375)928",
    ("RIO VERDE/GO", "01.838.723/0172-83"): "BRF/Rio Verde(Up331)1001",
    ("SERAFINA CORRÊA/RS", "01.838.723/0256-26"): "BRF/Serafina(Up322)103",
    ("SEROPEDICA/RJ", "01.838.723/0472-71"): "BRF/Seropedica(Up299)",
    ("TATUI/SP", "01.838.723/0451-47"): "BRF/Tatui(Up392)10",
    ("TOLEDO/PR", "01.838.723/0376-32"): "BRF/Toledo(Up355)716",
    ("TOLEDO/PR", "01.838.723/0422-02"): "BRF/Toledo(Up237)",
    ("UBERLANDIA/MG", "01.838.723/0438-70"): "BRF/Uber.(Up376)3681",
    ("UBERLANDIA/MG", "01.838.723/0430-12"): "BRF/Uber.Aves(Up377)121",
    ("UBERLANDIA/MG", "01.838.723/0443-37"): "BRF/Uberlandia - 3278",
    ("VIDEIRA/SC", "01.838.723/0213-96"): "BRF/Videira",
    ("VIDEIRA/SC", "01.838.723/0224-49"): "BRF/Videira (Up300)87",
    ("VITORIA DE SANTO ANTAO/PE", "01.838.723/0346-17"): "BRF/Vitoria S.At(390)2999",
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
        "BELTRAO/PR": "FRANCISCO BELTRAO/PR",
        "VIZINHOS/PR": "DOIS VIZINHOS/PR",
        "ALEGRE/GO": "BURITI ALEGRE/GO",
        "GROSSA/PR": "PONTA GROSSA/PR",
        "CAXIAS/RJ": "DUQUE DE CAXIAS/RJ"
        # Adicione outras substituições se necessário
    }
    return substituicoes.get(cidade_cliente, cidade_cliente)

def formatar_data(data):
    """Formatar a data DD.MM.AAAA para AAAA-MM-DD."""
    dia, mes, ano = data.split(".")
    return f"{ano}-{mes}-{dia}"

def definir_pasta_destino(material_pedido, medida_pedido):
    """Define a pasta de destino baseada no material e medida."""
    if any(mat in material_pedido for mat in ["AA01","AA13", "ADESIVA"]):
        if (re.search("250X100",medida_pedido) or re.search("100X250",medida_pedido)):
            return"./TRANST 250X100"    
        elif (re.search("240X170",medida_pedido) or re.search("170X240",medida_pedido)):
            return"./TRANST 240X170"
        elif (re.search("210X100",medida_pedido) or re.search("100X210",medida_pedido)):
            return"./TRANST 210X100"
        elif (re.search("230X100",medida_pedido) or re.search("100X230",medida_pedido)):
            return"./TRANST 230X100"    
        elif (re.search("210X70",medida_pedido) or re.search("70X210",medida_pedido)):
            return"./TRANST 210X70"
        elif (re.search("200X104",medida_pedido) or re.search("104X200",medida_pedido)):
            return"./TRANST 210X70"
        elif (re.search("200X85",medida_pedido) or re.search("85X200",medida_pedido)):
            return"./TRANST 200X85"
        elif (re.search("200X75",medida_pedido) or re.search("75X200",medida_pedido)):
            return"./TRANST 200X75"
        elif (re.search("180X70",medida_pedido) or re.search("70X180",medida_pedido)):
            return"./TRANST 180X70"
        elif (re.search("180X80",medida_pedido) or re.search("80X180",medida_pedido)):
            return"./TRANST 180X80"
        elif (re.search("95X60",medida_pedido) or re.search("60X95",medida_pedido)):
            return"./TRANST 95X60"
        elif (re.search("165X85",medida_pedido) or re.search("85X165",medida_pedido)):
            return"./TRANST 165X85"
        elif (re.search("110X85",medida_pedido) or re.search("85X110",medida_pedido)):
            return"./TRANST 110X85"
        elif (re.search("140X50",medida_pedido) or re.search("50X140",medida_pedido)):
            return"./TRANST 140X50"
        elif (re.search("70X50",medida_pedido) or re.search("50X70",medida_pedido)):
            return"./TRANST 70X50"     
        elif (re.search("70X80",medida_pedido) or re.search("80X70",medida_pedido)):
            return"./TRANST 70X80"     
        elif (re.search("60X61",medida_pedido) or re.search("60X61",medida_pedido)):
            return"./TRANST 60X61"        
        elif (re.search("45X60",medida_pedido) or re.search("60X45",medida_pedido)):
            return"./TRANST 45X60"
        elif (re.search("30X40",medida_pedido) or re.search("40X30",medida_pedido)):
            return"./TRANST 30X40"
        elif (re.search("190X90",medida_pedido) or re.search("90X190",medida_pedido)):
            return"./TRANST 190X90"
        elif (re.search("240X75",medida_pedido) or re.search("75X240",medida_pedido)):
            return"./TRANST 240X75"
        elif (re.search("150X70",medida_pedido) or re.search("150X70",medida_pedido)):
            return"./TRANST 150X70"
        elif (re.search("75X75",medida_pedido) or re.search("75X75",medida_pedido)):
            return"./TRANST 75X75"
        elif (re.search("280X220",medida_pedido) or re.search("220X280",medida_pedido)):
            return"./TRANST 280X220"
        elif (re.search("26X28",medida_pedido) or re.search("28X26",medida_pedido)):
            return"./TRANST 26X28"
        else: return "./OUTROS"
        
    elif any(mat in material_pedido for mat in ["NA01","NA02", "NA"]):
        if (re.search("230X45",medida_pedido) or re.search("45X230",medida_pedido) or re.search("230X45MM",medida_pedido)):
            return "./PEAD 230X45"
        elif (re.search("230X100",medida_pedido) or re.search("100X230",medida_pedido)):
            return "./PEAD 230X100"
        elif (re.search("220X100",medida_pedido) or re.search("100X220",medida_pedido)):
            return "./PEAD 220X100"
        elif (re.search("125X80",medida_pedido) or re.search("80X125",medida_pedido)):
            return "./PEAD 125X80"
        elif (re.search("125X65",medida_pedido) or re.search("65X125",medida_pedido)):
            return "./PEAD 125X65"
        elif (re.search("148X110",medida_pedido) or re.search("110X148",medida_pedido)):
            return "./PEAD 148X110"
        else: return "./OUTROS"
    
    elif any(mat in material_pedido for mat in ["AA08","AA07"]):
        if (re.search("250X100",medida_pedido) or re.search("100X250",medida_pedido)):
            return "./BOPP 230X100"    
        elif (re.search("240X170",medida_pedido) or re.search("170X240",medida_pedido)):
            return "./BOPP 240X170"
        elif (re.search("230X100",medida_pedido) or re.search("100X230",medida_pedido)):
            return "./BOPP 230X100"    
        elif (re.search("210X70",medida_pedido) or re.search("70X210",medida_pedido)):
            return "./BOPP 210X70"
        elif (re.search("200X104",medida_pedido) or re.search("104X200",medida_pedido)):
            return "./BOPP 210X70"
        elif (re.search("200X85",medida_pedido) or re.search("85X200",medida_pedido)):
            return "./BOPP 200X85"
        elif (re.search("200X75",medida_pedido) or re.search("75X200",medida_pedido)):
            return "./BOPP 200X75"
        elif (re.search("180X70",medida_pedido) or re.search("70X180",medida_pedido)):
            return "./BOPP 180X70"
        elif (re.search("95X60",medida_pedido) or re.search("60X95",medida_pedido)):
            return "./BOPP 95X60"
        elif (re.search("165X85",medida_pedido) or re.search("85X165",medida_pedido)):
            return "./BOPP 165X85"
        elif (re.search("110X85",medida_pedido) or re.search("85X110",medida_pedido)):
            return "./BOPP 110X85"
        elif (re.search("140X50",medida_pedido) or re.search("50X140",medida_pedido)):
            return "./BOPP 140X50"
        elif (re.search("70X50",medida_pedido) or re.search("50X70",medida_pedido)):
            return "./BOPP 70X50"        
        elif (re.search("60X61",medida_pedido) or re.search("60X61",medida_pedido)):
            return "./TRANST 60X61"        
        elif (re.search("45X60",medida_pedido) or re.search("60X45",medida_pedido)):
            return "./BOPP 45X60"
        elif (re.search("30X40",medida_pedido) or re.search("40X30",medida_pedido)):
            return "./BOPP 30X40"
        elif (re.search("190X90",medida_pedido) or re.search("90X190",medida_pedido)):
            return "./BOPP 190X90"
        elif (re.search("240X75",medida_pedido) or re.search("75X240",medida_pedido)):
            return "./BOPP 240X75"
        elif (re.search("150X70",medida_pedido) or re.search("150X70",medida_pedido)):
            return "./BOPP 150X70"
        elif (re.search("75X75",medida_pedido) or re.search("75X75",medida_pedido)):
            return "./BOPP 75X75"
        
        else: return "./OUTROS"
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
        data_atual = datetime.strptime(entry_data.get(), "%d/%m/%Y")
        dia = data_atual.day
        caminho_pdfs = f"./data/pdf_pedidos_brf/{datetime.year}/{datetime.month}/{dia}"
        
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