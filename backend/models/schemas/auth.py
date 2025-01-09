from fastapi import Body
from pydantic import BaseModel, Field


class InitData(BaseModel):
    init_data: str = Field(title="Init Data", description="A string with raw data transferred to the Mini App")
