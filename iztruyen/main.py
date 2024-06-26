from bs4 import BeautifulSoup
import requests
import json
import flask
from flask import request

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>iztruyen API home page</p>'''

@app.route('/api/chapters', methods=['GET'])
@app.route('/api/books/contents', methods=['GET'])
def api_books_contents():
    try:
        url = request.args['url']        
        html = requests.get(url)        
        soup = BeautifulSoup(html.content,'html.parser')

        # Create an empty dictionary for our results
        info = {}
        info['source'] = 'iztruyen.com'
        info['next_chap'] = ""
        info['prev_chap'] = ""

        try:
            info['prev_chap'] = soup.find('div', attrs={'class':'nav-previous'}).find('a')['href']
        except:
            pass

        try:
            info['next_chap'] = soup.find('div', attrs={'class':'nav-next'}).find('a')['href']
        except:
            pass
        # Find chapter title and book title container
        titles = soup.find('ol', attrs={'class':'breadcrumb'}).find_all('li')

        for idx, title in enumerate(titles):
            if idx == 1:
                info['book_title'] = title.find('a').get_text().replace("\n","").replace("\t","")
            elif idx == 2:
                info['chapter_title'] = title.get_text().replace("\n","").replace("\t","")

        # Find chapter content container
        info['content'] = ""
        contents = soup.find('div', attrs={'class':'reading-content'}).find_all('p')
        for content in contents:
            info['content'] += content.get_text() + '\n'

        return json.dumps(info)

    except Exception as e:
        return "Unable to get url {} due to {}.".format(url, e.__class__)       
    
@app.route('/api/books', methods=['GET'])
def api_books():
    try:
        url = request.args['url']        
        html = requests.get(url)    
        soup = BeautifulSoup(html.content,'html.parser')

        # Create an empty dictionary for our results
        info = {}

        # Add book source    
        info['source'] = 'iztruyen.com'

        # Find book id container    
        info['book_id'] = soup.find('input', attrs ={'class':'rating-post-id'})['value']

        # Find book cover image container
        info['img_url'] = soup.find('div', attrs ={'class':'summary_image'}).find('img')['data-src']

        # Find book name, book info and book author container
        info['book_name'] = soup.find('div', attrs={'class':'post-title'}).find('h1').get_text().replace("\n","").replace("\t","").replace("\r","")

        info['book_intro'] = ""
        book_intros = soup.find('div', attrs ={'class':'description-summary'}).find_all('p')

        for book_intro in book_intros:
            info['book_intro'] += book_intro.get_text() + '\n'

        info['book_author'] = soup.find('div', attrs ={'class':'author-content'}).find('a').get_text()

        # Create lists to store multiple chapters
        info['chapter_name'] = []
        info['chapter_link'] = []
        info['season_name'] = []
        info['season_index'] = []
        info['has_seasons'] = False       
        # Find chapters container
        total_chapter = soup.find('ul', attrs={'class':'main version-chap'}).find_all('li')
        total_chapter.reverse()
        for chapter in total_chapter:
            info['chapter_name'].append(chapter.find('a').get_text().replace("\n","").replace("\t",""))
            info['chapter_link'].append(chapter.find('a')['href'])

        if len(info['season_name']) == 0:
            info['season_name'].append('Quyển 1')
            info['season_index'].append(0)
        
        return json.dumps(info)
    except Exception as e:
        return "Unable to get url {} due to {}.".format(url, e.__class__)   
        
@app.route('/api/async/books', methods=['GET'])
def async_api_books():
    pass

        