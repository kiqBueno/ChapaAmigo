import PyPDF2
import fitz  # PyMuPDF
import sys
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import Color
from PIL import Image

# Verifica se o nome do arquivo foi passado como argumento
if len(sys.argv) < 14:
    print("Uso: python Cache.py <arquivo_pdf> <usar_marca_dagua> <foto_path> <grupos_selecionados>")
    sys.exit(1)

input_pdf = sys.argv[1]
usar_marca_dagua = sys.argv[2].lower() == 'true'
foto_path = sys.argv[3] if sys.argv[3] else None
grupos_selecionados = {
    "CADASTROS BÁSICOS": sys.argv[4].lower() == 'true',
    "RENDA": sys.argv[5].lower() == 'true',
    "HISTÓRICO DA RECEITA FEDERAL": sys.argv[6].lower() == 'true',
    "DADOS DA CTPS": sys.argv[7].lower() == 'true',
    "TITULO ELEITORAL": sys.argv[8].lower() == 'true',
    "DADOS DO PASSAPORTE": sys.argv[9].lower() == 'true',
    "DADOS SOCIAIS": sys.argv[10].lower() == 'true',
    "CELULARES E TELEFONES FIXO": sys.argv[11].lower() == 'true',
    "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA": sys.argv[12].lower() == 'true',
    "AUXÍLIO EMERGENCIAL": sys.argv[13].lower() == 'true'
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
                # Aumentar a resolução da imagem especificando uma DPI maior
                pix = page.get_pixmap(dpi=300)
                img_bytes = BytesIO(pix.tobytes())
                images.append(img_bytes)
                print(f"Saved page {page_num + 1} as image in memory")

    return images

# Função para cortar 10% das imagens em cima e em baixo
def crop_image(img_bytes):
    img = Image.open(img_bytes)
    width, height = img.size
    crop_height = int(height * 0.09)
    cropped_img = img.crop((0, crop_height, width, height - crop_height))
    cropped_img_bytes = BytesIO()
    cropped_img.save(cropped_img_bytes, format='PNG')
    cropped_img_bytes.seek(0)
    return cropped_img_bytes

# Salvar páginas específicas como imagens
images = save_specific_pages_as_images(input_pdf)

# Função para adicionar transparência à imagem
def add_transparency(image_path, transparency):
    img = Image.open(image_path).convert("RGBA")
    alpha = img.split()[3]
    alpha = alpha.point(lambda p: p * transparency)
    img.putalpha(alpha)
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

# Função para criar um PDF com as informações extraídas e adicionar imagens
def create_pdf(data, output_pdf_path, images, usar_marca_dagua=True, foto_path=None):
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
                c.setFont("Helvetica-Bold", 12)
                c.drawString(60, y, f"{key}:")
                c.setFont("Helvetica", 12)
                text_width = c.stringWidth(f"{key}: ", "Helvetica-Bold", 12)
                c.drawString(60 + text_width + 10, y, f"{data[key]}")  # Espaçamento dinâmico antes do dado
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
            # Adicionar marca d'água LogoChapaAmigo.png centralizada e aumentada
            c.saveState()
            c.translate(width / 2, height / 2)
            c.rotate(45)  # Rotacionar a imagem 45 graus
            logo_img_bytes = add_transparency('LogoChapaAmigo.png', 0.05)  # 100% de transparência
            img = ImageReader(logo_img_bytes)
            c.drawImage(img, -250, -125, width=500, height=250, mask='auto')  # Centralizar a imagem
            c.restoreState()

    # Adicionar foto no topo direito da primeira página
    if foto_path:
        img = ImageReader(foto_path)
        c.drawImage(img, width - 150, height - 200, width=100, height=150)

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
        cropped_img_bytes = crop_image(img_bytes)
        img = ImageReader(cropped_img_bytes)
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

# Criar o PDF com nome específico e senha
nome_pessoa = extracted_data.get("Nome", "Relatorio").replace(" ", "_")

output_pdf_path = f"Relatorio_{nome_pessoa}.pdf"
create_pdf(extracted_data, output_pdf_path, images, usar_marca_dagua, foto_path)

# Adicionar senha ao PDF
with open(output_pdf_path, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    writer = PyPDF2.PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Definir a senha do PDF
    writer.encrypt(user_password="1234", owner_password="1234", use_128bit=True)

    with open(output_pdf_path, 'wb') as f_encrypted:
        writer.write(f_encrypted)

print(f"PDF protegido gerado: {output_pdf_path} com senha: 1234")