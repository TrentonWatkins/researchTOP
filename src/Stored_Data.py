import PyPDF2
import openai

with open("fire.pdf", "rb") as pdf_file:
    read_pdf = PyPDF2.PdfReader(pdf_file)
    number_of_pages = len(read_pdf.pages)
    page = read_pdf.pages[0]

    page_content = page.extract_text()
print(number_of_pages)

messsage = send_to_openai("Store the following PDF file in memory to reffrance when needed ")
ai_response = send_to_openai(read_pdf)
