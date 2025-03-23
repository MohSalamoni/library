from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load books data from books.json
def load_books():
    with open('data/books.json') as f:
        return json.load(f)

# Save updated books data to books.json
def save_books(books):
    with open('data/books.json', 'w') as f:
        json.dump(books, f, indent=4)

# Search function to look for books by name or part of the name (case-insensitive)
def search_books(books, name):
    results = {}
    for book_id, book in books.items():
        if name.lower() in book['name'].lower():  # Check for partial match in book name
            results[book_id] = book
    return results

# Search function to look for books by name or part of the name (case-insensitive)
def search_books_modify(books, name):
    for book_id, book in books.items():
        if name.lower() in book_id.lower():  # Check for partial match in book name
           return book_id,book
    return None,None

# Home route to display all books
@app.route('/')
def index():
    books = load_books()  # Load books
    return render_template('index.html', books=books)

# Search page route
@app.route('/search', methods=['GET', 'POST'])
def search_page():
    books = {}
    search_query = None
    if request.method == 'POST':
        search_query = request.form.get('book_name')  # Get book name from form
        books = load_books()  # Load books from JSON
        books = search_books(books, search_query)  # Search for books matching the query
    return render_template('search.html', books=books, search_query=search_query)

# Modify page route
@app.route('/modify', methods=['GET', 'POST'])
def modify_page():
    book = None
    if request.method == 'POST':
        search_query = request.form.get('book_id')  # Get book name from form
        books = load_books()  # Load books from JSON
        book_id, book = search_books_modify(books, search_query)  # Search for the book

        if book:
            return render_template('modify.html', book=book, book_id=book_id)
        else:
            return render_template('modify.html', book=None, search_query=search_query)

    return render_template('modify.html', book=None)

# Add page route
@app.route('/add', methods=['GET', 'POST'])
def add_page():
    message = None
    if request.method == 'POST':
        books = load_books()
        book_id = request.form.get('id')
        book_name = request.form.get('name')
        book_status = request.form.get('status')
        book_count = int(request.form.get('count'))

        if book_id in books:
            message = f"Book ID {book_id} already exists. Please use a different ID."
        else:
            books[book_id] = {
                "name": book_name,
                "status": book_status,
                "count": book_count
            }
            save_books(books)
            message = f"Book ID {book_id} has been successfully added."

    return render_template('add.html', message=message)

# Route to delete a book
@app.route('/delete', methods=['GET', 'POST'])
def delete_book():
    message=''
    if request.method == 'POST':
        book_id = request.form.get('book_id')  # Get the book ID from the form
        books = load_books()

        if book_id in books:
            del books[book_id]  # Delete the book from the dictionary
            save_books(books)  # Save the updated data back to the JSON file
            message = f"Book with ID {book_id} has been deleted successfully."
        else:
            message = f"Book with ID {book_id} does not exist."


    return render_template('delete.html', message=message)

# Update book route
@app.route('/update/<book_id>', methods=['POST'])
def update_book(book_id):
    books = load_books()  # Load books from JSON
    book = books[book_id]
    book['name'] = request.form['name']
    book['status'] = request.form['status']
    book['count'] = int(request.form['count'])
    save_books(books)  # Save updated data back to JSON
    return redirect(url_for('index'))  # Redirect to the home page after updating


if __name__ == '__main__':
    app.run(debug=True)
