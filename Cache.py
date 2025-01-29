import PyPDF2
import sys
import os

# Verifica se o nome do arquivo foi passado como argumento
if len(sys.argv) < 2:
    print("Uso: python Cache.py <arquivo_pdf>")
    sys.exit(1)

input_pdf = sys.argv[1]

# Abre o arquivo PDF
with open(input_pdf, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)

    # Cria o arquivo de saída
    with open('temp.txt', 'w', encoding='utf-8') as output_file:
        # Extrai o texto de cada página e escreve no arquivo de saída
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            output_file.write(f"Page {page_num + 1}:\n{text}\n\n")