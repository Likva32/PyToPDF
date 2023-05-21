import os
import glob
import pdfkit
import sys
from PyPDF2 import PdfMerger


def convert_py_to_pdf(folder_path):
    if not os.path.exists(folder_path):
        print("Folder not found")
        return

    py_files = []
    for root, dirs, files in os.walk(folder_path):
        if 'venv' in dirs:
            dirs.remove('venv')
        if '.venv' in dirs:
            dirs.remove('.venv')
        py_files += glob.glob(os.path.join(root, '*.py'))
    if not py_files:
        print(".py files not found")
        return

    pdf_folder = os.path.join('pdf_files')
    os.makedirs(pdf_folder, exist_ok=True)

    # Specify the path to the wkhtmltopdf executable file
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    for py_file in py_files:
        py_file_name = os.path.basename(py_file)
        pdf_file_name = os.path.splitext(py_file_name)[0] + '.pdf'
        pdf_file_path = os.path.join(pdf_folder, pdf_file_name)

        with open(py_file, 'r', encoding='utf-8') as file:
            py_code = file.read()

        formatted_code = "<pre>" + py_code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n",
                                                                                                                   "<br>") + "</pre>"
        pdfkit.from_string(formatted_code, pdf_file_path, configuration=config)

        print(f"file {pdf_file_name} created")

    print("Conversion completed")


def merge_pdfs(input_folder, output_path):
    merger = PdfMerger()

    input_files = glob.glob(f"{input_folder}/*.pdf")

    for path in input_files:
        merger.append(path)

    merger.write(output_path)
    merger.close()


try:
    args = sys.argv
    folder_path = args[1]
except:
    folder_path = 'C:/Users/artur/Desktop/projects/ГОДОВОЙ ПРОЕКТ/code'
convert_py_to_pdf(folder_path)

input_folder = 'pdf_files'
output_file = 'merged.pdf'
merge_pdfs(input_folder, output_file)
