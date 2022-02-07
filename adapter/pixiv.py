from bs4 import BeautifulSoup
from json import loads
from urllib3 import PoolManager


def getImgUrl(url, http: PoolManager):
    response = http.request('get', url, headers={'User-Agent': 'Mozilla/5.0'}, preload_content=True)
    soup = BeautifulSoup(response.data.decode('utf-8'), features="html.parser")
    try:
        data = soup.find(id="meta-preload-data")["content"]
        json = loads(data)
        imgUrl = list(json["illust"].values())[0]["urls"]["original"]
        return imgUrl
    except KeyError as e:
        print("Error scrapping ", url)
        raise Exception("Error extracting image url")
   
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/jxl,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'DNT': '1', 'Host': 'i.pximg.net',
           'Referer': 'https://www.pixiv.net/', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-User': '?1', 'TE': 'trailers', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0 Waterfox/91.5.0'}

if __name__ == "__main__":
    http = PoolManager()
    print(getImgUrl(
        "https://www.pixiv.net/en/artworks/93392275", http))