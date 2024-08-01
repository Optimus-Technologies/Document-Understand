import PyPDF2, docx2txt, textract, os, re
from PIL import Image
import pytesseract

from fastapi import UploadFile, File
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
import tempfile
from io import BytesIO


#Convert pdf to text
def convert_pdf_text(document):
    contents = document.read()
    pdf_reader = PyPDF2.PdfReader(BytesIO(contents))

    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text 


#Convert docx to text
def convert_docx_text(document):
    contents = document.read()
    text = docx2txt.process(BytesIO(contents))
    return text
    

#Convert image to text
def convert_image_text(image):
    contents = image.read()
    image = Image.open(BytesIO(contents))
    
    # Extract text from image using pytesseract
    text = pytesseract.image_to_string(image)
    return text

#Convert other file types to text
def convert_other_text(document):
    contents =  document.read()
    
    with open("tempfile", "wb") as temp_file:
        temp_file.write(contents)
        
    text = textract.process("tempfile").decode("utf-8")
    
    os.remove("tempfile")
    
    return text

def document_convertor(ext: str, document):
    if ext == "pdf":
        text = convert_pdf_text(document=document)
    elif ext == "docx":
        text =  convert_docx_text(document=document)
    elif ext in ['jpg', 'jpeg', 'png', 'tiff']:
        text =  convert_image_text(image=document)
    else:
        text = convert_other_text(document=document)
    return text

def format_output(text):
    formatted_text = ""
    
    # Use regex to identify key sections
    sections = re.split(r'\*\*([^:]+):\*\*', text)
    
    if len(sections) > 1:
        formatted_text += "\n".join([f"**{sections[i].strip()}**\n{sections[i+1].strip()}\n" 
                                     for i in range(1, len(sections) - 1, 2)])
    
    return formatted_text.strip()





#Converts PDF, JPEG/JPG, PNG, BMP, TIFF, HEIF, DOCX, XLSX, PPTX and HTML to text
async def convert_to_text(document):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await document.read())
        tmp_path = tmp.name


    file_path = tmp_path
    endpoint = "https://universal-document-parser.cognitiveservices.azure.com/"
    key = "29f9e4735ba248649e10f3ee4d8d0b5c"
    loader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=endpoint, api_key=key, file_path=file_path, api_model="prebuilt-layout"
    )

    documents = loader.load()
    text = ""
    for doc in documents:
        text += doc.page_content
    return text