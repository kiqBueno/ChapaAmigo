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
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import encodings

# Verifica se o nome do arquivo foi passado como argumento
if len(sys.argv) < 17:
    print("Uso: python Cache.py <arquivo_pdf> <senha_pdf> <usar_marca_dagua> <foto_path> <incluir_contrato> <incluir_documentos> <CADASTROS BÁSICOS> <RENDA> <HISTÓRICO DA RECEITA FEDERAL> <DADOS DA CTPS> <TITULO ELEITORAL> <DADOS DO PASSAPORTE> <DADOS SOCIAIS> <CELULARES E TELEFONES FIXO> <PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUada> <AUXÍLIO EMERGENCIAL>")
    sys.exit(1)

input_pdf = sys.argv[1]
senha_pdf = sys.argv[2]
usar_marca_dagua = sys.argv[3].lower() == 'true'
foto_path = sys.argv[4] if sys.argv[4] else None
incluir_contrato = sys.argv[5].lower() == 'true'
incluir_documentos = sys.argv[6].lower() == 'true'

grupos_selecionados = {
    "CADASTROS BÁSICOS": sys.argv[7].lower() == 'true',
    "RENDA": sys.argv[8].lower() == 'true',
    "HISTÓRICO DA RECEITA FEDERAL": sys.argv[9].lower() == 'true',
    "DADOS DA CTPS": sys.argv[10].lower() == 'true',
    "TITULO ELEITORAL": sys.argv[11].lower() == 'true',
    "DADOS DO PASSAPORTE": sys.argv[12].lower() == 'true',
    "DADOS SOCIAIS": sys.argv[13].lower() == 'true',
    "CELULARES E TELEFONES FIXO": sys.argv[14].lower() == 'true',
    "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA": sys.argv[15].lower() == 'true',
    "AUXÍLIO EMERGENCIAL": sys.argv[16].lower() == 'true',
}

# Função para identificar páginas específicas e salvar como imagem
def save_specific_pages_as_images(pdf_path, senha_pdf):
    doc = fitz.open(pdf_path)
    if doc.needs_pass:
        doc.authenticate(senha_pdf)
    keywords = ["Comprovante de Situação Cadastral no CPF", "Sistema Nacional de Informações Criminais", "Portal do BNMP"]
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        for keyword in keywords:
            if keyword in text:
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
images = save_specific_pages_as_images(input_pdf, senha_pdf)

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
    pdfmetrics.registerFont(TTFont('Calibri', 'calibri.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))
    c.setFont("Calibri", 12)
    y = height - 40

    def draw_group(title, keys):
        nonlocal y
        y -= 20
        c.drawString(40, y, title)
        y -= 20
        for key in keys:
            if key in data:
                c.setFont("Calibri-Bold", 12)
                c.drawString(60, y, f"{key}:")
                c.setFont("Calibri", 12)
                text_width = c.stringWidth(f"{key}: ", "Helvetica-Bold", 12)
                text = data[key]
                if isinstance(text, list):
                    text = " ".join(text)
                lines = []
                while text:
                    if c.stringWidth(text, "Calibri", 12) <= width - 80 - text_width:
                        lines.append(text)
                        break
                    else:
                        for i in range(len(text), 0, -1):
                            if c.stringWidth(text[:i], "Calibri", 12) <= width - 80 - text_width:
                                lines.append(text[:i])
                                text = text[i:].lstrip()
                                break
                for line in lines:
                    c.drawString(60 + text_width + 10, y, line)
                    y -= 20
                    if y < 40:
                        c.showPage()
                        c.setFont("Calibri", 12)
                        y = height - 40
        y -= 20

    def add_watermark():
        if usar_marca_dagua:
            c.saveState()
            c.translate(width / 2, height / 2)
            c.rotate(45)
            logo_img_bytes = add_transparency(os.path.join(os.path.dirname(__file__), 'Files', 'LogoChapaAmigo.png'), 0.05)
            img = ImageReader(logo_img_bytes)
            c.drawImage(img, -250, -125, width=500, height=250, mask='auto')
            c.restoreState()

    if foto_path:
        try:
            img = ImageReader(foto_path)
            c.drawImage(img, width - 150, height - 200, width=100, height=150)
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

    groups = {
        "CADASTROS BÁSICOS": ["Data e Hora", "Nome", "Nascimento", "Idade", "Sexo", "Rg", "Cpf", "CNH", "Mãe", "Pai", "Óbito", "Endereços"],
        "RENDA": ["Renda Mensal Presumida"],
        "HISTÓRICO DA RECEITA FEDERAL": ["Situação Cadastral", "Inscrito em", "Última Consulta"],
        "DADOS DA CTPS": ["CTPS", "Série"],
        "TITULO ELEITORAL": ["Título de eleitor"],
        "DADOS DO PASSAPORTE": ["Passaporte", "País", "Validade"],
        "DADOS SOCIAIS": ["Nis (pis/pasep)", "Nis - outros", "Cns", "Cns - outros", "Inscrição social"],
        "CELULARES E TELEFONES FIXO": ["Número"],
        "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA": ["Quantidade de Pagamentos", "Valor Total dos Pagamentos"],
        "AUXÍLIO EMERGENCIAL": ["Valor total recebido como beneficiário", "Valor total recebido como responsável", "Valor total recebido como benef./resp."]
    }

    for group_title, group_keys in groups.items():
        if grupos_selecionados[group_title]:
            add_watermark()
            draw_group(group_title, group_keys)

    if incluir_documentos:
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
    reader.decrypt(senha_pdf)
    num_pages = len(reader.pages)

    # Extrai o texto de cada página e escreve no arquivo de saída
    with open(os.path.join(os.path.dirname(__file__), 'Files', 'temp.txt'), 'w', encoding='utf-8') as output_file:
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            output_file.write(f"Page {page_num + 1}:\n{text}\n\n")

# Extrair dados do temp.txt
from InterpretePdf import extract_data_from_text
extracted_data = extract_data_from_text(os.path.join(os.path.dirname(__file__), 'Files', 'temp.txt'))

# Criar o PDF com nome específico e senha
nome_pessoa = extracted_data.get("Nome", "Relatorio").replace(" ", "_")
output_dir = os.path.join(os.path.dirname(__file__), 'Relatórios')
os.makedirs(output_dir, exist_ok=True)
output_pdf_path = os.path.join(output_dir, f"Relatorio_{nome_pessoa}.pdf")
create_pdf(extracted_data, output_pdf_path, images, usar_marca_dagua, foto_path)

# Concatenar o documento TERMO_FICHA_CADASTRO_PDF.pdf se incluir_contrato for True
if incluir_contrato:
    termo_pdf_path = os.path.join(os.path.dirname(__file__), 'Files', 'TERMO_FICHA_CADASTRO_PDF.pdf')
    with open(termo_pdf_path, 'rb') as termo_file, open(output_pdf_path, 'rb') as output_file:
        termo_reader = PyPDF2.PdfReader(termo_file)
        output_reader = PyPDF2.PdfReader(output_file)
        writer = PyPDF2.PdfWriter()
        width, height = letter
        termo_page = termo_reader.pages[0]
        termo_page.scale_to(width, height)
        writer.add_page(termo_page)
        for page in termo_reader.pages[1:]:
            writer.add_page(page)
        for page in output_reader.pages:
            writer.add_page(page)
        writer.encrypt(user_password="1234", owner_password="1234", use_128bit=True)
        with open(output_pdf_path, 'wb') as final_output_file:
            writer.write(final_output_file)
else:
    with open(output_pdf_path, 'rb') as output_file:
        output_reader = PyPDF2.PdfReader(output_file)
        writer = PyPDF2.PdfWriter()
        for page in output_reader.pages:
            writer.add_page(page)
        writer.encrypt(user_password="1234", owner_password="1234", use_128bit=True)
        with open(output_pdf_path, 'wb') as final_output_file:
            writer.write(final_output_file)

print(f"PDF final protegido gerado: {output_pdf_path} com senha: 1234")