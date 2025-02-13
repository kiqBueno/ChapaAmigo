# ChapaAmigo

## Descrição (Description)

ChapaAmigo é uma aplicação para extração e manipulação de dados de arquivos PDF. A aplicação permite personalizar layouts de PDF, inserir fotos, e proteger PDFs com senha.

ChapaAmigo is an application for extracting and manipulating data from PDF files. The application allows customizing PDF layouts, inserting photos, and protecting PDFs with a password.

## Estrutura do Projeto (Project Structure)

- `app/InterpretePdf.py`: Script para extrair dados de arquivos PDF. (Script to extract data from PDF files.)
- `app/index.py`: Interface gráfica para interação com o usuário. (Graphical interface for user interaction.)
- `app/DestravarPdf.py`: Script para destravar arquivos PDF protegidos por senha. (Script to unlock password-protected PDF files.)
- `app/Cache.py`: Funções auxiliares para manipulação de PDFs e imagens. (Helper functions for manipulating PDFs and images.)

## Dependências (Dependencies)

- Python 3.x
- PyPDF2
- PySimpleGUI
- PyMuPDF (fitz)
- Pillow
- reportlab

## Instalação (Installation)

1. Clone o repositório: (Clone the repository:)
   ```sh
   git clone https://github.com/SeuUsuario/ChapaAmigo.git
   ```
2. Navegue até o diretório do projeto: (Navigate to the project directory:)
   ```sh
   cd ChapaAmigo
   ```
3. Instale as dependências: (Install the dependencies:)
   ```sh
   pip install -r requirements.txt
   ```

## Uso (Usage)

1. Execute a interface gráfica: (Run the graphical interface:)
   ```sh
   python app/index.py
   ```
2. Utilize os botões para selecionar arquivos PDF, personalizar o layout e inserir fotos. (Use the buttons to select PDF files, customize the layout, and insert photos.)
3. Os PDFs gerados serão salvos no diretório `Relatórios`. (The generated PDFs will be saved in the `Relatórios` directory.)

## Funções Principais (Main Functions)

### `extract_data_from_pdf(file_path, senha='515608')`

Extrai dados de um arquivo PDF protegido por senha. (Extracts data from a password-protected PDF file.)

### `destravar_pdf(input_pdf, senha='515608')`

Destrava um arquivo PDF protegido por senha. (Unlocks a password-protected PDF file.)

### `save_specific_pages_as_images(pdf_path, senha_pdf)`

Salva páginas específicas de um PDF como imagens. (Saves specific pages of a PDF as images.)

### `crop_image(img_bytes)`

Corta 10% das imagens em cima e em baixo. (Crops 10% of the images from the top and bottom.)

### `add_transparency(image_path, transparency)`

Adiciona transparência à imagem. (Adds transparency to the image.)

### `create_pdf(data, output_pdf_path, images, usar_marca_dagua=True, foto_path=None, incluir_contrato=False, incluir_documentos=False, grupos_selecionados=None)`

Cria um PDF com as informações extraídas e adiciona imagens. (Creates a PDF with the extracted information and adds images.)

## Licença (License)

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes. (This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.)
