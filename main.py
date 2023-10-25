from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
  {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
  {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
  {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
  {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
  {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
  {'title': 'Title Six', 'author': 'Author Six', 'category': 'math'}
]


@app.get('/books')
async def get_all_books() -> list:
  return BOOKS


@app.get('/books/{book_title}')
async def get_book(book_title: str) -> dict:
  for book in BOOKS:
    if book['title'].casefold() == book_title.casefold():
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
async def create_Book(new_book=Body()) -> None:
  BOOKS.append(new_book)


@app.put('/books/update_book')
async def update_book(updated_book=Body()) -> None:
  for i in range(len(BOOKS)):
    if BOOKS[i]['title'].casefold() == updated_book['title'].casefold():
      BOOKS[i] = updated_book
