import PyPDF2
import openai

with open("fire.pdf", "rb") as pdf_file:
    read_pdf = PyPDF2.PdfReader(pdf_file)
    number_of_pages = len(read_pdf.pages)
    page = read_pdf.pages[0]

    page_content = page.extract_text()
print(number_of_pages)

storeInfo = send_to_openai("Store the following PDF file in memory to reffrance when needed ")
fileSend = send_to_openai(read_pdf)

def send_to_openai(message):
    try:
        # Send the MQTT message to OpenAI for processing
        response = openai.Completion.create(engine="text-davinci-003",  # Replace with desired model
            prompt=f"Process this message: {message}",max_tokens=50)
        # Extract and return the generated response
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error interacting with OpenAI: {e}")
        return None
