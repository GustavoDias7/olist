from flask import Flask, render_template, request, Response
from playhouse.shortcuts import model_to_dict
import csv
from io import TextIOWrapper
from models import Author, Book, AuthorBook
import math
import json
from validation import is_valid_number
import peewee
from peewee import fn, JOIN

app = Flask(__name__)

convert_ids = lambda s: [int(i) for i in (s or '').split(',') if i]

@app.route("/authors", methods=["GET", "POST", "PATCH", "DELETE"])
def authors_view():
    if request.method == "GET":
        try:
            page = request.args.get("page")

            if page == None:
                raise TypeError('The "page" param is required!') 

            if not is_valid_number(page):
                raise TypeError('The "page" param is an invalid number!') 
            
            # if page was a float string, raise ValueError
            page = int(page)
            offset = 10

            if page < 1:
                raise TypeError('The "page" param must be a positive integer greater then zero!') 
            
            authors = Author.select().paginate(page, offset)
            total_pages = math.ceil(Author.select().count() / offset)
            authors_dict = [model_to_dict(a) for a in authors]
            
            data = {
                "authors": authors_dict,
                "total_pages": total_pages
            }
            data["next_page"] = page + 1 if page < total_pages else None
            
            return Response(json.dumps(data, indent=2), status=200)

        except TypeError as e:
            return Response(str(e), status=400)
        
        except ValueError as e:
            msg = 'The "page" param must be a positive integer greater then zero!'
            return Response(msg, status=400)

    elif request.method == "POST":
        if request.is_json:
            try:
                data = request.json
                name = data.get("name")

                if name == None:
                    raise TypeError('The "name" property is required!') 
                
                if type(name) != str:
                    raise TypeError('The "name" property must be a string!') 
                
                if name == "":
                    raise ValueError('The "name" property cannot be an empty string!') 

                author = Author(name=name)
                author.save()

                return Response(json.dumps(data, indent=2), status=200)
            except Exception as e:
                return Response(str(e), status=400)

        else:
            return Response("There is no json!", status=400)
        
        
    elif request.method == "PATCH":
        data = request.json

        id = data.get("id")
        name = data.get("name")

        author = Author.get(Author.id == id)

        if name: author.name = name
                
        author.save()  # Save the changes
        book_dict = model_to_dict(author)
        
        return Response(json.dumps(book_dict, indent=2), status=200)

    elif request.method == "DELETE":
        authors = Author.delete().execute()
        return Response(json.dumps(authors, indent=2), status=200)
    
@app.route("/book", methods=["GET", "POST", "PATCH", "DELETE"])
def book_view():
    if request.method == "GET":
        try:
            allowed_args = ["id", "name", "edition", "publication_year"]
            args = {}
            for ra in request.args:
                if ra in allowed_args:
                    args[ra] = request.args[ra]

            expression = None
            for i, x in enumerate(args):
                if i == 0:
                    expression |= (getattr(Book,x) == args.get(x))
                else:
                    expression &= (getattr(Book,x) == args.get(x))

            book = (Book
                .select(
                    Book,
                    fn.GROUP_CONCAT(Author.id).python_value(convert_ids).alias('authors'),
                )
                .join(AuthorBook, JOIN.LEFT_OUTER, on=(Book.id == AuthorBook.book_id))
                .join(Author, JOIN.LEFT_OUTER, on=(Author.id == AuthorBook.author_id))
                .group_by(Book)
            )
            
            if expression != None:
                book = book.where(expression)

            book_dict = [b for b in book.dicts()]

            return Response(json.dumps(book_dict), status=200)
        except peewee.DoesNotExist as e:
            id = request.args.get("id")
            return Response(f"The id '{id}'' does not exist.", status=400)
        except Exception as e:
            return Response(str(e), status=400)
    
    elif request.method == "POST":
        try:
            data = request.json
            name = data.get("name")
            edition = data.get("edition")
            publication_year = data.get("publication_year")
            authors = data.get("authors")

            book = Book(
                name=name, 
                edition=edition, 
                publication_year=publication_year
            )
            book.save()

            authorbook_list = []
            if authors and type(authors) == list and len(authors) > 0:
                for author in authors:
                    authorbook_list.append({
                        "author_id": author,
                        "book_id": book.id
                    })
                AuthorBook.insert_many(authorbook_list).execute()

            book_dict = model_to_dict(book)
            book_dict["authors"] = [a["author_id"] for a in authorbook_list]

            return Response(json.dumps(book_dict, indent=2))
        except Exception as e:
            return Response(str(e), status=400)
    
    elif request.method == "PATCH":
        data = request.json

        id = data.get("id")
        name = data.get("name")
        edition = data.get("edition")
        publication_year = data.get("publication_year")

        book = Book.get(Book.id == id)

        if edition: book.edition = edition
        if name: book.name = name
        if publication_year: book.publication_year = publication_year
                
        book.save()  # Save the changes
        book_dict = model_to_dict(book)
        
        return Response(json.dumps(book_dict, indent=2), status=200)

    elif request.method == "DELETE":
        id = int(request.args.get("id"))
        book = Book.delete().where(Book.id == id)
        book.execute()
        return Response(f"The book {id} has been deleted!", status=200)
