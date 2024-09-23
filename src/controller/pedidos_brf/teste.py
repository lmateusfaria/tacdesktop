import os
import re
import shutil
import logging
from pypdf import PdfReader
from datetime import datetime

# Configuração inicial de logging
logging.basicConfig(filename="organizacao_pdfs.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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
    # Adicione as outras cidades conforme necessário...
}


# Diretório raiz onde os PDFs são armazenados
DIRETORIO_RAIZ = r"C:\Users\Usuario\Desktop\TAC\tacdesktop\data\pdf_pedidos_brf\2024"


# Expressões regulares para encontrar informações relevantes nos PDFs
RE_CIDADE_CNPJ = re.compile(r"(CIDADE: (.*?)/\w{2}) CNPJ: (\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})")
RE_DATA = re.compile(r"DATA: (\d{2}\.\d{2}\.\d{4})")
RE_PEDIDO = re.compile(r"NÚMERO DO PEDIDO: (\d+)")

def processar_pdf(caminho, ano, mes, dia):
    # Adicione sua lógica para processar o PDF aqui
    print(f"Processando {caminho} do dia {dia}/{mes}/{ano}")

def organizar_pdfs(DIRETORIO_RAIZ):
    # Verifica se o diretório raiz existe
    if not os.path.exists(DIRETORIO_RAIZ):
        print(f"O diretório {DIRETORIO_RAIZ} não existe.")
        return

    # Percorre cada ano no diretório raiz
    for ano in os.listdir(DIRETORIO_RAIZ):
        caminho_ano = os.path.join(DIRETORIO_RAIZ, ano)
        if os.path.isdir(caminho_ano):  # Verifica se o caminho do ano é um diretório
            # Percorre cada mês no diretório do ano
            for mes in os.listdir(caminho_ano):
                caminho_mes = os.path.join(caminho_ano, mes)
                if os.path.isdir(caminho_mes):  # Verifica se o caminho do mês é um diretório
                    # Percorre cada dia no diretório do mês
                    for dia in os.listdir(caminho_mes):
                        caminho_dia = os.path.join(caminho_mes, dia)
                        if os.path.isdir(caminho_dia):  # Verifica se o caminho do dia é um diretório
                            # Percorre cada arquivo no diretório do dia
                            for arquivo in os.listdir(caminho_dia):
                                if arquivo.endswith('.pdf'):
                                    caminho_completo = os.path.join(caminho_dia, arquivo)
                                    processar_pdf(caminho_completo, ano, mes, dia)

def definir_destino(cidade, cnpj, data):
    # Define o diretório de destino com base na cidade e CNPJ
    nome_cidade = cidades.get((cidade.upper(), cnpj), "OUTROS")
    data_formatada = formatar_data(data)
    destino = os.path.join("organizados", nome_cidade, data_formatada)
    if not os.path.exists(destino):
        os.makedirs(destino)
    return destino

def formatar_data(data):
    dia, mes, ano = data.split(".")
    return f"{ano}-{mes}-{dia}"

def mover_arquivo(origem, destino):
    shutil.move(origem, os.path.join(destino, os.path.basename(origem)))

# Iniciar o processo de organização
if __name__ == "__main__":
    organizar_pdfs(DIRETORIO_RAIZ)
