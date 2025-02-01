import logging
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

# Configurar o logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def destravar_pdf(input_pdf, senha='515608'):
    logging.info(f"Destravando PDF: {input_pdf}")
    try:
        # Carregar e desbloquear o PDF
        reader = PdfReader(input_pdf)
        reader.decrypt(senha)

        # Criar um novo PDF sem senha
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        # Salvar o PDF desbloqueado em um objeto BytesIO
        output_pdf = BytesIO()
        writer.write(output_pdf)
        output_pdf.seek(0)  # Voltar ao início do BytesIO

        logging.info("PDF desbloqueado com sucesso")
        return output_pdf
    except Exception as e:
        logging.error(f"Falha ao desbloquear o PDF: {e}")
        raise Exception(f"Falha ao desbloquear o PDF: {e}")