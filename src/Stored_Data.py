import openai
import PyPDF2


openai.api_key = "Enter API key here"


def sendFile():
    try:
        # Open and read the PDF file
        with open("fire.pdf", "rb") as pdf_file:
            read_pdf = PyPDF2.PdfReader(pdf_file)
            pdf_content = ""
            for page in read_pdf.pages:
                pdf_content += page.extract_text()
            number_of_pages = len(read_pdf.pages)
            page = read_pdf.pages[0]

            # Extract text from the first page
            page_content = page.extract_text()
        
        # Print the number of pages
        print(f"Number of pages: {number_of_pages}")

        # Send the extracted text to OpenAI
        storeInfo = send_to_openai("Store the following PDF file in memory to reference when needed: " + pdf_content)
        
        # Print confirmation
        print("Info Stored")

    except FileNotFoundError:
        print("Error: The file 'fire.pdf' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def send_to_openai(message):
    try:
        # Send the message to OpenAI for processing
        response = openai.Completion.create(
            engine="text-davinci-003",  # Replace with desired model
            prompt=f"Process this message: {message}",
            max_tokens=50
        )
        # Extract and return the generated response
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error interacting with OpenAI: {e}")
        return None

def main():
    sendFile()

if __name__ == "__main__":
    main()
