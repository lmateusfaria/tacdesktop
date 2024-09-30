import os

# Caminho para a pasta que contém as subpastas de 2024
path = './data/pdf_pedidos_brf/2024'

def find_first_pdf_in_subfolders(path):
    first_pdfs = {}
    # Percorrer o diretório e subdiretórios
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.pdf'):
                if root not in first_pdfs:  # Se ainda não salvamos um PDF desta pasta
                    first_pdfs[root] = os.path.join(root, file)
                    break  # Parar a busca nesta subpasta depois de encontrar o primeiro PDF

    return first_pdfs

# Chamando a função e imprimindo os resultados
first_pdfs = find_first_pdf_in_subfolders(path)
for folder, pdf_path in first_pdfs.items():
    print(f"Pasta: {folder}, Primeiro PDF: {pdf_path}")

# Opcional: Salvar os caminhos em um arquivo de texto
with open('caminhos_dos_pdfs.txt', 'w') as f:
    for folder, pdf_path in first_pdfs.items():
        f.write(f"Pasta: {folder}, Primeiro PDF: {pdf_path}\n")
