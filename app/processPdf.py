import os
import logging
import traceback
from PyPDF2 import PdfReader, PdfWriter
from app.pdfUtils import createPdf, saveSpecificPagesAsImages
from app.extractPdfData import extractDataFromPdf
from reportlab.lib.pagesizes import letter

def processPdf(file, password, useWatermark, includeContract, includeDocuments, selectedGroups, photoPath):
    """
    Process the selected PDF and generate a customized report.
    """
    try:
        extractedData = extractDataFromPdf(file, password)
        with open(os.path.join(os.path.dirname(__file__), 'Files', 'cache.txt'), 'w', encoding='utf-8') as outputFile:
            for key, value in extractedData.items():
                outputFile.write(f"{key}: {value}\n")

        images = saveSpecificPagesAsImages(file, password)
        personName = extractedData.get("Nome", "Relatorio").replace(" ", "_")
        outputDir = os.path.join(os.path.dirname(__file__), 'Relatórios')
        os.makedirs(outputDir, exist_ok=True)
        outputPdfPath = os.path.join(outputDir, f"Relatorio_{personName}.pdf")

        createPdf(
            extractedData, outputPdfPath, images, useWatermark, photoPath,
            includeContract, includeDocuments, selectedGroups
        )

        if includeContract:
            termPdfPath = os.path.join(os.path.dirname(__file__), 'Files', 'TERMO_FICHA_CADASTRO_PDF.pdf')
            with open(termPdfPath, 'rb') as termFile, open(outputPdfPath, 'rb') as outputFile:
                termReader = PdfReader(termFile)
                outputReader = PdfReader(outputFile)
                writer = PdfWriter()
                width, height = letter
                termPage = termReader.pages[0]
                termPage.scale_to(width, height)
                writer.add_page(termPage)
                for page in termReader.pages[1:]:
                    writer.add_page(page)
                for page in outputReader.pages:
                    writer.add_page(page)
                writer.encrypt(user_password="1234", owner_password="1234", use_128bit=True)
                with open(outputPdfPath, 'wb') as finalOutputFile:
                    writer.write(finalOutputFile)
        else:
            with open(outputPdfPath, 'rb') as outputFile:
                outputReader = PdfReader(outputFile)
                writer = PdfWriter()
                for page in outputReader.pages:
                    writer.add_page(page)
                writer.encrypt(user_password="1234", owner_password="1234", use_128bit=True)
                with open(outputPdfPath, 'wb') as finalOutputFile:
                    writer.write(finalOutputFile)

        logging.info(f"Protected PDF generated: {outputPdfPath} with password: 1234")
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
        traceback.print_exc()
        raise
