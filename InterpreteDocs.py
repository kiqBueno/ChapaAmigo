import PyPDF2
from pdf2image import convert_from_path

def process_pdf(input_pdf):
    titles = [
        "SITUAÇÃO CADASTRAL DO CPF - RECEITA FEDERAL",
        "CERTIDÃO DE ANTECEDENTES CRIMINAIS - POLÍCIA FEDERAL",
        "BANCO NACIONAL DE MANDADOS DE PRISÃO - CNJ"
    ]

    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()

            if any(title in text for title in titles):
                images = convert_from_path(input_pdf, first_page=page_num + 1, last_page=page_num + 1)
                for i, image in enumerate(images):
                    image.save(f'page_{page_num + 1}.png', 'PNG')
                print(f"Página {page_num + 1} salva como imagem.")