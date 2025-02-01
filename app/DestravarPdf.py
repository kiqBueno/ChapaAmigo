from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def destravar_pdf(input_pdf, senha='515608'):
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

        print("PDF desbloqueado com sucesso")
        return output_pdf
    except Exception as e:
        raise Exception(f"Falha ao desbloquear o PDF: {e}")