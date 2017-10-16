import requests
from bs4 import BeautifulSoup


count = 0
url = 'https://en.wikipedia.org/wiki/Special:AllPages'
main_url = 'https://en.wikipedia.org'
while True:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    collection = soup.find('div', {'class': 'mw-allpages-body'})
    collection = collection.findAll('li')
    nav = soup.find('div', {'class': 'mw-allpages-nav'})
    next_page = nav.findAll('a')[-1]
    next_page_str = next_page.string

    if next_page_str.startswith('Next page'):
        print(count)
        count += 1
        url  = main_url + str(next_page.get('href'))
    else:
        break

    for i, el in enumerate(collection):
        clas = el.get('class')
        if clas is not None and 'allpagesredirect' in clas:
            continue
        else:
            link = el.find('a')
            href = str(main_url + str(link.get('href')))
            if href.startswith('https://en.wikipedia.org/wiki/List_of'):
                continue
            if href.startswith('https://en.wikipedia.org/Category:'):
                continue
            if href.startswith('https://en.wikipedia.org/wiki/Wikipedia:'):
                continue
            if href.startswith('https://en.wikipedia.org/wiki/Help:'):
                continue
            if href.startswith('https://en.wikipedia.org/wiki/Special:'):
                continue
            if href.endswith('(disambiguation)'):
                continue
            if href.startswith('https://en.wikipedia.org/wiki/Portal:'):
                continue
            if 'talk:' in href.lower():
                continue
            if 'user:' in href.lower():
                continue
            if 'file:' in href.lower():
                continue
            if '/wiki/mediawiki:' in href.lower():
                continue
            if '/wiki/template:' in href.lower():
                continue
            if '/wiki/book:' in href.lower():
                continue
            if '/wiki/draft:' in href.lower():
                continue
            if '/wiki/timedtext:' in href.lower():
                continue
            if '/wiki/module:' in href.lower():
                continue
            if '/wiki/timedtext:' in href.lower():
                continue
            f = open('links.txt', 'a')
            print(href, file=f)
            f.close()
f.close()