import logging
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def destravarPdf(inputPdf, password='515608'):
    """
    Unlock a password-protected PDF and return it as a BytesIO object.
    """
    logging.info(f"Unlocking PDF: {inputPdf}")
    try:
        reader = PdfReader(inputPdf)
        reader.decrypt(password)

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        outputPdf = BytesIO()
        writer.write(outputPdf)
        outputPdf.seek(0)
        logging.info("PDF unlocked successfully")
        return outputPdf
    except Exception as e:
        logging.error(f"Failed to unlock PDF: {e}")
        raise