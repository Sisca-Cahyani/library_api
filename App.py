from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

# Dummy data
books = [
    {'id': 1, 'title': 'Book 1', 'author': 'Author 1', 'available': True},
    {'id': 2, 'title': 'Book 2', 'author': 'Author 2', 'available': True}
]

@app.route('/')
def index():
    return render_template('index.html', books=books)

@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify({'book': book})
    return jsonify({'message': 'Book not found'}), 404

@app.route('/api/books', methods=['POST'])
def create_book():
    new_book = request.get_json()
    new_book['id'] = len(books) + 1
    new_book['available'] = True
    books.append(new_book)
    return jsonify({'book': new_book}), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_book = request.get_json()
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        book.update(updated_book)
        return jsonify({'book': book})
    return jsonify({'message': 'Book not found'}), 404

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return jsonify({'message': 'Book deleted'})

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    if title and author:
        new_book = {
            'id': len(books) + 1,
            'title': title,
            'author': author,
            'available': True
        }
        books.append(new_book)
    return redirect(url_for('index'))

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book_form(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return redirect(url_for('index'))

@app.route('/update_book/<int:book_id>', methods=['POST'])
def update_book_form(book_id):
    title = request.form.get('title')
    author = request.form.get('author')
    book = next((book for book in books if book['id'] == book_id), None)
    if book and title and author:
        book['title'] = title
        book['author'] = author
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
