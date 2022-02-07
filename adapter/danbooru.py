from bs4 import BeautifulSoup
from urllib3 import PoolManager


def getImgUrl(url, http: PoolManager):
    response = http.request('get', url, preload_content=True)
    soup = BeautifulSoup(response.data.decode('utf-8'), features="html.parser")
    try:
        imgUrl = soup.find_all("a", class_="image-view-original-link")[0]["href"]
        return imgUrl
    except KeyError as e:
        print("Error scrapping ", url)
        raise Exception("Error extracting image url")


headers = {'Accept': 'image/avif,image/jxl,image/webp,*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5', 'Alt-Used': 'cdn.donmai.us', 'Connection': 'keep-alive', 'Cookie': '_danbooru2_session=SSQjguKF2LZZcBUQT9qZOV%2FYdVPEgEvv4Ow1cvgSBQ9JKvwMQ82qgBpIiPapF5ndfgrR3rRtgdHMzdNfJM8Ahuhp2Ei9Cqr72F%2FLBvhrgjWFEGMtVy1jnsMMLSohSIFu4yzqlDsTGI8m7hqikWEJL%2BYzflwI1I0kGIX%2BaerWYqfcB0gtFbB8KLIRUvkEHth8qJExjJglDkqcJupo2sIPObrKqwjIrsgIS0gh4OD1dH3Xie1TAe5RbQuHgnrTX9ue7aSMuXg1uK771JlQHr%2FuZieAQSYGZisoDyPkmlX2DJOm4OGvp8Or3rfA3z759wm87VVRXPWuLU23DoRNYFpQjglUjf0G6IjJhRpZvjeLsD0qXU3UZ1UJkIP1XfwPYjxL%2FbDKnA%3D%3D--911hxeFsOlNhTsvH--ZTIVQn1g1ntgbRrK2ab8fw%3D%3D',
           'DNT': '1', 'Host': 'cdn.donmai.us', 'Referer': 'https://danbooru.donmai.us/', 'Sec-Fetch-Dest': 'image', 'Sec-Fetch-Mode': 'no-cors', 'Sec-Fetch-Site': 'same-site', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0 Waterfox/91.5.0'}


if __name__ == "__main__":
    http = PoolManager()
    print(getImgUrl(
        "https://danbooru.donmai.us/posts/5108729", http))
