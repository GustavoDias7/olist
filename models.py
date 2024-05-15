from peewee import *

db = SqliteDatabase('database.sqlite3', pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db

class Author(BaseModel):
    id = AutoField()
    name = CharField()

class Book(BaseModel):
    id = AutoField()
    name = CharField()
    edition = IntegerField()
    publication_year = DateField()

class AuthorBook(BaseModel):
    author_id = ForeignKeyField(Author, backref="authorbooks")
    book_id = ForeignKeyField(Book, backref="authorbooks")

    class Meta:
        primary_key = CompositeKey('author_id', 'book_id')


db.create_tables([Author, Book, AuthorBook])