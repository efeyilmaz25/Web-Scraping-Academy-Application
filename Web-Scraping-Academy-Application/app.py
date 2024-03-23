from flask import Flask, render_template, request
import pymongo
from bson import Code

app = Flask(__name__)

# MongoDB database connection -----
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydatabase = client["articledatabase"]
mycollection = mydatabase["articledatas"]

# Home page -----
@app.route('/')
def index():
    articles = mycollection.find()
    return render_template('index.html', articles=articles)


# Sorting function -----
@app.route('/sort')
def sort():
    column = request.args.get('column')
    order = request.args.get('order')

    sort_direction = pymongo.ASCENDING if order == 'asc' else pymongo.DESCENDING


    if column == '10':
        articles = mycollection.find().sort("Article quotes", sort_direction)
    elif column == '1':
        articles = mycollection.find().sort("Article name", sort_direction)
    elif column == '0':
        articles = mycollection.find().sort("Article id", sort_direction)
    else:
        sort_key = list(mycollection.find().limit(1))[0].keys()[int(column)]
        articles = mycollection.find().sort(sort_key, sort_direction)

    
    return render_template('index.html', articles=articles)


# Filtering function -----
@app.route('/filter')
def filter_by_article_type():
    article_type = request.args.get('type')
    articles = mycollection.find({"Article types": article_type})
    return render_template('index.html', articles=articles)


# Sorting function -----
@app.route('/sortByArticleAuthors')
def sort_by_article_authors():
    articles = list(mycollection.find())
    articles.sort(key=lambda x: x["Article authors"].count(','), reverse=True)
    return render_template('index.html', articles=articles)


# Sorting function -----
@app.route('/sortByArticleKeywords')
def sort_by_article_keywords():
    articles = list(mycollection.find())
    articles.sort(key=lambda x: x["Article keywords"].count(','), reverse=True)
    return render_template('index.html', articles=articles)



if __name__ == '__main__':
    app.run(debug=True)

