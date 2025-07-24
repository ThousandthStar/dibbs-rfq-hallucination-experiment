# sam.gov-hallucination-experiment

This is an experiment to determine the rate of hallucinations of LLMs on contract data, depending on the foundational model and the way the data is passed to the LLM.

## How to run:

`pip install -r requirements.txt`

You must also install `poppler` for `pdf2image` to work.

Create a file named `.env` and add your API keys like so:

```
TODO FILL THIS
```

`python3 main.py`
