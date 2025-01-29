import PyPDF2
import fitz  # PyMuPDF
import sys
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Verifica se o nome do arquivo foi passado como argumento
if len(sys.argv) < 13:
    print("Uso: python Cache.py <arquivo_pdf> <usar_marca_dagua> <grupos_selecionados>")
    sys.exit(1)

input_pdf = sys.argv[1]
usar_marca_dagua = sys.argv[2].lower() == 'true'
grupos_selecionados = {
    "CADASTROS BÁSICOS": sys.argv[3].lower() == 'true',
    "RENDA": sys.argv[4].lower() == 'true',
    "HISTÓRICO DA RECEITA FEDERAL": sys.argv[5].lower() == 'true',
    "DADOS DA CTPS": sys.argv[6].lower() == 'true',
    "TITULO ELEITORAL": sys.argv[7].lower() == 'true',
    "DADOS DO PASSAPORTE": sys.argv[8].lower() == 'true',
    "DADOS SOCIAIS": sys.argv[9].lower() == 'true',
    "CELULARES E TELEFONES FIXO": sys.argv[10].lower() == 'true',
    "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA": sys.argv[11].lower() == 'true',
    "AUXÍLIO EMERGENCIAL": sys.argv[12].lower() == 'true'
}

# Função para identificar páginas específicas e salvar como imagem
def save_specific_pages_as_images(pdf_path):
    doc = fitz.open(pdf_path)
    keywords = [
        "Comprovante de Situação Cadastral no CPF",
        "Sistema Nacional de Informações Criminais",
        "Portal do BNMP"
    ]
    
    images = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        
        for keyword in keywords:
            if keyword in text:
                pix = page.get_pixmap()
                img_bytes = BytesIO(pix.tobytes())
                images.append(img_bytes)
                print(f"Saved page {page_num + 1} as image in memory")

    return images

# Salvar páginas específicas como imagens
images = save_specific_pages_as_images(input_pdf)

# Função para criar um PDF com as informações extraídas e adicionar imagens
def create_pdf(data, output_pdf_path, images, usar_marca_dagua=True):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    
    y = height - 40

    def draw_group(title, keys):
        nonlocal y
        # Espaçamento antes do nome do grupo
        y -= 20
        c.drawString(40, y, title)
        y -= 20
        for key in keys:
            if key in data:
                c.drawString(60, y, f"{key}: {data[key]}")  # Adiciona um tab (espaçamento) antes do dado
                y -= 20
                if y < 40:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = height - 40
        # Espaçamento após o nome do grupo
        y -= 20

    # Adicionar marca d'água em cada página
    def add_watermark():
        if usar_marca_dagua:
            c.drawImage('LogoChapaAmigo.png', width - 100, height - 100, width=80, height=80, mask='auto')

    # Grupos de dados
    groups = {
        "CADASTROS BÁSICOS": [
            "Data e Hora", "Nome", "Nascimento", "Idade", "Sexo", "Rg", "Cpf", "CNH", "Mãe", "Pai", "Óbito"
        ],
        "RENDA": [
            "Renda Mensal Presumida"
        ],
        "HISTÓRICO DA RECEITA FEDERAL": [
            "Situação Cadastral", "Inscrito em", "Última Consulta"
        ],
        "DADOS DA CTPS": [
            "CTPS", "Série"
        ],
        "TITULO ELEITORAL": [
            "Título de eleitor"
        ],
        "DADOS DO PASSAPORTE": [
            "Passaporte", "País", "Validade"
        ],
        "DADOS SOCIAIS": [
            "Nis (pis/pasep)", "Nis - outros", "Cns", "Cns - outros", "Inscrição social"
        ],
        "CELULARES E TELEFONES FIXO": [
            "Número"
        ],
        "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA": [
            "Quantidade de Pagamentos", "Valor Total dos Pagamentos"
        ],
        "AUXÍLIO EMERGENCIAL": [
            "Valor total recebido como beneficiário", "Valor total recebido como responsável", "Valor total recebido como benef./resp."
        ]
    }

    for group_title, group_keys in groups.items():
        if grupos_selecionados[group_title]:
            add_watermark()
            draw_group(group_title, group_keys)

    # Adicionar imagens ao PDF
    for img_bytes in images:
        c.showPage()
        add_watermark()
        img = ImageReader(img_bytes)
        c.drawImage(img, 0, 0, width=width, height=height)
    
    c.save()

# Abre o arquivo PDF
with open(input_pdf, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)

    # Extrai o texto de cada página e escreve no arquivo de saída
    with open('temp.txt', 'w', encoding='utf-8') as output_file:
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            output_file.write(f"Page {page_num + 1}:\n{text}\n\n")

# Extrair dados do temp.txt
from InterpretePdf import extract_data_from_text
extracted_data = extract_data_from_text('temp.txt')

# Criar o PDF com as informações extraídas e adicionar imagens
create_pdf(extracted_data, 'Relatorio.pdf', images, usar_marca_dagua)