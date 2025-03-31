import os
import logging
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from app.imageUtils import cropImage, addTransparency
import fitz  # PyMuPDF

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def saveSpecificPagesAsImages(pdfPath, pdfPassword):
    """
    Extract specific pages from a PDF containing certain keywords and save them as images in memory.
    """
    logging.info("Saving specific pages as images")
    doc = fitz.open(pdfPath)
    if doc.needs_pass:
        doc.authenticate(pdfPassword)
    keywords = ["Comprovante de Situação Cadastral no CPF", "Sistema Nacional de Informações Criminais", "Portal do BNMP"]
    images = []
    for pageNum in range(len(doc)):
        page = doc.load_page(pageNum)
        text = page.get_text()
        if any(keyword in text for keyword in keywords):
            pix = page.get_pixmap(dpi=300)
            imgBytes = BytesIO(pix.tobytes())
            images.append(imgBytes)
            logging.info(f"Saved page {pageNum + 1} as image in memory")
    return images

def createPdf(data, outputPdfPath, images, useWatermark=True, photoPath=None, includeContract=False, includeDocuments=False, selectedGroups=None):
    """
    Create a PDF with extracted data and optional images, watermark, and customization.
    """
    logging.info(f"Creating PDF: {outputPdfPath}")
    c = canvas.Canvas(outputPdfPath, pagesize=letter)
    width, height = letter
    pdfmetrics.registerFont(TTFont('Calibri', 'calibri.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))
    c.setFont("Calibri", 12)
    y = height - 40

    def drawGroup(title, keys):
        nonlocal y
        y -= 20
        c.drawString(40, y, title)
        y -= 20
        if title == "PROCESSOS":
            singleOccurrenceKeys = [
                "Total de Processos", "Como Requerente", "Como Requerido", "Como Outra Parte",
                "Nos Últimos 30 Dias", "Nos Últimos 90 Dias", "Nos Últimos 180 Dias", "Nos Últimos 365 Dias"
            ]
            for key in singleOccurrenceKeys:
                if key in data:
                    c.setFont("Calibri-Bold", 12)
                    c.drawString(60, y, f"{key}:")
                    c.setFont("Calibri", 12)
                    textWidth = c.stringWidth(f"{key}: ", "Helvetica-Bold", 12)
                    text = str(data[key]) if data[key] is not None else ''
                    lines = []
                    while text:
                        if c.stringWidth(text, "Calibri", 12) <= width - 80 - textWidth:
                            lines.append(text)
                            break
                        else:
                            for j in range(len(text), 0, -1):
                                if c.stringWidth(text[:j], "Calibri", 12) <= width - 80 - textWidth:
                                    lines.append(text[:j])
                                    text = text[j:].lstrip()
                                    break
                    for line in lines:
                        c.drawString(60 + textWidth + 10, y, line)
                        y -= 20
                        if y < 40:
                            c.showPage()
                            c.setFont("Calibri", 12)
                            y = height - 40
            y -= 20

            maxLength = max(len(data[key]) for key in keys if key in data and isinstance(data[key], list))
            for i in range(maxLength):
                for key in keys:
                    if key in data and isinstance(data[key], list) and i < len(data[key]):
                        c.setFont("Calibri-Bold", 12)
                        c.drawString(60, y, f"{key}:")
                        c.setFont("Calibri", 12)
                        textWidth = c.stringWidth(f"{key}: ", "Helvetica-Bold", 12)
                        text = str(data[key][i]) if data[key][i] is not None else ''
                        lines = []
                        while text:
                            if c.stringWidth(text, "Calibri", 12) <= width - 80 - textWidth:
                                lines.append(text)
                                break
                            else:
                                for j in range(len(text), 0, -1):
                                    if c.stringWidth(text[:j], "Calibri", 12) <= width - 80 - textWidth:
                                        lines.append(text[:j])
                                        text = text[j:].lstrip()
                                        break
                        for line in lines:
                            c.drawString(60 + textWidth + 10, y, line)
                            y -= 20
                            if y < 40:
                                c.showPage()
                                c.setFont("Calibri", 12)
                                y = height - 40
                y -= 20
        else:
            for key in keys:
                if key in data:
                    c.setFont("Calibri-Bold", 12)
                    c.drawString(60, y, f"{key}:")
                    c.setFont("Calibri", 12)
                    textWidth = c.stringWidth(f"{key}: ", "Helvetica-Bold", 12)
                    text = data[key]
                    if isinstance(text, list):
                        text = [str(item) if item is not None else '' for item in text]
                        text = " ".join(text)
                    else:
                        text = str(text) if text is not None else ''
                    lines = []
                    while text:
                        if c.stringWidth(text, "Calibri", 12) <= width - 80 - textWidth:
                            lines.append(text)
                            break
                        else:
                            for i in range(len(text), 0, -1):
                                if c.stringWidth(text[:i], "Calibri", 12) <= width - 80 - textWidth:
                                    lines.append(text[:i])
                                    text = text[i:].lstrip()
                                    break
                    for line in lines:
                        c.drawString(60 + textWidth + 10, y, line)
                        y -= 20
                        if y < 40:
                            c.showPage()
                            c.setFont("Calibri", 12)
                            y = height - 40
            y -= 20

    def addWatermark():
        if useWatermark:
            c.saveState()
            c.translate(width / 2, height / 2)
            c.rotate(45)
            logoImgBytes = addTransparency(os.path.join(os.path.dirname(__file__), 'Files', 'LogoChapaAmigo.png'), 0.05)
            img = ImageReader(logoImgBytes)
            c.drawImage(img, -250, -125, width=500, height=250, mask='auto')
            c.restoreState()

    if photoPath:
        try:
            img = ImageReader(photoPath)
            c.drawImage(img, width - 150, height - 200, width=100, height=150)
        except Exception as e:
            logging.error(f"Error loading image: {e}")

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
        "AUXÍLIO EMERGENCIAL": ["Valor total recebido como beneficiário", "Valor total recebido como responsável", "Valor total recebido como benef./resp."],
        "PROCESSOS": ["Número do Processo", "Tipo", "Status", "Papel", "Valor da Causa", "Envolvidos", "Assunto", "Tribunal", "Data de Abertura", "Idade em Dias", "Última Atualização", "Data de Encerramento", "Última Movimentação"]
    }

    for groupTitle, groupKeys in groups.items():
        if selectedGroups and selectedGroups.get(groupTitle, False):
            addWatermark()
            drawGroup(groupTitle, groupKeys)

    if includeDocuments:
        for imgBytes in images:
            c.showPage()
            addWatermark()
            croppedImgBytes = cropImage(imgBytes)
            img = ImageReader(croppedImgBytes)
            c.drawImage(img, 0, 0, width=width, height=height)
    
    c.save()