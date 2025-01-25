from PyPDF2 import PdfReader, PdfWriter

def destravar_pdf(input_pdf, output_pdf, senha='515608'):
    # Carregar e desbloquear o PDF
    reader = PdfReader(input_pdf)
    reader.decrypt(senha)

    # Criar um novo PDF sem senha
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"Arquivo desbloqueado salvo como: {output_pdf}")