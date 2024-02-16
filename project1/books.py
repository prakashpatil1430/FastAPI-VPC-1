from fastapi import FastAPI, Body

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get('/books/{book_title}')
def get_a_book(book_title: str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book

# filter books by category   
@app.get('/books/')
async def read_book_by_category(category: str):
    book_list = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            book_list.append(book)
    return book_list


# filter books by author and category  
@app.get('/books/{author}/')
async def read_author_category_by_query(author:str, category: str):
    book_list = []
    for book in BOOKS:
        if (book.get('author').casefold() == author.casefold()  and 
            book.get('category').casefold() == category.casefold()
           ):
            book_list.append(book)
    return book_list



# post request create a book
@app.post('/books/create_book')
async def create_book(new_book=Body()):
    return BOOKS.append(new_book)



# update book
@app.put('/books/update_book')
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book
    return BOOKS



# delete book
@app.delete('/books/delete_book/{title}')
async def update_book(title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == title.casefold():
            BOOKS.pop(i)
            break
    return 'deleted'