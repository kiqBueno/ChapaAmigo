from PySimpleGUI import PySimpleGUI as sg

def criarCaixaSelecao(title, options):
    """
    Create a dialog box with checkboxes.
    """
    layout = [[sg.Checkbox(option, key=option, default=True)] for option in options] + [[sg.Button('OK')]]
    window = sg.Window(title, layout, size=(450, 475))
    event, values = window.read()
    window.close()
    return values
