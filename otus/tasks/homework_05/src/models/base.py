from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    id: Mapped[int_pk]
    
    type_annotation_map = {
        str_256: String(256)
    }