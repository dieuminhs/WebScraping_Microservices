import flask
from flask import request, redirect
import requests

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/books', methods=['GET'])
def books_url():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'url' in request.args:
        url = request.args['url']
        books_source = url[8:]
        first_idx = books_source.find('.')
        second_idx = books_source.find('.', first_idx + 1, len(books_source))
        if second_idx == -1:
            second_idx = books_source.find('/', first_idx + 1, len(books_source))
        
        books_source = books_source[:second_idx]
        api_source = "https://ebook-" + books_source.replace('.', '-') + '.herokuapp.com'
        if requests.get(api_source).status_code == 200:
            return redirect(api_source + '/api/books?url=' + url)
        else:
            return "Error: Invalid books source."

    else:
        return "Error: No url field provided. Please specify an url."

@app.route('/api/books/contents', methods=['GET'])
@app.route('/api/chapters', methods=['GET'])
def books_contents_url():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.    
    if 'url' in request.args:
        url = request.args['url']
        books_source = url[8:]
        first_idx = books_source.find('.')
        second_idx = books_source.find('.', first_idx + 1, len(books_source))
        if second_idx == -1:
            second_idx = books_source.find('/', first_idx + 1, len(books_source))
        
        books_source = books_source[:second_idx]
        api_source = "https://ebook-" + books_source.replace('.', '-') + '.herokuapp.com'
        if requests.get(api_source).status_code == 200:
            return redirect(api_source + '/api/chapters?url=' + url)
        else:
            return "Error: Invalid books source."

    else:
        return "Error: No url field provided. Please specify an url."


@app.route('/api/async/books', methods=['GET'])
def async_books_url():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'url' in request.args:
        url = request.args['url']
        books_source = url[8:]
        first_idx = books_source.find('.')
        second_idx = books_source.find('.', first_idx + 1, len(books_source))
        if second_idx == -1:
            second_idx = books_source.find('/', first_idx + 1, len(books_source))
        
        books_source = books_source[:second_idx]
        api_source = "https://ebook-" + books_source.replace('.', '-') + '.herokuapp.com'
        if requests.get(api_source).status_code == 200:
            return redirect(api_source + '/api/async/books?url=' + url)
        else:
            return "Error: Invalid books source."

    else:
        return "Error: No url field provided. Please specify an url."