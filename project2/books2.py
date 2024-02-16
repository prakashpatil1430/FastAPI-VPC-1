from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    desc: str
    rating: int
    published_year: int

    def __init__(self, id, title, author, desc, rating, published_year=None) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.desc = desc
        self.rating = rating
        self.published_year = published_year


class BookRequest(BaseModel):
    # for id fileds pidentic2 version tells provide None for if you using as optional as fileds

    # id: Optional[int] = Field(None, title='id is not needed') or
    id: Optional[int] = None  # here
    title: str = Field(min_length=3, examples=["A new book"])
    author: str = Field(min_length=1, examples=['codingwithroby'])
    desc: str = Field(min_length=1, max_length=100, examples=[
                      'A new description of a book'])
    rating: int = Field(gt=0, lt=6, examples=[5])
    published_year: int = Field(gt=1999, lt=2031, examples=[2021])

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'codingwithroby',
                'desc': 'A new description of a book',
                'rating': 5,
                'published_year': 2023  # Corrected attribute name
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby',
         'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{id}", status_code=status.HTTP_200_OK)
def get_book_by_id(id: int):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


@app.get('/books/', status_code=status.HTTP_200_OK)
def get_book_by_rating(book_rating: int = Query(gt=1, lt=6)):
    book_list = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_list.append(book)
    return book_list


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2024)):
    book_list = []
    for book in BOOKS:
        if book.published_date == published_date:
            book_list.append(book)
    return book_list


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
def creating_book(request_book: BookRequest):
    new_book = Book(**request_book.dict())
    new_book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    BOOKS.append(new_book)
    return new_book  # Optionally return the created book


@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='item not found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')
