from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Body
from pydantic import BaseModel, Field

from models.schemas.auth import InitData


InitDataDep = Annotated[InitData, Body(title="body title", description="body description")]
