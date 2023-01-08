from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "bababoobli"




app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)
db.init_app(app)

class BookDataBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()
    db_books = db.session.query(BookDataBase).all()


all_books = []

class BookForm(FlaskForm):
    book_name = StringField(label='Book name', validators=[DataRequired()])
    book_author = StringField(label='Book author', validators=[DataRequired()])
    book_rating = StringField(label='Book rating', validators=[DataRequired()])
    submit = SubmitField(label='submit')


class DataBaseForm(FlaskForm):
    new_rating = StringField(label='New rating')
    submit = SubmitField(label='Submit')

@app.route('/')
def home():
    return render_template('index.html', books=db_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    book_form = BookForm()
    if book_form.submit.data == True:
        new_book = BookDataBase(title=book_form.book_name.data, author=book_form.book_author.data, rating=book_form.book_rating.data)
        db.session.add(new_book)
        db.session.commit()


    return render_template('add.html', form=book_form)


@app.route('/edit', methods=['GET', 'POST'])
def edit():

    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = BookDataBase.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))



    book_id = request.args.get('id')
    book_selected = BookDataBase.query.get(book_id)

    return render_template('edit.html', book= book_selected)

if __name__ == "__main__":
    app.run(debug=True)

