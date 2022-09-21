from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
"""With flask_sqlalchemy it is not needed to import sqlite3 """
import sqlite3


app = Flask(__name__)
"""SQLALchemy"""
"""Connection between sqlite and SQLALchemy. by naming and allocating the db """
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
"""class with a structure and condition of the db"""
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Books %r>' % self.title
"""creation of the db with the containt from the class """
db.create_all()

# new_book = Book(id=1, title='Las Historias de Belzebuth a su nieto', author='George Gurddieff', rating=10)
# db.session.add(new_book)
# db.session.commit()
""" sqlite3
db = sqlite3.connect("books-collection.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
db.commit()
"""
all_books = []



@app.route('/')
def home():
    """variable create to render in the template in case there is not data in the db will
     display the text from the variable"""
    empty="Library is empty."
    """all the data contain in the db """
    all_books = Book.query.all()
    return render_template('index.html', books=all_books,empty=empty)

"""(CREATE)To add a new data to the db"""
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        #This is when there is not db
        # new_book = {
        #     "title": request.form['title'],
        #     "author": request.form['author'],
        #     "rating": request.form['rating']
        # }
        # all_books.append(new_book)
        # print(all_books)"""
        return redirect(url_for('home'))
    return render_template('add.html')

"""(UPDATE)To edit a choosen data that it is in the db"""
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        #UPDATE RECORD
        """the id of the element as  reference"""
        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        """data that will be updated"""
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit.html", book=book_selected)


"""(DELETE)To delete an element in the db"""
@app.route('/delete', methods=['GET','POST'])
def delete():
    """the id of the element as  reference"""
    book_id = request.args.get('id')
    delete_book = Book.query.get(book_id)
    db.session.delete(delete_book)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

