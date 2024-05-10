from peewee import *

db = SqliteDatabase('database.sqlite3')

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
    author = ForeignKeyField(Author)
    book = ForeignKeyField(Book)

    class Meta:
        primary_key = CompositeKey('author', 'book')


db.create_tables([Author, Book, AuthorBook])