import requests
from bs4 import BeautifulSoup
import networkx as nx
from networkx.readwrite import json_graph
import math
import json
from collections import defaultdict

main_url = 'https://en.wikipedia.org'
url = 'https://en.wikipedia.org/wiki/Flash_(Barry_Allen)'

def generate_graph(url, graph, l=1, max_nodes=50):
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
        if 'File:' str(el.get('href')).strip()
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
    if header not in graph.nodes():
        graph.add_node(header, url=url)
    sorted_values = sorted(value_dict, key=lambda x:value_dict[x], reverse=True)
    if max_nodes == -1:
        max_nodes = math.inf
    for i, el in enumerate(sorted_values):
        if i < max_nodes and value_dict[el] >= l and (header, el[0]) not in graph.edges():
            graph.add_edge(header, el[0], weight=value_dict[el])
            graph.node[el[0]]['url'] = el[1]
    return graph
    

'''def print_sorted(value_dict, l=1):
    sorted_values = sorted(value_dict, key=lambda x:value_dict[x])
    for k in sorted_values:
        if value_dict[k] >= l:
            print("{}: {}".format(k, value_dict[k]))

#value_dict = generate_graph(url)
#print_sorted(value_dict, l=1)
print(generate_graph(url, {}))'''

'''G = nx.MultiDiGraph()
G = generate_graph(url, G)
print(len(G.nodes()))
print(G.nodes())
for i, el in enumerate(G.nodes(data=True)):
    if i != 0:
        G = generate_graph(el[1]['url'], G)
        print(len(G.nodes()))
        print(G.nodes())'''

def recursive_graph(url, depth=2, l=1, max_nodes=50):
    G = nx.MultiDiGraph()
    G = generate_graph(url, G, l=l, max_nodes=max_nodes)
    print(0, 0, len(G.nodes()))
    #print(G.nodes())
    count = 1
    while count <= depth:
        for i, el in enumerate(G.nodes(data=True)):
            try:
                G = generate_graph(el[1]['url'], G, l=l, max_nodes=max_nodes)
            except:
                continue
            print(count-1, i,len(G.nodes()))
            #print(G.nodes())
        count += 1
    return G

G = recursive_graph(url, max_nodes=-1)
with open('output.json', 'w') as out:
    out.write(json.dumps(json_graph.node_link_data(G)))