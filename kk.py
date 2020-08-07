import requests, json
from bs4 import BeautifulSoup


ID=83421658
url = 'https://www.pixiv.net/en/artworks/'+ID
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
x = soup.find("meta", {"id": "meta-preload-data"}).get("content")

usefulData = json.loads(x)

print(type(usefulData))

test=usefulData["illust"]['83421658']['tags']['tags'][0]['tag']
print(len(usefulData["illust"]['83421658']['tags']['tags']))
print(test)

for i in range(len(usefulData["illust"]['83421658']['tags']['tags'])):
    print(usefulData["illust"]['83421658']['tags']['tags'][i]['tag'])


# print(usefulData)