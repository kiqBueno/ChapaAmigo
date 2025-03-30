import logging
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def destravar_pdf(input_pdf, senha='515608'):
    """
    Unlock a password-protected PDF and return it as a BytesIO object.
    """
    logging.info(f"Unlocking PDF: {input_pdf}")
    try:
        reader = PdfReader(input_pdf)
        reader.decrypt(senha)

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        output_pdf = BytesIO()
        writer.write(output_pdf)
        output_pdf.seek(0)
        logging.info("PDF unlocked successfully")
        return output_pdf
    except Exception as e:
        logging.error(f"Failed to unlock PDF: {e}")
        raise