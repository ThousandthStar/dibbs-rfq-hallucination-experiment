import os
import getpass
from urllib.request import urlretrieve

import langchain
from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

import output
import data_loader

if __name__ == "__main__":

    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

    urls_path = "./urls.txt"
    folder_path = "./pdfs"

    #llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    #llm = llm.with_structured_output(output.Output)
    #print(llm.invoke("Tell me a joke about cats"))

    data_loader.load_data(urls_path, folder_path)