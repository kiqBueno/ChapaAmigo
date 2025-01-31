# filepath: /c:/Users/Pornelius Hubert/Documents/GitHub/ChapaAmigo/Interface.py
from PySimpleGUI import PySimpleGUI as sg
from DestravarPdf import destravar_pdf
from InterpretePdf import extract_data_from_text
import subprocess
import traceback
import os
import sys
import encodings

# Função para criar a caixa de diálogo com caixas de seleção
def criar_caixa_selecao(titulo, opcoes):
    layout = [
        [sg.Checkbox(opcao, key=opcao, default=True)] for opcao in opcoes
    ] + [[sg.Button('OK')]]
    janela = sg.Window(titulo, layout, size=(450, 450))  # Define a largura e altura da janela
    evento, valores = janela.read()
    janela.close()
    return valores

# Layout
sg.theme('BlueMono')
layout = [
    [
        sg.Image(
            filename=os.path.join(os.path.dirname(__file__), 'Files', 'LogoChapaAmigo.png'),
            subsample=5
        ),
        sg.Column(
            [
                [
                    sg.Text(
                        'Raspagem de Pdf',
                        justification='right',
                        font=('Helvetica', 15)
                    )
                ]
            ],
            justification='right',
            element_justification='right',
            expand_x=True
        )
    ],
    [sg.VPush()],  # Espaçamento vertical
    [
        sg.Column(
            [
                [sg.Button(
                    'Personalizar Layout do Pdf',
                    size=(20, 2),
                    key='Personalizar'
                ),
                sg.Button(
                    'Inserir Foto',
                    size=(20, 2),
                    key='InserirFoto'
                )]
            ],
            justification='center',
            element_justification='center',
            expand_x=True
        )
    ],
    [sg.Text('', size=(1, 1))],  # Espaçamento vertical reduzido pela metade
    [
        sg.Column(
            [
                [
                    sg.Button(
                        'Selecionar Arquivo',
                        size=(30, 2),
                        font=('Helvetica', 25),
                        border_width=2
                    )
                ]
            ],
            justification='center',
            element_justification='center',
            expand_x=True,
        )
    ],
    [sg.VPush()],  # Espaçamento vertical
    [
        sg.Column(
            [
                [
                    sg.Text('Versão: ' + '1.0')
                ]
            ],
            justification='center',
            element_justification='center',
            expand_x=True
        )
    ]
]

# Janela
janela = sg.Window(
    'Raspagem de Pdf',
    layout,
    size=(800, 400)
)

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
        opcoes = ['Usar Marca d\'água', 'Contrato', 'Documentos'] + list(grupos_selecionados.keys())  # Opções para marca d'água, contrato, documentos e grupos de dados
        selecoes = criar_caixa_selecao('Personalizar Layout do Pdf', opcoes)
        usar_marca_dagua = selecoes.get('Usar Marca d\'água', True)
        incluir_contrato = selecoes.get('Contrato', True)
        incluir_documentos = selecoes.get('Documentos', True)
        for grupo in grupos_selecionados.keys():
            grupos_selecionados[grupo] = selecoes.get(grupo, True)
        print('Opções de Personalização:', selecoes)
    elif evento == 'InserirFoto':
        foto_path = sg.popup_get_file('Selecione a imagem:')
        if foto_path:
            print(f"Imagem selecionada: {foto_path}")
    elif evento == 'Selecionar Arquivo':
        arquivo = sg.popup_get_file('Selecione o arquivo PDF:')
        if arquivo:
            senha = '515608'  # Senha fixa
            try:
                # Chamar o script Cache.py passando o arquivo PDF original e as opções de personalização
                cache_script_path = os.path.join(os.path.dirname(__file__), 'Cache.py')
                subprocess.run([sys.executable, cache_script_path, arquivo, senha, str(usar_marca_dagua), foto_path or "", str(incluir_contrato), str(incluir_documentos)] + [str(grupos_selecionados[grupo]) for grupo in grupos_selecionados], check=True)
                  
                # Extrair dados do temp.txt
                extracted_data = extract_data_from_text('temp.txt')
                
                # Escrever os dados extraídos no arquivo cache.txt
                with open('cache.txt', 'w', encoding='utf-8') as output_file:
                    for key, value in extracted_data.items():
                        output_file.write(f"{key}: {value}\n")
                
                # Nome do arquivo específico e senha
                nome_pessoa = extracted_data.get("Nome", "Relatorio").replace(" ", "_")
                output_pdf_path = f"Relatorio_{nome_pessoa}.pdf"
                
                # Exibir mensagem de confirmação
                sg.popup(f"PDF protegido gerado: {output_pdf_path} com senha: 1234")
                
            except Exception as e:
                print(f"Erro ao processar o PDF: {e}")
                traceback.print_exc()
                sg.popup(f"Erro ao processar o PDF: {e}")