from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import pickle

url = 'https://www.wikiwand.com/en/The_Flash_(2014_TV_series)'
parent_url = 'https://www.wikiwand.com'

'''wd = webdriver.PhantomJS()
wd.get(url)

WebDriverWait(wd, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "read_more_link")))

html_page = wd.page_source
wd.quit()

soup = BeautifulSoup(html_page, 'html.parser')

root = soup.find(class_='firstHeading')

root_title = str(root.text).strip()

nodes = []
nodes.append(root_title)

relatives = soup.find_all('a', {'class': 'read_more_link'})
relatives = relatives[:3]

count = 1

for i, el in enumerate(relatives):
    url = parent_url + el['href']
    wd = webdriver.PhantomJS()
    wd.get(url)

    WebDriverWait(wd, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "read_more_link")))

    html_page = wd.page_source
    wd.quit()

    soup = BeautifulSoup(html_page, 'html.parser')

    head = soup.find(class_='firstHeading')

    title = str(head.text).strip()
    nodes.append(title)
    count += 1
    if count > 100:
        break'''

def get_relatives(url):
    wd = webdriver.PhantomJS()
    wd.get(url)

    WebDriverWait(wd, 600).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "read_more_link")))

    html_page = wd.page_source
    wd.quit()

    soup = BeautifulSoup(html_page, 'html.parser')

    head = soup.find(class_='firstHeading')

    title = str(head.text).strip()
    relatives = soup.find_all('a', {'class': 'read_more_link'})
    urls = relatives[:3]
    url_list = []
    title_list = []
    for i, el in enumerate(urls):
        url = parent_url + el['href']
        titl = el.find('span')
        titl = str(titl.text)
        title_list.append(titl)
        url_list.append(url)
    return title, title_list, url_list

title, title_list, url_list = get_relatives(url)

graph = {
    title: title_list
}

count = 1
urls = []
while count < 15:
    for i, el in enumerate(url_list):
        title, title_list, rel_url_list = get_relatives(el)
        graph[title] = title_list
        urls.extend(rel_url_list)
        print(graph)
        filename = 'graph.pkl'
        file = open(filename, 'wb')
        pickle.dump(graph, file)
        file.close()
    url_list = urls
    urls = []
    count += 1

filename = 'graph.pkl'
file = open(filename, 'wb')
pickle.dump(graph, file)
file.close()