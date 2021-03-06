from flask import request
from bs4 import BeautifulSoup
import requests
import json
import asyncio
import aiohttp
import flask

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>tangthuvien API home page</p>'''

@app.route('/api/chapters', methods=['GET'])
@app.route('/api/books/contents', methods=['GET'])
def api_books_contents():
    try:
        url = request.args['url']
        html = requests.get(url)    
        soup = BeautifulSoup(html.content,'html.parser')
        # Create an empty dictionary for our results
        info = {}
        info['source'] = 'truyen.tangthuvien.vn'

        # Find chapter title and book title container
        info['book_title'] = soup.find('h1', attrs={"class":"truyen-title"}).find('a')['title']   
        info['chapter_title'] = soup.find('h2').get_text()

        book_id = soup.find('input', attrs = {'name':'story_id'})['value']       

        # Find chapters and seasons container
        hidden_url = "https://truyen.tangthuvien.vn/doc-truyen/page/" + book_id + "?page=0&limit=18446744073709551615&web=1"

        hidden_html = requests.get(hidden_url)
        hidden_soup = BeautifulSoup(hidden_html.content, 'html.parser')
        chapters = hidden_soup.find('ul').find_all('li', attrs={'class':None})
        info['prev_chap'] = ""
        info['next_chap'] = ""

        # Loop through chapters list to push chapters and seasons into container list
        for idx, chap in enumerate(chapters):
            chapter_name = chap.find('a')['title']
            if chapter_name == info['chapter_title']:
                chapter_idx = idx + 1

                if chapter_idx > 0:
                    try:
                        info['prev_chap'] = chapters[idx-1].find('a')['href']
                    except:
                        pass

                if chapter_idx < len(chapters):
                    try:
                       info['next_chap'] = chapters[idx+1].find('a')['href']
                    except:
                        pass
                break

        rows = soup.find_all('div')
        # Loop through the data and match results that fit the requested url.        
        for index in range(40, len(rows)):
            row = rows[index]
            if "box-chap box-chap" in str(row):
                info['content'] = row.get_text()
                break

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
        info['source'] = 'truyen.tangthuvien.vn'

        # Find book id container    
        book_id = soup.find('meta', attrs ={"name":"book_detail"})['content']
        info['book_id'] = book_id

        # Find book cover image container
        info['img_url'] = soup.find('a', attrs ={"id":"bookImg"}).find('img')['src']

        # Find book name, book info and book author container
        info['book_name'] = soup.find('h1').get_text()
        info['book_author'] = soup.find('div', attrs ={'id':'authorId'}).find('p').get_text()    
        info['book_intro'] = soup.find('div', attrs ={'class':'book-intro'}).find('p').get_text()

        # Create lists to store multiple chapters and seasons
        info['chapter_name'] = []
        info['chapter_link'] = []
        info['season_name'] = []
        info['season_index'] = []

        # Find first season container
        info['season_name'].append(soup.find('li', attrs ={"class":"divider-chap"}).get_text())
        info['season_index'].append(0)
        
        # Find chapters and seasons container
        hidden_url = "https://truyen.tangthuvien.vn/doc-truyen/page/" + book_id + "?page=0&limit=18446744073709551615&web=1"
        hidden_html = requests.get(hidden_url)
        hidden_soup = BeautifulSoup(hidden_html.content, 'html.parser')
        chapters = hidden_soup.find('ul').find_all('li')

        # Loop through chapters list to push chapters and seasons into container list
        for chap in chapters:
            try:
                info['chapter_name'].append(chap.find('a')['title'])
                info['chapter_link'].append(chap.find('a')['href'])
            except:
                season = chap.find('span').get_text()
                if info['season_name'][len(info['season_name']) - 1][:8] == season[:8]:
                    continue
                info['season_name'].append(season)
                info['season_index'].append(len(info['chapter_name']))

        info['season_index'].append(len(info['chapter_name']))   

        return json.dumps(info)

    except Exception as e:
        return "Unable to get url {} due to {}.".format(url, e.__class__)

async def get(semaphore, url, session, timeout=10):
    try:
        async with semaphore:
            # with async_timeout.timeout(timeout):
                async with session.get(url=url) as response:
                    # print(response.status)
                    resp = await response.read()
                    soup = BeautifulSoup(resp.decode('utf-8'), 'html5lib')

                    return soup
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))

async def get_chapters(urls):
    try:
        sem = asyncio.Semaphore(1)
        # timeout = 3.5
        # with async_timeout.timeout(timeout):
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(*[get(sem, url, session) for url in urls])
        return ret         
    except Exception as e:
        print("Unable to get chapters due to {}.".format(e.__class__))

def async_books_contents(soup, idx):    
    try:
        # Create an empty dictionary for our results
        info = {}
        info['source'] = 'truyen.tangthuvien.vn'
        # Find chapter title and book title container
        info['book_title'] = soup.find('h1', attrs={"class":"truyen-title"}).find('a')['title']   
        info['chapter_title'] = soup.find('h2').get_text()

        rows = soup.find_all('div')

        # Loop through the data and match results that fit the requested url.        
        for index in range(len(rows)):
            if index < 40:
                continue
            row = rows[index]
            if "box-chap box-chap" in str(row):
                chap_id = row['class'][1][9:]
                info['content'] = row.get_text()
                break
        story_id = soup.find('input', attrs = {'name':'story_id'})['value']
        
        info['next_4_url'] = 'https://truyen.tangthuvien.vn/get-4-chap?story_id=' + str(story_id) + '&chap_id=' + str(chap_id) + '&sort_by_ttv=' + str(idx)

        return info
    except Exception as e:
        print("Unable to get book contents async due to {}.".format(e.__class__))

def get_4_next(soup, title):
    try:
        # Create an empty dictionary for our results
        result = []

        chap_titles = soup.find_all('h5')
        chap_contents = soup.find_all('div', attrs = {'class':'box-chap'})

        for chap_idx in range(len(chap_titles)):
            info = {}
            info['source'] = 'truyen.tangthuvien.vn'
            # Find chapter title and book title container
            info['book_title'] = title  
            info['chapter_title'] = chap_titles[chap_idx].get_text()
            info['content'] = chap_contents[chap_idx].get_text()        
            result.append(info) 

        return result
    except Exception as e:
        pass

@app.route('/api/async/books', methods=['GET'])
def async_api_books():
    try:
        url = request.args['url']
        html = requests.get(url)
        soup = BeautifulSoup(html.content,'html.parser')

        # Create an empty dictionary for our results
        info = {}

        # Add book source
        info['source'] = 'truyen.tangthuvien.vn'

        # Find book id container    
        book_id = soup.find('meta', attrs ={"name":"book_detail"})['content']
        info['book_id'] = book_id

        # Find book cover image container
        info['img_url'] = soup.find('a', attrs ={"id":"bookImg"}).find('img')['src']

        # Find book name, book info and book author container
        info['book_name'] = soup.find('h1').get_text()
        info['book_author'] = soup.find('div', attrs ={'id':'authorId'}).find('p').get_text()    
        info['book_intro'] = soup.find('div', attrs ={'class':'book-intro'}).find('p').get_text()

        # Create lists to store multiple chapters and seasons
        info['chapter_name'] = []
        info['chapter_link'] = []
        info['season_name'] = []
        info['season_index'] = []

        # Find first season container
        info['season_name'].append(soup.find('li', attrs ={"class":"divider-chap"}).get_text())
        info['season_index'].append(0)

        # Find chapters and seasons container
        hidden_url = "https://truyen.tangthuvien.vn/doc-truyen/page/" + book_id + "?page=0&limit=18446744073709551615&web=1"
        hidden_html = requests.get(hidden_url)
        hidden_soup = BeautifulSoup(hidden_html.content, 'html.parser')
        chapters = hidden_soup.find('ul').find_all('li')

        # Loop through chapters list to push chapters and seasons into container list
        for chap in chapters:
            try:
                info['chapter_name'].append(chap.find('a')['title'])
                info['chapter_link'].append(chap.find('a')['href'])
            except:
                season = chap.find('span').get_text()
                if info['season_name'][len(info['season_name']) - 1][:8] == season[:8]:
                    continue
                info['season_name'].append(season)
                info['season_index'].append(len(info['chapter_name']))

        info['season_index'].append(len(info['chapter_name']))   
        info['chapter_contents'] = [None] * len(info['chapter_link'])

        chapters_first_of_5 = []
        chapters_get_4 = []
        index = 0
        while index < len(info['chapter_link']):
            chapters_first_of_5.append(info['chapter_link'][index])
            index += 5

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        first_of_5_soups = loop.run_until_complete(get_chapters(chapters_first_of_5))

        for idx, soup in enumerate(first_of_5_soups):
            chapter = async_books_contents(soup, idx*5 + 1)
            chapters_get_4.append(chapter['next_4_url'])
            chapter.pop('next_4_url', None)
            info['chapter_contents'][idx*5] = chapter

        get_4_soups = loop.run_until_complete(get_chapters(chapters_get_4))
        
        for idx, soup in enumerate(get_4_soups):
            chapters = get_4_next(soup, info['chapter_contents'][idx*5]['chapter_title'])
            for chap_idx, chap in enumerate(chapters):
                info['chapter_contents'][idx*5 + chap_idx + 1] = chap

        return json.dumps(info)

    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))