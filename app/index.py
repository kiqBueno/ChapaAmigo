# filepath: /c:/Users/Pornelius Hubert/Documents/GitHub/ChapaAmigo/index.py
import PyPDF2
from PySimpleGUI import PySimpleGUI as sg
from DestravarPdf import destravar_pdf
from InterpretePdf import extract_data_from_pdf
import traceback
import os
import sys
import encodings
from Cache import create_pdf, save_specific_pages_as_images, crop_image, add_transparency
from reportlab.lib.pagesizes import letter

# Função para criar a caixa de diálogo com caixas de seleção
def criar_caixa_selecao(titulo, opcoes):
    layout = [[sg.Checkbox(opcao, key=opcao, default=True)] for opcao in opcoes] + [[sg.Button('OK')]]
    janela = sg.Window(titulo, layout, size=(450, 450))
    evento, valores = janela.read()
    janela.close()
    return valores

# Layout
sg.theme('BlueMono')
layout = [
    [
        sg.Image(filename=os.path.join(os.path.dirname(__file__), './Files', 'LogoChapaAmigo.png'), subsample=5),
        sg.Column([[sg.Text('Raspagem de Pdf', justification='right', font=('Helvetica', 15))]], justification='right', element_justification='right', expand_x=True)
    ],
    [sg.VPush()],
    [
        sg.Column(
            [
                [sg.Button('Personalizar Layout do Pdf', size=(20, 2), key='Personalizar'),
                 sg.Button('Inserir Foto', size=(20, 2), key='InserirFoto')]
            ],
            justification='center', element_justification='center', expand_x=True
        )
    ],
    [sg.Text('', size=(1, 1))],
    [
        sg.Column(
            [[sg.Button('Selecionar Arquivo', size=(30, 2), font=('Helvetica', 25), border_width=2)]],
            justification='center', element_justification='center', expand_x=True
        )
    ],
    [sg.VPush()],
    [
        sg.Column([[sg.Text('Versão: 1.0')]], justification='center', element_justification='center', expand_x=True)
    ]
]

# Janela
janela = sg.Window('Raspagem de Pdf', layout, size=(800, 400))

# Variáveis para armazenar as opções de personalização
usar_marca_dagua = True
incluir_contrato = True
incluir_documentos = True
grupos_selecionados = {
    "CADASTROS BÁSICOS": True,
    "RENDA": True,
    "HISTÓRICO DA RECEITA FEDERAL": True,
    "DADOS DA CTPS": True,
    "TITULO ELEITORAL": True,
    "DADOS DO PASSAPORTE": True,
    "DADOS SOCIAIS": True,
    "CELULARES E TELEFONES FIXO": True,
    "PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA": True,
    "AUXÍLIO EMERGENCIAL": True
}
foto_path = None

# Ler os eventos
while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED:
        break
    elif evento == 'Personalizar':
        opcoes = ['Usar Marca d\'água', 'Contrato', 'Documentos'] + list(grupos_selecionados.keys())
        selecoes = criar_caixa_selecao('Personalizar Layout do Pdf', opcoes)
        usar_marca_dagua = selecoes.get('Usar Marca d\'água', True)
        incluir_contrato = selecoes.get('Contrato', True)
        incluir_documentos = selecoes.get('Documentos', True)
        for grupo in grupos_selecionados.keys():
            grupos_selecionados[grupo] = selecoes.get(grupo, True)
        print('Opções de Personalização:', selecoes)
    elif evento == 'InserirFoto':
        foto_path = sg.popup_get_file('Selecione a imagem:', file_types=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),))
        if foto_path:
            print(f"Imagem selecionada: {foto_path}")
    elif evento == 'Selecionar Arquivo':
        arquivo = sg.popup_get_file('Selecione o arquivo PDF:')
        if arquivo:
            senha = '515608'
            try:
                # Extrair dados do PDF
                extracted_data = extract_data_from_pdf(arquivo, senha)
                with open(os.path.join(os.path.dirname(__file__), 'Files', 'cache.txt'), 'w', encoding='utf-8') as output_file:
                    for key, value in extracted_data.items():
                        output_file.write(f"{key}: {value}\n")
                
                # Salvar páginas específicas como imagens
                images = save_specific_pages_as_images(arquivo, senha)
                
                # Criar o PDF com nome específico e senha
                nome_pessoa = extracted_data.get("Nome", "Relatorio").replace(" ", "_")
                output_dir = os.path.join(os.path.dirname(__file__), 'Relatórios')
                os.makedirs(output_dir, exist_ok=True)
                output_pdf_path = os.path.join(output_dir, f"Relatorio_{nome_pessoa}.pdf")
                
                # Call the Cache.py functions directly
                create_pdf(
                    extracted_data, output_pdf_path, images, usar_marca_dagua, foto_path,
                    incluir_contrato, incluir_documentos, grupos_selecionados
                )
                
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
                
                sg.popup(f"PDF protegido gerado: {output_pdf_path} com senha: 1234")
            except Exception as e:
                print(f"Erro ao processar o PDF: {e}")
                traceback.print_exc()
                sg.popup(f"Erro ao processar o PDF: {e}")