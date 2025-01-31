import re
import encodings

def extract_data_from_text(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
        #CADASTROS BÁSICOS
        
        #Data e Hora
        #CHECK
        match = re.search(r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", text)
        data["Data e Hora"] = match.group(1) if match else "ERROR"

        #Nome
        #CHECK

        match = re.search(r"Nome:\s*([A-Z\s]+)(?=\s*CPF|$)", text)
        data["Nome"] = match.group(1).strip() if match else "ERROR"
        
        #Nascimento
        #CHECK
        match = re.search(r"Nascimento\s*(\d{2}/\d{2}/\d{4})", text)
        data["Nascimento"] = match.group(1) if match else "ERROR"

        #Idade
        #CKECK
        match = re.search(r"Idade\s*(\d+)", text)
        data["Idade"] = match.group(1) if match else "ERROR"

        #Sexo
        #CHECK
        match = re.search(r"Sexo\s*([A-Z\s\-]+)", text)
        data["Sexo"] = match.group(1) if match else "ERROR"

        #Rg
        #CHECK
        match = re.search(r"RG\s*([\d]+)", text)
        data["Rg"] = match.group(1) if match else "-"
        

        #Cpf
        #CHECK
        match = re.search(r"CPF\s*([\d\.\-]+)", text)
        if match and "cpf" not in data:
            data["Cpf"] = match.group(1) if match else "ERROR"

        #Cnh
        #CHECK
        match = re.search(r"DADOS DA CNH\s*CNH\s*([\w\-]*)", text)
        data["CNH"] = match.group(1) if match else "ERROR"


        #Mãe
        #CHECK
        match = re.search(r"Nome da Mãe\s*([A-Z\s]+)", text)
        data["Mãe"] = match.group(1).strip() if match else "ERROR"

        #Pai
        #CHECK
        match = re.search(r"Nome do Pai\s*([A-Z\s\-]+)(?=\s*CPF|$)", text)
        data["Pai"] = match.group(1).strip() if match else "ERROR"
        
        #Obito
        #CHECK
        match = re.search(r"Óbito\?\s*(\w+)", text)
        data["Óbito"] = match.group(1) if match else "ERROR"
        
        #Endereços
        match = re.search(r"ENDEREÇOS\s*Prioridade\s*Tipo Endereço\s*Endereço Completo\s*\d+\s*-\s*(.*?)(?=\s*E-MAILS|$)", text, re.DOTALL)
        data["Endereços"] = match.group(1).strip() if match else "ERROR"

        #RENDA
        
        #Renda Mensal Presumida
        #CHECK
        match = re.search(r"Renda Mensal Presumida\s*R\$\s*([\d\.,]+)", text)
        data["Renda Mensal Presumida"] = match.group(1) if match else "-"

        #HISTÓRICO DA RECEITA FEDERAL
        
        #Situação Cadastral
        #CHECK
        match = re.search(r"Situação Cadastral\s*([A-Z]+)", text)
        data["Situação Cadastral"] = match.group(1) if match else "ERROR"

        #Inscrito em
        #CHECK
        match = re.search(r"Inscrito em\s*(\d{2}/\d{2}/\d{4}|-)", text)
        data["Inscrito em"] = match.group(1) if match else "ERROR"

        #Última Consulta
        #CHECK
        match = re.search(r"Última Consulta\s*(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", text)
        data["Última Consulta"] = match.group(1) if match else "ERROR"

        #DADOS DA CTPS
        
        #Ctps
        #CHECK
        match = re.search(r"DADOS DA CTPS\s*CTPS\s*([\w\-]*)", text)
        data["CTPS"] = match.group(1) if match else "ERROR"
        
        #Série
        #CHECK
        match = re.search(r"Série\s*([\w\-]*)", text)
        data["Série"] = match.group(1) if match else "ERROR"

        #TITULO ELEITORAL
        
        #Titulo de Eleitor
        #CHECK
        match = re.search(r"Título de Eleitor\s*([\w\-]*)", text)
        data["Título de eleitor"] = match.group(1) if match else "ERROR"

        #DADOS DO PASSAPORTE
        
        #Passaporte
        #CHECK
        match = re.search(r"Passaporte\s*([\w\-]*)", text)
        data["Passaporte"] = match.group(1) if match else "ERROR"

        #País
        #CHECK
        match = re.search(r"País\s*(\w+|-)", text)
        data["País"] = match.group(1) if match else "ERROR"

        #Validade
        #CHECK
        match = re.search(r"Validade\s*(\d{2}/\d{2}/\d{4})", text)
        data["Validade"] = match.group(1) if match else "ERROR"

        #DADOS SOCIAIS
        
        #Nis (pis/pasep)
        #CHECK
        match = re.search(r"NIS \(PIS/PASEP\)\s*([\w\-]*)", text)
        data["Nis (pis/pasep)"] = match.group(1) if match else "ERROR"

        #Nis - outros
        #CHECK
        match = re.search(r"NIS - Outros\s*([\w\-]*)", text)
        data["Nis - outros"] = match.group(1) if match else "ERROR"

        #Cns
        #CHECK
        match = re.search(r"CNS\s*([\d\-]+)", text)
        data["Cns"] = match.group(1) if match else "ERROR"

        #Cns - outros
        #CHECK
        match = re.search(r"CNS - Outros\s*([\d\-]+)", text)
        data["Cns - outros"] = match.group(1) if match else "ERROR"

        #Inscrição social
        #CHECK
        match = re.search(r"Inscrição Social\s*([\w\s\-]+)", text)
        data["Inscrição social"] = match.group(1).strip() if match else "ERROR"
        
        match = re.search(r"Inscrição Social\s*([\w\s\-]+)(?=\s*Relatório de Pessoa Física|$)", text)
        data["Inscrição social"] = match.group(1).strip() if match else "-"

        
        #CELULARES E TELEFONES FIXO
        
        #Número
        #CHECK
        match = re.findall(r"\(\d{2}\) \d{4,5}-\d{4}", text)
        data["Número"] = match if match else "-"

        #PAGAMENTOS DO BENEFÍCIO DE PRESTAÇÃO CONTINUADA
        
        #Quantidade de Pagamentos
        #CHECK
        match = re.search(r"Quantidade de Pagamentos\s*(\d+)", text)
        data["Quantidade de Pagamentos"] = match.group(1) if match else "ERROR"
        
        #Valor Total dos Pagamentos
        #CHECK
        match = re.search(r"Valor Total dos Pagamentos\s*R\$\s*([\d,.]+)", text)
        data["Valor Total dos Pagamentos"] = match.group(1) if match else "ERROR"

        #AUXÍLIO EMERGENCIAL
        
        #Valor total recebido como beneficiário
        #CHECK
        match = re.search(r"Valor total recebido como\s*beneficiario\s*R\$\s*([\d,.]+)", text)
        data["Valor total recebido como beneficiário"] = match.group(1) if match else "0"
        
        #Valor total recebido como responsável
        #CHECK
        match = re.search(r"Valor total recebido como\s*responsável\s*R\$\s*([\d,.]+)", text)
        data["Valor total recebido como responsável"] = match.group(1) if match else "0"
        
        #Valor total recebido como benef./resp.
        #CHECK
        match = re.search(r"Valor total recebido como\s*benef./resp.\s*R\$\s*([\d,.]+)", text)
        data["Valor total recebido como benef./resp."] = match.group(1) if match else "0"

        #Primeira ocorrência
        #CHECK
        match = re.search(r"Primeira ocorrência\s*([a-z]{3}/\d{4})", text)
        data["Primeira ocorrência"] = match.group(1) if match else "-"

        #Última ocorrência
        #CHECK
        match = re.search(r"Última ocorrência\s*([a-z]{3}/\d{4})", text)
        data["Última ocorrência"] = match.group(1) if match else "-"

    return data