# SAM.gov hallucination experiment

This is an experiment to determine the rate of hallucinations of LLMs on contract data, depending on the foundational model and the way the data is passed to the LLM.

The script tests for predetermined data found in 4 RFQs. The RFQ PDFs are stored in the `pdfs/` directory. The full validation schema and data is found in `validation/`.

The script challenges the LLMs to find the following data in the RFQs:
- NSN
- Quantity
- Delivery Time
- Delivery Type
- Unit
- Whether it is a small business set-aside
- Delivery address

The script compares the performance of `GPT-4o-mini` to that of `Claude 3.5 Sonnet 20240620`.

## What was this made for?

This was made for the [Harvard Undergraduate Ventures-TECH Summer Program (HUVTSP)](https://tech.seas.harvard.edu/summer), as part of the internship project for a defense tech company.

## How does the code work?

Here is described what each file in the code base does:
- `main.py` is the main script: it loads the LLMs and tests each model against each case;
- `output.py` defines the class `Output`, which describes the output schema we pass to LangChain when prompting the LLMs.
- `data_loader.py` defines utility functions for loading LLM-compatible data from the PDFs, converting the PDFs to images and loading the validation data.

## How to run:

1. `pip install -r requirements.txt`

**N.B.: You must also install `poppler` for `pdf2image` to work.**

2. Create a file named `.env` and add your API keys like so:

    ```
    OPENAI_API_KEY=<your key here>
    ANTHROPIC_API_KEY=<your key here>
    ```

3. `python3 main.py`

## Limitations

In order to avoid reaching the token limits, the LLMs are only passed the first 10 pages of each document.

In order to avoid reaching the rate limit for the APIs, a delay of 30 seconds is added between each prompt, making the script slower.
