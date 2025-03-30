import os
import logging
import traceback
from PyPDF2 import PdfReader, PdfWriter
from Cache import create_pdf, save_specific_pages_as_images
from InterpretePdf import extract_data_from_pdf
from reportlab.lib.pagesizes import letter

def process_pdf(arquivo, senha, usar_marca_dagua, incluir_contrato, incluir_documentos, grupos_selecionados, foto_path):
    """
    Process the selected PDF and generate a customized report.
    """
    try:
        extracted_data = extract_data_from_pdf(arquivo, senha)
        with open(os.path.join(os.path.dirname(__file__), 'Files', 'cache.txt'), 'w', encoding='utf-8') as output_file:
            for key, value in extracted_data.items():
                output_file.write(f"{key}: {value}\n")

        images = save_specific_pages_as_images(arquivo, senha)
        nome_pessoa = extracted_data.get("Nome", "Relatorio").replace(" ", "_")
        output_dir = os.path.join(os.path.dirname(__file__), 'Relatórios')
        os.makedirs(output_dir, exist_ok=True)
        output_pdf_path = os.path.join(output_dir, f"Relatorio_{nome_pessoa}.pdf")

        create_pdf(
            extracted_data, output_pdf_path, images, usar_marca_dagua, foto_path,
            incluir_contrato, incluir_documentos, grupos_selecionados
        )

        if incluir_contrato:
            termo_pdf_path = os.path.join(os.path.dirname(__file__), 'Files', 'TERMO_FICHA_CADASTRO_PDF.pdf')
            with open(termo_pdf_path, 'rb') as termo_file, open(output_pdf_path, 'rb') as output_file:
                termo_reader = PdfReader(termo_file)
                output_reader = PdfReader(output_file)
                writer = PdfWriter()
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
                output_reader = PdfReader(output_file)
                writer = PdfWriter()
                for page in output_reader.pages:
                    writer.add_page(page)
                writer.encrypt(user_password="1234", owner_password="1234", use_128bit=True)
                with open(output_pdf_path, 'wb') as final_output_file:
                    writer.write(final_output_file)

        logging.info(f"PDF protegido gerado: {output_pdf_path} com senha: 1234")
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
        traceback.print_exc()
        raise
