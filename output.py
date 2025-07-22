

from pydantic import BaseModel, Field

class Output(BaseModel):

    setup: str = Field(description="Setup of the joke")
    punchline: str = Field(description="The punchline of the joke")