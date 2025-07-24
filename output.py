

from pydantic import BaseModel, Field

class Output(BaseModel):

    nsn: str = Field(description="The NSN number, without hyphens.")
    qty: str = Field(description="The quantity to deliver.")
    delivery_time: str = Field(description="The timeline to deliver, such as 15 DAYS ADO. Write it exactly as it is in the document.")
    delivery_type: str = Field(description="The type of deliver, such as FOB DESTINATION. Write it exactly as it is in the document.")
    unit: str = Field(description="The type of unit to deliver. Make sure to use the abbreviation and write it as it is in the document.")
    small_business_set_aside: str = Field(description="If the RFQ is a small business set-aside, enter 'yes'. Otherwise, enter 'no'.")
    destination_address: str = Field(description="The full post address of the destination. Replace all newline characters with spaces, so as to make the answer a one-line string.")

    