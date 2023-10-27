from fastapi import FastAPI, Body
from typing import List
from pydantic import BaseModel

app = FastAPI()


class Book:
  id: int
  title: str
  author: str
  description: str
  rating: int

  def __init__(self, id, title, author, description, rating) -> None:
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating


class BookRequest(BaseModel):
  id: int
  title: str
  author: str
  description: str
  rating: int


BOOKS = [
  Book(1, 'Computer Science Pro', 'Jeff', 'A very nice book!', 5),
  Book(2, 'Be Fast with FastAPI', 'Jeff', 'A great book!', 5),
  Book(3, 'Master Endpoints', 'Jeff', 'An awesome book!', 5),
  Book(4, 'HP1', 'Author 1', 'Book Description', 2),
  Book(5, 'HP2', 'Author 2', 'Book Description', 3),
  Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]


@app.get('/books')
async def get_all_books():
  return BOOKS


@app.get('/books/title/{book_title}')
async def get_book_by_title(book_title: str):
  for book in BOOKS:
    if book['title'].casefold() == book_title.casefold():
      return book

  return {'message': 'Book not found'}


@app.get('/books/author/{book_author}')
async def get_book_by_author(book_author: str) -> dict:
  for book in BOOKS:
    if book['author'].casefold() == book_author.casefold():
      return book

  return {'message': 'Book not found'}


@app.get('/books/')
async def get_books_by_category(category: str) -> list:
  books = []
  for book in BOOKS:
    if book['category'].casefold() == category.casefold():
      books.append(book)

  return books


@app.get('/books/{book_author}/')
async def get_books_by_author_and_category(book_author: str, category: str) -> list:
  books = []
  for book in BOOKS:
    if book['author'].casefold() == book_author.casefold() and book['category'].casefold() == category.casefold():
      books.append(book)

  return books


@app.post('/books/create_book')
async def create_Book(book_request: BookRequest):
  new_book = Book(**book_request.model_dump())
  BOOKS.append(new_book)


@app.put('/books/update_book')
async def update_book(updated_book=Body()) -> None:
  for i in range(len(BOOKS)):
    if BOOKS[i]['title'].casefold() == updated_book['title'].casefold():
      BOOKS[i] = updated_book


@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title: str) -> None:
  for i in range(len(BOOKS)):
    if BOOKS[i]['title'].casefold() == book_title.casefold():
      BOOKS.pop(i)
      break
