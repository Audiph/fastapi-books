from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from typing import List
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
  id: int
  title: str
  author: str
  description: str
  rating: int
  published_date: int

  def __init__(self, id, title, author, description, rating, published_date) -> None:
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating
    self.published_date = published_date


class BookRequest(BaseModel):
  id: Optional[int] = None
  title: str = Field(min_length=3)
  author: str = Field(min_length=1)
  description: str = Field(min_length=1, max_length=100)
  rating: int = Field(gt=-1, lt=6)
  published_date: int = Field(gt=0)

  class Config:
    json_schema_extra = {
      'example': {
        'title': 'A new book',
        'author': 'Jeff',
        'description': 'A new description of a book',
        'rating': 5,
        'published_date': 2023
      }
    }


BOOKS = [
  Book(1, 'Computer Science Pro', 'Jeff', 'A very nice book!', 5, 2012),
  Book(2, 'Be Fast with FastAPI', 'Jeff', 'A great book!', 5, 2011),
  Book(3, 'Master Endpoints', 'Jeff', 'An awesome book!', 5, 2012),
  Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2012),
  Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2022),
  Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2023)
]


@app.get('/books', status_code=status.HTTP_200_OK)
async def get_all_books():
  return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
  for book in BOOKS:
    if book.id == book_id:
      return book

  raise HTTPException(status_code=404, detail='Book not found')


@app.get('/books/by_rating/', status_code=status.HTTP_200_OK)
async def get_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
  books = []
  for book in BOOKS:
    if book.rating == book_rating:
      books.append(book)

  return books


@app.get('/books/by_published_date/', status_code=status.HTTP_200_OK)
async def get_books_by_published_date(book_published_date: int = Query(gt=0)):
  books = []
  for book in BOOKS:
    if book.published_date == book_published_date:
      books.append(book)

  return books


@app.post('/books/create_book', status_code=status.HTTP_201_CREATED)
async def create_Book(book_request: BookRequest):
  new_book = Book(**book_request.model_dump())
  BOOKS.append(find_book_id(new_book))


@app.put('/books/update_book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest) -> None:
  book_changed = False
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book.id:
      BOOKS[i] = book
      book_changed = True

  if not book_changed:
    raise HTTPException(status_code=404, detail='Book not found')


@app.delete('/books/delete_book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)) -> None:
  book_changed = False
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book_id:
      BOOKS.pop(i)
      book_changed = True
      break

  if not book_changed:
    raise HTTPException(status_code=404, detail='Book not found')


def find_book_id(book: Book):
  book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

  return book
