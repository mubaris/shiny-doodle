import math
from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup
from py2neo import Graph, Node, Relationship, NodeSelector
from secret import password


def generate_graph(G, url, l=1, max_nodes=50):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    header = str(soup.find('h1', {'id': 'firstHeading', 'class': 'firstHeading'}).text).strip()
    try:
        soup.find('div', {'class': 'reflist'}).decompose()
    except:
        pass
    content = soup.find('div', {'class': 'mw-parser-output'})
    links = content.findAll('a', href=True, title=True)
    for i, el in enumerate(links):
        try:
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
            if 'File:' in str(el.get('href')).strip():
                del links[i]
            if str(el.get('title')).strip().endswith('(disambiguation)'):
                del links[i]
            if str(el.get('title')).strip().startswith('Edit section'):
                del links[i]
            if str(el.get('title')).strip().startswith('Portal:'):
                del links[i]
            if str(el.get('title')).strip().startswith('Template:'):
                del links[i]
            if str(el.get('title')).strip().startswith('Enlarge'):
                del links[i]
            if str(el.get('title')).strip().startswith('List of'):
                del links[i]
            if 'mw-redirect' in str(el.get('class')).strip():
                del links[i]
        except:
            continue

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
        if href.startswith('https://en.wikipedia.org/wiki/List_of'):
            continue
        if title.endswith('(disambiguation)'):
            continue
        if 'File:' in href:
            continue
        if title.startswith('Edit section'):
            continue
        if title.startswith('List of'):
            continue
        if title.startswith('Portal:'):
            continue
        if title.startswith('Template:'):
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
    exists_root = G.find_one("Page", "name", header)
    if exists_root:
        root_node = exists_root
    else:
        root_node = Node("Page", name=header, url=url)
    sorted_values = sorted(value_dict, key=lambda x:value_dict[x], reverse=True)
    if max_nodes == -1:
        max_nodes = math.inf
    for i, el in enumerate(sorted_values):
        if i < max_nodes and value_dict[el] >= l:
            exists_child = G.find_one("Page", "name", el[0])
            if exists_child:
                child_node = exists_child
            else:
                child_node = Node("Page", name=el[0], url=el[1])
            connection = Relationship(root_node, "CONNECTS_TO", child_node, weight=value_dict[el])
            if G.exists(connection):
                continue
            try:
                G.create(connection)
            except Exception as e:
                raise Exception(str(connection) + " " + str(e))




G = Graph(password=password)
G.run('CREATE CONSTRAINT ON (p:Page) ASSERT p.url IS UNIQUE')
G.run('CREATE CONSTRAINT ON (p:Page) ASSERT p.name IS UNIQUE')

main_url = 'https://en.wikipedia.org'

count = 0
total = 5348758

with open('links.txt') as f:
    for line in f:
        url = line.strip()
        count += 1
        percentage = 100 * count / total
        progress = open('progress.log', 'a')
        failure = open('failure.log', 'a')
        failed_links = open('failed_links.txt', 'a')
        visited_links = open('visited_links.txt', 'a')
        try:
            generate_graph(G, url, l=1, max_nodes=-1)
            print("Run number - {}, Percentage - {}%, Page - {}\n".format(count, percentage, url), file=progress)
            print(url, file=visited_links)
        except Exception as e:
            print("Run number - {}, Percentage - {}%, Page - {}\n".format(count, percentage, url), file=failure)
            print(url, file=failed_links)
            print("ERROR - ", e)
        progress.close()
        failure.close()
        failed_links.close()
