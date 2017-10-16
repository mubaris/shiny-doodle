import requests
from bs4 import BeautifulSoup
#import networkx as nx
#from networkx.readwrite import json_graph
from py2neo import Graph, Node, Relationship, NodeSelector
import math
import json
from collections import defaultdict
from secret import password

main_url = 'https://en.wikipedia.org'
url = 'https://en.wikipedia.org/wiki/Flash_(comics)'

def generate_graph(G, url, l=1, max_nodes=50):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
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
    '''if header not in graph.nodes():
        graph.add_node(header, url=url)'''
    '''selector = NodeSelector(G)
    selected = list(selector.select("Page", name=header, url=url))
    if selected:
        root_node = selected[0]
    else:
        root_node = Node("Page", name=header, url=url)'''
    selector = NodeSelector(G)
    selected = list(selector.select("Page", name=header, url=url))
    if selected:
        root_node = selected[0]
    else:
        root_node = Node("Page", name=header, url=url)
    sorted_values = sorted(value_dict, key=lambda x:value_dict[x], reverse=True)
    if max_nodes == -1:
        max_nodes = math.inf
    for i, el in enumerate(sorted_values):
        if i < max_nodes and value_dict[el] >= l:
            # and (header, el[0]) not in graph.edges()
            '''graph.add_edge(header, el[0], weight=value_dict[el])
            graph.node[el[0]]['url'] = el[1]'''
            selector = NodeSelector(G)
            selected = list(selector.select("Page", name=el[0], url=el[1]))
            if selected:
                child_node = selected[0]
            else:
                child_node = Node("Page", name=el[0], url=el[1])
            connection = Relationship(root_node, "CONNECTS_TO", child_node, weight=value_dict[el])
            print(connection)
            if G.exists(connection):
                continue
            G.create(connection)
    #return graph

def recursive_graph(G, url, depth=2, l=1, max_nodes=50):
    '''G = nx.MultiDiGraph()
    G = generate_graph(url, G, l=l, max_nodes=max_nodes)'''
    generate_graph(G, url, l=l, max_nodes=max_nodes)
    selector = NodeSelector(G)
    selected = list(selector.select("Page"))
    print(0, 0, len(selected))
    count = 1
    while count <= depth:
        selected = list(selector.select("Page"))
        #for i, el in enumerate(G.nodes(data=True)):
        for i, el in enumerate(selected):
            url = el.properties["url"]
            generate_graph(G, url, l=l, max_nodes=max_nodes)
            selected = list(selector.select("Page"))
            print(count-1, i, len(selected))
        count += 1
    return G

G = Graph(password=password)
G.run('CREATE CONSTRAINT ON (p:Page) ASSERT p.url IS UNIQUE')
recursive_graph(G, url, max_nodes=10, depth=5)