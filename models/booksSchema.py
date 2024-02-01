from pydantic import BaseModel

class Book(BaseModel):
    title : str
    price : int
    is_in_circulation : bool
    is_issued : bool
