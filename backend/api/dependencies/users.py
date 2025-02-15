from typing import Annotated

from fastapi.params import Query

username_dep = Annotated["str", Query()]