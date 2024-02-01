from pydantic import BaseModel
from .booksSchema import Book

class Student(BaseModel):
    name : str
    class_name : str
    section : str
    is_member : bool
    books_issued : list[object] | None = None
