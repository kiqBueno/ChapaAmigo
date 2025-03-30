# filepath: /c:/Users/Pornelius Hubert/Documents/GitHub/ChapaAmigo/index.py
import os
import logging
import traceback
from PySimpleGUI import PySimpleGUI as sg
from Processamento import process_pdf

# Função para criar a caixa de diálogo com caixas de seleção
def criar_caixa_selecao(titulo, opcoes):
    layout = [[sg.Checkbox(opcao, key=opcao, default=True)] for opcao in opcoes] + [[sg.Button('OK')]]
    janela = sg.Window(titulo, layout, size=(450, 475))
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
        sg.Column([[sg.Text('Versão: 1.1')]], justification='center', element_justification='center', expand_x=True)
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
    "AUXÍLIO EMERGENCIAL": True,
    "PROCESSOS": True
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
                process_pdf(arquivo, senha, usar_marca_dagua, incluir_contrato, incluir_documentos, grupos_selecionados, foto_path)
            except Exception as e:
                logging.error(f"Erro ao processar o PDF: {e}")
                traceback.print_exc()
                sg.popup(f"Erro ao processar o PDF: {e}")