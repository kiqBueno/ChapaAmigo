import re
import logging
import PyPDF2

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

        def extract(pattern, key, default="ERROR"):
            match = re.search(pattern, text)
            data[key] = match.group(1).strip() if match else default

        # CADASTROS BÁSICOS
        fields = [
            (r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", "Data e Hora"),
            (r"Nome:\s*([A-Z\s]+)(?=\s*CPF|$)", "Nome"),
            (r"Nascimento\s*(\d{2}/\d{2}/\d{4})", "Nascimento"),
            (r"Idade\s*(\d+)", "Idade"),
            (r"Sexo\s*([A-Z\s\-]+)(?=\s*Signo|$)", "Sexo"),
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
            (r"Última ocorrência\s*([a-z]{3}/\d{4})", "Última ocorrência", "-")
        ]

        for pattern, key, *default in fields:
            extract(pattern, key, *default)

        match = re.findall(r"\(\d{2}\) \d{4,5}-\d{4}", text)
        data["Número"] = match if match else "-"

    logging.info("Dados extraídos com sucesso")
    return data