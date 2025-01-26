from PySimpleGUI import PySimpleGUI as sg
from DestravarPdf import destravar_pdf
from InterpretePdf import extract_data_from_text
import subprocess
import traceback

# Função para criar a caixa de diálogo com caixas de seleção
def criar_caixa_selecao(titulo, opcoes):
    layout = [
        [sg.Checkbox(opcao, key=opcao) for opcao in opcoes],
        [sg.Button('OK')]
    ]
    janela = sg.Window(titulo, layout)
    evento, valores = janela.read()
    janela.close()
    return valores

# Layout
sg.theme('BlueMono')
layout = [
    [
        sg.Image(
            filename='./LogoChapaAmigo.png',
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
                [
                    sg.Button(
                        'Dados para Entrada',
                        size=(20, 2)
                    ),
                    sg.Button(
                        'Dados para Saída',
                        size=(20, 2)
                    )
                ]
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

# Ler os eventos
while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED:
        break
    elif evento == 'Dados para Entrada':
        opcoes = ['Opção 1', 'Opção 2', 'Opção 3']  # Substitua com suas opções
        selecoes = criar_caixa_selecao('Selecionar Opções para Interpretação', opcoes)
        print('Seleções para Interpretação:', selecoes)
    elif evento == 'Dados para Saída':
        opcoes = ['Opção A', 'Opção B', 'Opção C']  # Substitua com suas opções
        selecoes = criar_caixa_selecao('Selecionar Opções para Impressão', opcoes)
        print('Seleções para Impressão:', selecoes)
    elif evento == 'Selecionar Arquivo':
        arquivo = sg.popup_get_file('Selecione o arquivo PDF:')
        if arquivo:
            senha = '515608'  # Senha fixa
            try:
                output_pdf = 'desbloqueado.pdf'
                destravar_pdf(arquivo, output_pdf, senha)
                
                # Chamar o script Cache.py passando o arquivo PDF desbloqueado
                subprocess.run(['python', 'Cache.py', output_pdf])
                
                # Extrair dados do rascunho.txt
                extracted_data = extract_data_from_text('rascunho.txt')
                
                # Verificar o valor interno de data
                # print("Dados extraídos:", extracted_data)
                
                # Escrever os dados extraídos no arquivo cache.txt
                with open('cache.txt', 'w', encoding='utf-8') as output_file:
                    for key, value in extracted_data.items():
                        output_file.write(f"{key}: {value}\n")
                
                sg.popup("Dados extraídos e salvos em cache.txt com sucesso!")
            except Exception as e:
                print(f"Erro ao processar o PDF: {e}")
                traceback.print_exc()
                sg.popup(f"Erro ao processar o PDF: {e}")