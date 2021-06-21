from bs4 import BeautifulSoup
import requests
import json
import asyncio
import aiohttp
import flask
from flask import request

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>trumtruyen API home page</p>'''

@app.route('/api/chapters', methods=['GET'])
@app.route('/api/books/contents', methods=['GET'])
def api_books_contents():
    try:
        url = request.args['url']        
        html = requests.get(url)        
        soup = BeautifulSoup(html.content,'html.parser')

        # Create an empty dictionary for our results
        info = {}
        info['source'] = 'trumtruyen.net'
        
        # Find chapter title and book title container
        info['book_title'] = soup.find('a', attrs={"class":"truyen-title"}).get_text()
        info['chapter_title'] = soup.find('a', attrs={"class":"chapter-title"}).get_text()
        info['prev_chap'] = soup.find('a', attrs={'id':'prev_chap'})['href']
        info['next_chap'] = soup.find('a', attrs={'id':'next_chap'})['href']
        if info['source'] not in info['prev_chap']:
            info['prev_chap'] = ""
        if info['source'] not in info['next_chap']:
            info['next_chap'] = ""

        info['content'] = ""
        # Loop through the data and match results that fit the requested url.        
        contents = soup.find('div',attrs={'id':'chapter-c'})
        for content in contents:
            try:
                content.get_text()
                info['content'] += '\n'
            except:
                info['content'] += content                
        
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
        info['source'] = 'trumtruyen.net'

        # "Domain name to access data"
        domain = 'https://trumtruyen.net'

        # Find book id container    
        book_id = soup.find('input', attrs={'id':'truyen-id'})['value']
        total_page = int(soup.find('input', attrs={'id':'total-page'})['value'])
        book_name = soup.find('input', attrs={'id':'truyen-ascii'})['value']
        info['book_id'] = book_id

        # Find book cover image container
        info['img_url'] = soup.find('div', attrs ={'class':'book'}).find('img')['src']

        # Find book name, book info and book author container
        info['book_name'] = soup.find('h3', attrs={'class':'title'}).get_text()
        info['book_intro'] = ""

        intros = soup.find('div',attrs={'class':'desc-text'})
        for intro in intros:
            try:
                intro.get_text()
                info['book_intro'] += '\n'
            except:
                info['book_intro'] += intro

        info['book_author'] = soup.find('a', attrs ={'itemprop':'author'}).get_text()

        # Create lists to store multiple chapters
        info['chapter_name'] = []
        info['chapter_link'] = []
        info['season_name'] = []
        info['season_index'] = []
        info['has_seasons'] = False       
        page_link = []
        for page_idx in range(1, total_page + 1):
            page_link.append('https://trumtruyen.net/ajax.php?type=list_chapter&tid=' + str(book_id) + '&tascii=' + str(book_name) + '&page=' + str(page_idx) + '&totalp=50')

        # Find chapters container
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        soups = loop.run_until_complete(get_chapters(page_link))
        for s in soups:
            for i in s.find_all('a'):
                info['chapter_link'].append(i['href'])
                info['chapter_name'].append(i['title'])

        if len(info['season_name']) == 0:
            info['season_name'].append('Quyển 1')
            info['season_index'].append(0)

        return json.dumps(info)
    except Exception as e:
        return "Unable to get url {} due to {}.".format(url, e.__class__)   

async def get(semaphore, url, session, timeout=10):
    try:
        async with semaphore:
            # with async_timeout.timeout(timeout):
                async with session.get(url=url) as response:
                    
                    resp = await response.json()
                    
                    soup = BeautifulSoup(resp['chap_list'], 'html.parser')
                    return soup
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))

async def get_chapters(urls):
    sem = asyncio.Semaphore(1)
    
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(sem, url, session) for url in urls])
    return ret         

@app.route('/api/async/books', methods=['GET'])
def async_api_books():
    pass