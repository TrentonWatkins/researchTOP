import PyPDF2

with open("fire.pdf", "rb") as pdf_file:
    read_pdf = PyPDF2.PdfReader(pdf_file)
    number_of_pages = len(read_pdf.pages)
    page = read_pdf.pages[0]

    page_content = page.extract_text()
print(number_of_pages)
