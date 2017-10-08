import requests
from bs4 import BeautifulSoup
from collections import defaultdict

main_url = 'https://en.wikipedia.org'
url = 'https://en.wikipedia.org/wiki/Flash_(comics)'

def generate_graph(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.find('div', {'class': 'mw-parser-output'})
    links = content.findAll('a', href=True, title=True)
    for i, el in enumerate(links):
        if not str(el.get('href')).strip().startswith('/wiki/'):
            del links[i]
        if str(el.get('title')).strip().startswith('Category:'):
            del links[i]
        if str(el.get('title')).strip().startswith('Help:'):
            del links[i]
        if str(el.get('title')).strip().startswith('Wikipedia:'):
            del links[i]
        if str(el.get('title')).strip().startswith('Special:'):
            del links[i]
        if str(el.get('href')).strip().startswith('/wiki/List_of'):
            del links[i]
        if str(el.get('title')).strip().endswith('(disambiguation)'):
            del links[i]
        if str(el.get('title')).strip().startswith('Edit section'):
            del links[i]
        if str(el.get('title')).strip().startswith('Enlarge'):
            del links[i]
        if 'mw-redirect' in str(el.get('class')).strip():
            del links[i]

    pairs = []
    for i, el in enumerate(links):
        href = main_url + str(el.get('href')).strip()
        title = str(el.get('title')).strip()
        if not href.startswith('https://en.wikipedia.org/wiki/'):
            continue
        if title.startswith('Category:'):
            continue
        if title.startswith('Help:'):
            continue
        if title.startswith('Wikipedia:'):
            continue
        if title.startswith('Special:'):
            continue
        if title.startswith('/wiki/List_of'):
            continue
        if title.endswith('(disambiguation)'):
            continue
        if title.startswith('Edit section'):
            continue
        if title.startswith('Enlarge'):
            continue
        if 'mw-redirect' in str(el.get('class')).strip():
            continue
        if '#' in href:
            index = href.index('#')
            href = href[:index]
        pairs.append((title, href))

    fq = defaultdict(int)
    for pair in pairs:
        fq[pair] += 1

    value_dict = dict(fq)
    return value_dict

def print_sorted(value_dict, l=1):
    sorted_values = sorted(value_dict, key=lambda x:value_dict[x])
    for k in sorted_values:
        if value_dict[k] >= l:
            print("{}: {}".format(k, value_dict[k]))

value_dict = generate_graph(url)
print_sorted(value_dict, l=3)