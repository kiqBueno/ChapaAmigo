import re
import logging
import PyPDF2
import os

# Configurar o logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_data_from_pdf(file_path, senha='515608'):
    logging.info(f"Extraindo dados do arquivo: {file_path}")
    data = {}
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        if reader.is_encrypted:
            reader.decrypt(senha)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Write the extracted text to a file
        output_file_path = os.path.join(os.path.dirname(__file__), 'Files', 'temp.txt')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text)

        def extract(pattern, key, default="ERROR", multiple=False):
            if multiple:
                matches = re.findall(pattern, text)
                data[key] = [match.replace('\n', ' ').strip() if isinstance(match, str) else match[0].replace('\n', ' ').strip() for match in matches] if matches else [default]
            else:
                match = re.search(pattern, text)
                data[key] = match.group(1).replace('\n', ' ').strip() if match else default

        # CADASTROS BÁSICOS
        fields = [
            (r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", "Data e Hora"),
            (r"Nome:\s*([A-Z\s]+)(?=\s*CPF|$)", "Nome"),
            (r"Nascimento\s*(\d{2}/\d{2}/\d{4})", "Nascimento"),
            (r"Idade\s*(\d+)", "Idade"),
            (r"Sexo\s*([A-Za-z\-]+)(?=\s*Signo|$)", "Sexo"),
            (r"RG\s*([\d]+)", "Rg", "-"),
            (r"CPF\s*([\d\.\-]+)", "Cpf"),
            (r"DADOS DA CNH\s*CNH\s*([\w\-]*)", "CNH"),
            (r"Nome da Mãe\s*([A-Z\s]+)", "Mãe"),
            (r"Nome do Pai\s*([A-Z\s\-]+)(?=\s*CPF|$)", "Pai"),
            (r"Óbito\?\s*(\w+)", "Óbito"),
            (r"ENDEREÇOS\s*Prioridade\s*Tipo Endereço\s*Endereço Completo\s*\d+\s*-\s*(.*?)(?=\s*E-MAILS|$)", "Endereços", "-"),
            (r"Renda Mensal Presumida\s*R\$\s*([\d\.,]+)", "Renda Mensal Presumida", "-"),
            (r"Situação Cadastral\s*([A-Z]+)", "Situação Cadastral"),
            (r"Inscrito em\s*(\d{2}/\d{2}/\d{4}|-)", "Inscrito em"),
            (r"Última Consulta\s*(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", "Última Consulta"),
            (r"DADOS DA CTPS\s*CTPS\s*([\w\-]*)", "CTPS"),
            (r"Série\s*([\w\-]*)", "Série"),
            (r"Título de Eleitor\s*([\w\-]*)", "Título de eleitor"),
            (r"Passaporte\s*([\w\-]*)", "Passaporte"),
            (r"País\s*(\w+|-)", "País"),
            (r"Validade\s*(\d{2}/\d{2}/\d{4})", "Validade"),
            (r"NIS \(PIS/PASEP\)\s*([\w\-]*)", "Nis (pis/pasep)"),
            (r"NIS - Outros\s*([\w\-]*)", "Nis - outros"),
            (r"CNS\s*([\d\-]+)", "Cns"),
            (r"CNS - Outros\s*([\d\-]+)", "Cns - outros"),
            (r"Inscrição Social\s*([\w\s\-]+)(?=\s*Relatório de Pessoa Física|$)", "Inscrição social", "-"),
            (r"Quantidade de Pagamentos\s*(\d+)", "Quantidade de Pagamentos"),
            (r"Valor Total dos Pagamentos\s*R\$\s*([\d,.]+)", "Valor Total dos Pagamentos"),
            (r"Valor total recebido como\s*beneficiario\s*R\$\s*([\d,.]+)", "Valor total recebido como beneficiário", "0"),
            (r"Valor total recebido como\s*responsável\s*R\$\s*([\d,.]+)", "Valor total recebido como responsável", "0"),
            (r"Valor total recebido como\s*benef./resp.\s*R\$\s*([\d,.]+)", "Valor total recebido como benef./resp.", "0"),
            (r"Primeira ocorrência\s*([a-z]{3}/\d{4})", "Primeira ocorrência", "-"),
            (r"Última ocorrência\s*([a-z]{3}/\d{4})", "Última ocorrência", "-"),
            
            # Novos campos para versao 1.1
            (r"Total de Processos\s*(\d+)", "Total de Processos"),
            (r"Como Requerente\s*(\d+)", "Como Requerente"),
            (r"Como Requerido\s*(\d+)", "Como Requerido"),
            (r"Como Outra Parte\s*(\d+)", "Como Outra Parte"),
            (r"Nos Últimos 30 Dias\s*(\d+)", "Nos Últimos 30 Dias"),
            (r"Nos Últimos 90 Dias\s*(\d+)", "Nos Últimos 90 Dias"),
            (r"Nos Últimos 180 Dias\s*(\d+)", "Nos Últimos 180 Dias"),
            (r"Nos Últimos 365 Dias\s*(\d+)", "Nos Últimos 365 Dias"),
            (r"(\d{20}|(?:\d{7}-\d{2}\.\d{4}\.\d{1,2}\.\d{2}\.\d{4}))", "Número do Processo", None, True),
            (r"Tipo\s*([A-Z\s]+)(?=\s*Status)", "Tipo", None, True),
            (r"Status\s*([A-Z\s\-]+)(?=\s*Papel)", "Status", None, True),
            (r"Papel\s*([A-Z\s]+)(?=\s*Valor)", "Papel", None, True),
            (r"Valor da Causa\s*(?:R\$)?\s*([\d,.]+|-)", "Valor da Causa", None, True),
            (r"Envolvidos\s*(\d+)", "Envolvidos", None, True),
            (r"Assunto\s*([\w\s\-\–\/\|]+)(?=\s*Tribunal|,)", "Assunto", None, True),
            (r"Tribunal\s*([\w\s\(\)\-\/]+ - [\w\s\/]+|TJ\w+ \/ [\w\s]+)(?=\s*Data|Relatório)", "Tribunal", None, True),
            (r"Data Abertura\s*(\d{2}/\d{2}/\d{2}|-)", "Data de Abertura", None, True),
            (r"Idade\s*(\d+|-)\s*(?=\s*dia|Assunto)", "Idade em Dias", None, True),
            (r"Data Encerramento\s*((?:\d{2}/\d{2}/\d{2}|-)+)", "Data de Encerramento", None, True),
            (r"Últ\. Atualização\s*(\d{2}/\d{2}/\d{2})", "Última Atualização", None, True),
            (r"Últ\. Movimentação\s*(\d{2}/\d{2}/\d{2}|-)", "Última Movimentação", None, True),
        ]

        for pattern, key, *default in fields:
            extract(pattern, key, *default)

        match = re.findall(r"\(\d{2}\) \d{4,5}-\d{4}", text)
        data["Número"] = match if match else "-"

    logging.info("Dados extraídos com sucesso")
    return data