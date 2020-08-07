import requests
from bs4 import BeautifulSoup as bs

headers={
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'

}

url='https://www.pixiv.net/artworks/57562855'
# url='http://coreyms.com'

# source=requests.get(url).text
# soup=bs(source,'lxml')
# print(soup.prettify())
# print(type(soup))

# match=soup.find('body')
# print(match)





req=requests.get(url,headers)
soup=bs(req.content,'html.parser')
# print(soup.prettify())
print(soup.head)


match=soup.find("meta")
# test=match.get()
print(match)