from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.file import FileTools
import PyPDF2

# Modeli tanımlayın
gemini_model = Gemini(id="gemini-2.0-flash-exp", api_key="API_KEY_HERE")

# File Agent tanımı
file_agent = Agent(
    model=gemini_model,
    description="""
    You are a computer file operator.
    Your job is to read files and return relevant information based on user queries.
    """,
    role="file reader",
    instructions=[
        "Read files.", 
        "If you face with an error, return the error to the user."],
    tools=[FileTools()],
    add_history_to_messages=True,
    num_history_responses=2,
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    debug_mode=True,
)

# PDF dosyasını okuyalım
def read_pdf(file_path):
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"An error occurred while reading the PDF file: {e}"

# PDF dosyasını işleme
try:
    pdf_text = read_pdf("1.5.5237.pdf")
    if "An error occurred" in pdf_text:
        print(pdf_text)  # PDF'den okuma sırasında hata varsa bildir
    else:
        # Kullanıcıdan dinamik bir soru al
        user_query = input("Lütfen analiz etmek istediğiniz soruyu yazın: ")

        # File Agent ile analiz
        response = file_agent.print_response(
            f"Analyzing the following text for legal insights: {pdf_text}\n\n{user_query}"
        )
        print(response)

except Exception as e:
    print(f"An error occurred while processing the file: {e}")
