import os
import logging
import traceback
from PySimpleGUI import PySimpleGUI as sg
from app.utils import criarCaixaSelecao

def runInterface(processPdf):
    """
    Run the GUI interface for the application.
    """
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

    window = sg.Window('Raspagem de Pdf', layout, size=(800, 400))

    # Variables to store customization options
    useWatermark = True
    includeContract = True
    includeDocuments = True
    selectedGroups = {
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
    photoPath = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Personalizar':
            options = ['Usar Marca d\'água', 'Contrato', 'Documentos'] + list(selectedGroups.keys())
            selections = criarCaixaSelecao('Personalizar Layout do Pdf', options)
            useWatermark = selections.get('Usar Marca d\'água', True)
            includeContract = selections.get('Contrato', True)
            includeDocuments = selections.get('Documentos', True)
            for group in selectedGroups.keys():
                selectedGroups[group] = selections.get(group, True)
            print('Customization Options:', selections)
        elif event == 'InserirFoto':
            photoPath = sg.popup_get_file('Selecione a imagem:', file_types=(("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),))
            if photoPath:
                print(f"Selected image: {photoPath}")
        elif event == 'Selecionar Arquivo':
            file = sg.popup_get_file('Selecione o arquivo PDF:')
            if file:
                password = '515608'
                try:
                    processPdf(file, password, useWatermark, includeContract, includeDocuments, selectedGroups, photoPath)
                    sg.popup("PDF processed successfully!")
                except Exception as e:
                    logging.error(f"Error processing the PDF: {e}")
                    traceback.print_exc()
                    sg.popup(f"Error processing the PDF: {e}")
