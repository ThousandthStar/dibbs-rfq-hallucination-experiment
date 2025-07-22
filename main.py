import os
import getpass

import langchain
from dotenv import load_dotenv

from output import Output

if __name__ == "__main__":

    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

    from langchain.chat_models import init_chat_model

    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    llm = llm.with_structured_output(Output)
    print(llm.invoke("Tell me a joke about cats"))