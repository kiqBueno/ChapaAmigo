import pdfplumber
import re

def extract_data_from_pdf(file_path):
    data = {}
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Nome, Data e Hora
            name_match = re.search(r"NOME\s*(.+)", text)
            date_time_match = re.search(r"(\d{2}/\d{2}/\d{4} - \d{2}:\d{2}:\d{2})", text)
            if name_match:
                data["Nome"] = name_match.group(1)
            if date_time_match:
                data["Data e Hora"] = date_time_match.group(1)

            # CPF, Data de Nascimento
            cpf_match = re.search(r"CPF\s*(\d{3}\.\d{3}\.\d{3}-\d{2})", text)
            dob_match = re.search(r"Data de Nascimento\s*(\d{2}/\d{2}/\d{4})", text)
            if cpf_match:
                data["CPF"] = cpf_match.group(1)
            if dob_match:
                data["Data de Nascimento"] = dob_match.group(1)

            # Cadastro Básico, Renda, Histórico Receita Federal
            basic_info_match = re.search(r"Cadastro Básico.*?Nome:\s*(.+)", text, re.DOTALL)
            income_match = re.search(r"Renda Mensal Presumida\s*R\$\s*([\d,]+)", text)
            hist_match = re.search(r"Histórico Receita Federal.*?(Situação:.*)", text, re.DOTALL)
            if basic_info_match:
                data["Cadastro Básico"] = basic_info_match.group(1).strip()
            if income_match:
                data["Renda Mensal"] = income_match.group(1)
            if hist_match:
                data["Histórico Receita Federal"] = hist_match.group(1).strip()

            # Dados do RG, CNH, Pais, CTPS, etc.
            rg_match = re.search(r"RG\s*(\d+).*?UF\s*([A-Z]{2})", text, re.DOTALL)
            cnh_match = re.search(r"CNH\s*(.+?)UF\s*([A-Z]{2})", text, re.DOTALL)
            mae_match = re.search(r"Nome da Mãe\s*(.+)", text)
            pai_match = re.search(r"Nome do Pai\s*(.+)", text)
            ctps_match = re.search(r"CTPS\s*(.+?)Série\s*(\d+)", text, re.DOTALL)
            passaporte_match = re.search(r"Passaporte\s*(.+?)País\s*([A-Z]+)", text, re.DOTALL)
            if rg_match:
                data["Dados do RG"] = rg_match.group(0)
            if cnh_match:
                data["Dados da CNH"] = cnh_match.group(0)
            if mae_match:
                data["Dados da Mãe"] = mae_match.group(1).strip()
            if pai_match:
                data["Dados do Pai"] = pai_match.group(1).strip()
            if ctps_match:
                data["Dados da CTPS"] = ctps_match.group(0)
            if passaporte_match:
                data["Dados do Passaporte"] = passaporte_match.group(0)

            # Certidões e Banco Nacional de Mandados de Prisão
            antecedentes_match = re.search(r"Certidão de Antecedentes.*?(Nada Consta)", text, re.DOTALL)
            mandados_match = re.search(r"Banco Nacional de Mandados de Prisão.*?(Nenhum Encontrado)", text, re.DOTALL)
            if antecedentes_match:
                data["Certidão de Antecedentes"] = antecedentes_match.group(1)
            if mandados_match:
                data["Mandados de Prisão"] = mandados_match.group(1)

            # Pagamentos Bolsa Família
            pagamentos_match = re.findall(r"Bolsa Família.*?Valor\s*R\$\s*([\d,]+)", text, re.DOTALL)
            if pagamentos_match:
                data["Pagamentos Bolsa Família"] = pagamentos_match

    return data

# Testando o programa com um arquivo PDF
file_path = "c:/GarotoDePrograma/ArquivoDesprotegido.pdf"
extracted_data = extract_data_from_pdf(file_path)
for key, value in extracted_data.items():
    print(f"{key}: {value}")