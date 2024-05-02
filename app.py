from flask import Flask, render_template, request, redirect
import csv
from io import TextIOWrapper
from models.main import Author
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index_view():
    if request.method == "POST":
        csv_authors = request.files.get("csv_authors")
        wrapper_authors = TextIOWrapper(csv_authors, encoding='utf-8')
        csv_reader = csv.reader(wrapper_authors, delimiter=',')
        Author.insert_many(csv_reader).execute()

    return render_template("pages/index.jinja")

@app.route("/authors")
def authors_view():
    page = request.args.get("page")
    offset = 10

    if page == None:
        return redirect("/authors?page=1")
    
    authors = Author.select().paginate(int(page), offset)
    total_pages = math.ceil(Author.select().count() / offset)
    
    return render_template("pages/authors.jinja", authors=authors, total_pages=total_pages)


@app.route("/delete")
def delete_view():
    Author.delete().execute()
    return redirect("/")