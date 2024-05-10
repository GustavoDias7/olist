from flask import Flask, render_template, request, redirect, Response
from playhouse.shortcuts import model_to_dict
import csv
from io import TextIOWrapper
from models import Author, Book, AuthorBook
import math
import json
from validation import is_valid_number

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index_view():
    if request.method == "POST":
        csv_authors = request.files.get("csv_authors")
        wrapper_authors = TextIOWrapper(csv_authors, encoding='utf-8')
        csv_reader = csv.reader(wrapper_authors, delimiter=',')
        Author.insert_many(csv_reader).execute()

    return render_template("pages/index.jinja")


@app.route("/authors", methods=["GET", "POST", "DELETE"])
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
                # get data
                data = request.json
                name = data.get("name")

                if name == None:
                    raise TypeError('The "name" property is required!') 
                
                if type(name) != str:
                    raise TypeError('The "name" property must be a string!') 
                
                if name == "":
                    raise ValueError('The "name" property cannot be empty!') 

                # save the author
                author = Author(name=name)
                author.save()

                return Response(json.dumps(data, indent=2), status=200)
            except Exception as e:
                return Response(str(e), status=400)

        else:
            return Response("There is no json!", status=400)

    elif request.method == "DELETE":
        authors = Author.delete().execute()
        return Response(json.dumps(authors, indent=2), status=200)

@app.route("/delete")
def delete_view():
    Author.delete().execute()
    return redirect("/")