import PyPDF2
import os

pdf_path = "Trabalho Final.pdf"
output_txt = "Trabalho_Final_extraido.txt"

if not os.path.exists(pdf_path):
    print(f"Arquivo PDF '{pdf_path}' não encontrado na pasta atual.")
    exit(1)

with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    any_text = False
    with open(output_txt, "w", encoding="utf-8") as out:
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                out.write(text + "\n")
                any_text = True
            else:
                print(f"Aviso: Nenhum texto extraído da página {i+1}.")

if any_text:
    print(f"Texto extraído para {output_txt}")
else:
    print("Nenhum texto foi extraído. O PDF pode estar protegido, ser uma imagem escaneada ou ter um formato incompatível com PyPDF2.")
    print("Sugestão: Tente usar a biblioteca 'pdfplumber' para PDFs escaneados ou com layout complexo.")