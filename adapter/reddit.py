from urllib.request import urlparse
from bs4 import BeautifulSoup
from json import loads
from urllib3 import PoolManager


def getImgUrl(url, http: PoolManager):
    parsed = urlparse(url)
    response = http.request('get', parsed.scheme + "://" +
                       parsed.hostname + parsed.path[:-1] + ".json", preload_content=True)
    json = loads(response.data.decode('utf-8'))
    try:
        imgUrl = json[0]["data"]["children"][0]["data"]["url"]
        return imgUrl
    except KeyError as e:
        print("Error scrapping ", url)
        raise Exception("Error extracting image url")


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/jxl,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'DNT': '1', 'Host': 'i.redd.it',
           'If-None-Match': '"0090c94b8112e2cd61ad222af05331ea"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-User': '?1', 'TE': 'trailers', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0 Waterfox/91.5.0'}

if __name__ == "__main__":
    http = PoolManager()
    print(getImgUrl(
        "https://www.reddit.com/r/PaintedFaces/comments/slsw8b/mistaken_identity_by_ken_wong/", http))
