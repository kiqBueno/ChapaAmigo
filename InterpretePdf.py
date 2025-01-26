import re

def extract_data_from_text(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

        # CADASTROS BASICOS
        match = re.search(r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", text)
        data["Data e Hora"] = match.group(1) if match else ""

        match = re.search(r"Nome:\s*([A-Z\s]+)", text)
        data["Nome"] = match.group(1).strip() if match else ""

        match = re.search(r"Nascimento:\s*(\d{2}/\d{2}/\d{4})", text)
        data["Nascimento"] = match.group(1) if match else ""

        match = re.search(r"Idade:\s*(\d+)", text)
        data["Idade"] = match.group(1) if match else ""

        match = re.search(r"Sexo:\s*([A-Z]+)", text)
        data["Sexo"] = match.group(1) if match else ""

        match = re.search(r"Rg:\s*([\d\.\-]+)", text)
        data["Rg"] = match.group(1) if match else ""

        match = re.search(r"Cpf:\s*([\d\.\-]+)", text)
        data["Cpf"] = match.group(1) if match else ""

        match = re.search(r"CNH:\s*([\d\.\-]+)", text)
        data["CNH"] = match.group(1) if match else ""

        match = re.search(r"Mãe:\s*([A-Z\s]+)", text)
        data["Mãe"] = match.group(1).strip() if match else ""

        match = re.search(r"Pai:\s*([A-Z\s]*)", text)
        data["Pai"] = match.group(1).strip() if match else ""

        match = re.search(r"Óbito\?:\s*(\w+)", text)
        data["Óbito?"] = match.group(1) if match else ""

        # Renda
        match = re.search(r"Renda Mensal Presumida:\s*([\d,]+)", text)
        data["Renda Mensal Presumida"] = match.group(1) if match else ""

        # Histórico receita federal
        match = re.search(r"Situação Cadastral:\s*([A-Z]+)", text)
        data["Situação Cadastral"] = match.group(1) if match else ""

        match = re.search(r"Inscrito em:\s*(\d{2}/\d{2}/\d{4})", text)
        data["Inscrito em"] = match.group(1) if match else ""

        match = re.search(r"Última Consulta:\s*(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", text)
        data["Última Consulta"] = match.group(1) if match else ""

        # Dados da Ctps
        match = re.search(r"CTPS:\s*([\d\.\-]+)", text)
        data["CTPS"] = match.group(1) if match else ""

        match = re.search(r"Série:\s*([\d\.\-]+)", text)
        data["Série"] = match.group(1) if match else ""

        match = re.search(r"Emissão:\s*(\d{2}/\d{2}/\d{4})", text)
        data["Emissão"] = match.group(1) if match else ""

        # TITULO ELEITORAL
        match = re.search(r"Título de eleitor:\s*([\d\.\-]+)", text)
        data["Título de eleitor"] = match.group(1) if match else ""

        match = re.search(r"Zona:\s*([\d\.\-]+)", text)
        data["Zona"] = match.group(1) if match else ""

        match = re.search(r"Seção:\s*([\d\.\-]+)", text)
        data["Seção"] = match.group(1) if match else ""

        # Dados do passaporte
        match = re.search(r"Passaporte:\s*([\d\.\-]+)", text)
        data["Passaporte"] = match.group(1) if match else ""

        match = re.search(r"País:\s*([A-Z]+)", text)
        data["País"] = match.group(1) if match else ""

        match = re.search(r"Validade:\s*(\d{2}/\d{2}/\d{4})", text)
        data["Validade"] = match.group(1) if match else ""

        match = re.search(r"Emissão:\s*(\d{2}/\d{2}/\d{4})", text)
        data["Emissão"] = match.group(1) if match else ""

        # DADOS SOCIAIS
        match = re.search(r"Nis \(pis/pasep\):\s*([\d\.\-]+)", text)
        data["Nis (pis/pasep)"] = match.group(1) if match else ""

        match = re.search(r"Nis - outros:\s*([\d\.\-]+)", text)
        data["Nis - outros"] = match.group(1) if match else ""

        match = re.search(r"Cns:\s*([\d\.\-]+)", text)
        data["Cns"] = match.group(1) if match else ""

        match = re.search(r"Cns - outros:\s*([\d\.\-]+)", text)
        data["Cns - outros"] = match.group(1) if match else ""

        match = re.search(r"Inscrição social:\s*([\d\.\-]+)", text)
        data["Inscrição social"] = match.group(1) if match else ""

        # CELULARES E TELEFONES FIXO
        match = re.search(r"Número:\s*([\d\(\)\-\s]+)", text)
        data["Número"] = match.group(1).strip() if match else ""

        # PAGAMENTOS E SAQUES BOLSA FAMILIA
        match = re.search(r"Resultado:\s*([\w\s]+)", text)
        data["Resultado"] = match.group(1).strip() if match else ""

        match = re.search(r"Descrição:\s*([\w\s]+)", text)
        data["Descrição"] = match.group(1).strip() if match else ""

        # AUXÍLIO EMERGENCIAL
        match = re.search(r"Números de ocorrências:\s*(\d+)", text)
        data["Números de ocorrências"] = match.group(1) if match else ""

        match = re.search(r"Valor total recebido como beneficiário:\s*R\$\s*([\d,]+)", text)
        data["Valor total recebido como beneficiário"] = match.group(1) if match else ""

        match = re.search(r"Valor total recebido como responsável:\s*R\$\s*([\d,]+)", text)
        data["Valor total recebido como responsável"] = match.group(1) if match else ""

        match = re.search(r"Valor total recebido como benef./resp.:\s*R\$\s*([\d,]+)", text)
        data["Valor total recebido como benef./resp."] = match.group(1) if match else ""

        match = re.search(r"Primeira ocorrência:\s*(\d{2}/\d{2}/\d{4})", text)
        data["Primeira ocorrência"] = match.group(1) if match else ""

        match = re.search(r"Última ocorrência:\s*(\d{2}/\d{2}/\d{4})", text)
        data["Última ocorrência"] = match.group(1) if match else ""

    return data