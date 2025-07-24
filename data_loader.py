
import requests
import base64
import os
import glob
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader, UnstructuredImageLoader
import output
from pdf2image import convert_from_path
import json

def load_pdf_text(file_path: str) -> str:

    loader = PyPDFLoader(file_path)
    final_string: str = ""

    for count, page in enumerate(loader.lazy_load()):
        if count < 10:
            final_string += page.page_content

    return final_string

def load_png_messages(file_path: str, prompt: str):
    image_messages = [{
        'type': 'text',
        'text': prompt,
    }]
    for image_file in glob.glob(os.path.join(file_path, '*.png')):
        with open(image_file, 'rb') as file:
            image_data = base64.b64encode(file.read()).decode('utf-8')
            image_messages.append(
                    {
                        "type": "image",
                        "source_type": "base64",
                        "data": image_data,
                        "mime_type": "image/png",
                    }
                
            )
    return {
        "role": "user",
        "content": image_messages
    }



def pdf_to_image(pdf_path: str, img_folder_path: str) -> str:
    pages = convert_from_path(pdf_path)
    
    try:
        os.mkdir(img_folder_path)
        print("Images folder created")
    except Exception:
        print("Images folder already exists")

    print("Clearing folder...\n")
    files = glob.glob(f"{img_folder_path}/*/*")
    for file in files:
        os.remove(file)

    dirs = glob.glob(f"{img_folder_path}/*")
    for dir in dirs:
        os.rmdir(dir)

    pdf_name = pdf_path.split("/")[-1].removesuffix(".PDF")
    os.mkdir(f"./{img_folder_path}/{pdf_name}")
    for count, page in enumerate(pages):
        if count < 10:
            page.save(f'./{img_folder_path}/{pdf_name}/out{count}.png', 'PNG')

    return f"{img_folder_path}/{pdf_name}"

def load_validation(pdf_name: str, validation_folder_path: str) -> output.Output:

    path = f"./{validation_folder_path}/{pdf_name.replace('.PDF', '.json')}"
    
    with open(path, 'r') as file:
        validation_object = json.load(file)

    return validation_object

