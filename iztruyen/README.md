# WebScraping
## 1/ Installation instruction:
- Install python (https://www.python.org/downloads/), check yes for Environment Path
- Install flask, beautifulsoup4, requests, lxml, html5lib, asyncio, aiohttp (use the below command in command line)
+ Command line: pip install flask bs4 requests lxml html5lib asyncio aiohttp
- Run the local server using:
  + Run using command line (python wsgi.py)
  + Run build using a code editor, tools (Visual studio code, Visual studio 20xx, Jupyter notebook)
## 2/ Local server usage:
- The local server is running on http://127.0.0.1:5000/
- There are currently 3 function available:
  + Get chapter details from the chapter page of a book (http://127.0.0.1:5000/api/books/contents?url=pageUrl)
    + e.g: http://127.0.0.1:5000/api/books/contents?url=https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien/chuong-4
    + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien/chuong-4
      * The returned value will be in json format contains 3 keys:
        + "book_title": contains the book title
        + "chapter_title": contains the chapter title
        + "content": contains chapter contents
    + You can use http://127.0.0.1:5000/api/chapters?url=pageUrl as alternative url
    
  + Get book details from the main page of a book (http://127.0.0.1:5000/api/books?url=pageUrl)
    + e.g: http://127.0.0.1:5000/api/books?url=https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien
    + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien
      * The returned value will be in json format contains 8 keys:
        + "img_url": contains the url of the book cover
        + "book_name": contains the book name
        + "book_intro": contains the book introduction
        + "book_author": contains the author name of the book
        + "chapter_name": contains the list of chapter name of the book
        + "chapter_link": contains the list of chapter link correspond to the chapter_name (link[i] will be the link for chapter_name[i])
        + "season_name": some books will contain seasons and each season the chapter number will start over, this key will contain the list of season number and season name
        + "season_index": contains a list that indicate index of the beginning chapter of each season in chapter_name (season_index[i] will return beginning chapter index of season[i]). This means the list of chapter of season[i] will from chapter_name[season_index[i]] to chapter_name[season_index[i+1]]
        
  + Get book details and chapter details asynchronously from the main page of a book (http://127.0.0.1:5000/api/async/books?url=pageUrl)
    + e.g: http://127.0.0.1:5000/api/async/books?url=https://truyen.tangthuvien.vn/doc-truyen/truong-da-du-hoa
    + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/truong-da-du-hoa
      * The returned value will be in json format contains 9 keys, the first 8 keys is the same as get book details function, the 9th key is:
        + "chapter_contents": contains the details of all chapters of the books (chapter_contents[i] will contain chapter_link[i] chapter details]).
 
- There are currently two sites that is able to parse data from: 
    1/ tangthuvien.vn
    2/ truyenchu.vn (This site doesn't seperate seasons with chapters so the size of season_name and season_index will be 0)
    
## 3/ Deployed server usage:
- The deployed server is running on https://flask-web-scraping.herokuapp.com/
- There are currently 2 function available:
  + Get book details from the chapter page of a book (https://flask-web-scraping.herokuapp.com/api/books/contents?url=pageUrl)
    + e.g: https://flask-web-scraping.herokuapp.com/api/books/contents?url=https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien/chuong-4
    + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien/chuong-4
    + You can use https://flask-web-scraping.herokuapp.com/api/chapters?url=pageUrl as alternative url

  + Get book details from the main page of a book (https://flask-web-scraping.herokuapp.com/api/books?url=pageUrl)
    + e.g: https://flask-web-scraping.herokuapp.com/api/books?url=https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien
    + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien

  + Get book details and chapter details asynchronously from the main page of a book (https://flask-web-scraping.herokuapp.com/api/async/books?url=pageUrl)
    + e.g: https://flask-web-scraping.herokuapp.com/api/async/books?url=https://truyen.tangthuvien.vn/doc-truyen/truong-da-du-hoa
    + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/truong-da-du-hoa
