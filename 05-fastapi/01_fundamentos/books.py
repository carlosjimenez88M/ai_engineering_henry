"""
Fundamentos de FastAPI: rutas, path params, query params y cuerpo de solicitud.

CRUD básico sobre una lista en memoria, sin base de datos.
Introduce GET, POST, PUT y DELETE con FastAPI puro.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Clase 1: FastAPI Fundamentos - Henry AI Engineering

from fastapi import Body, FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Batman: Year One',        'author': 'Frank Miller', 'category': 'superhero'},
    {'title': 'The Dark Knight Returns', 'author': 'Frank Miller', 'category': 'superhero'},
    {'title': 'Watchmen',                'author': 'Alan Moore',   'category': 'graphic-novel'},
    {'title': 'The Killing Joke',        'author': 'Alan Moore',   'category': 'graphic-novel'},
    {'title': 'Green Lantern: Rebirth',  'author': 'Geoff Johns',  'category': 'superhero'},
    {'title': 'Superman: Red Son',       'author': 'Mark Millar',  'category': 'graphic-novel'},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# Get all books from a specific author using path or query parameters
@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
