import os
import getpass
from urllib.request import urlretrieve
import time

import langchain
from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import init_chat_model
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

import output
import data_loader

prompt = """
Here is a RFQ document from SAM.gov. Please provide us these details about the document, as accurately as possible:
- NSN
"""

if __name__ == "__main__":

    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

    if "ANTHROPIC_API_KEY" not in os.environ:
        os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")
        
    urls_path = "./urls.txt"
    folder_path = "./pdfs"

    models = [
        init_chat_model("gpt-4o-mini", model_provider="openai").with_structured_output(output.Output),
        ChatAnthropic(model="claude-3-5-sonnet-20240620").with_structured_output(output.Output),
    ]

    model_names = [
        "OpenAI GPT-4o-mini",
        "Anthropic Claude 3.5 Sonnet 20240620"
    ]

    for llm, model_name in zip(models, model_names):
        print(f"\n\n\n*********************************************************")
        print(f"Checking model {model_name}")
        print(f"*********************************************************")
        for path in os.listdir("./pdfs"):
            print(f"Checking document {path}")
            dir = data_loader.pdf_to_image(f"./pdfs/{path}", "./img")
            message = data_loader.load_png_messages(dir, prompt)

            image_response = llm.invoke([message])
            print("Image file response:\n", image_response, '\n')

            pdf_content = data_loader.load_pdf_text(f"./pdfs/{path}")
            
            time.sleep(30) # this is to make sure the program isn't rate limited, especially by the OpenAI API

            pdf_response = llm.invoke([{
                "role": "user",
                "content": [
                    {
                        'type': 'text',
                        'text': prompt + '\n\n\n' + pdf_content
                    }
                ]
            }])

            print("PDF text response:\n", pdf_response, "\n")

            validation_object = data_loader.load_validation(path, 'validation')
            print("Validation object:\n", validation_object, "\n\n\n")

            for key, value in validation_object.items():
                print(f"Checking attribute {key}...")
                if getattr(image_response, key) == value:
                    print(f"Attribute {key} matched for image response")
                else:
                    print(f"Attribute {key} didn't match for image response")
                
                if getattr(pdf_response, key) == value:
                    print(f"Attribute {key} matched for PDF response")
                else:
                    print(f"Attribute {key} didn't match for PDF response")

            time.sleep(30) # this is to make sure the program isn't rate limited, especially by the OpenAI API

            


        

        