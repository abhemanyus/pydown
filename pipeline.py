import pathlib
import adapter.reddit
import adapter.pixiv
import adapter.danbooru
from classify import classify
from download import download
from hashimg import hashimg
from urllib.parse import ParseResult, urlparse
from urllib3 import PoolManager
import re
from enum import Enum
import inspect

SITEMAP = {
    "reddit": adapter.reddit,
    "pixiv": adapter.pixiv,
    "donmai": adapter.danbooru
}

def getExt(imgPath: str):
    regex = re.compile(r"\.(jpe?g|png|webp)$", flags=re.IGNORECASE)
    match = regex.search(imgPath)
    if match:
        return match.group()


class Image():
    path: pathlib.Path = None
    url: ParseResult = None
    imgURL: ParseResult = None
    data: bytes = None
    ext: str = None
    category: str = None
    precision: float = None
    root: pathlib.Path = None
    site: str = None
    hash: str = None
    tmpPath: pathlib.Path = None
    adapter = None
    http: PoolManager

    def __init__(self, root="test", precision=0.3):
        self.root = pathlib.Path(root)
        self.precision = precision
        self.http = PoolManager()

    def reset(self):
        path: pathlib.Path = None
        url: ParseResult = None
        imgURL: ParseResult = None
        data: bytes = None
        ext: str = None
        category: str = None
        site: str = None
        hash: str = None
        tmpPath: pathlib.Path = None
        adapter = None

    def start(self, url: str):
        self.reset()
        self.url = urlparse(url)
        self.getImgSite()
        self.getImgUrl()
        self.getImgExt()
        self.getImgData()
        self.getTmpPath()
        self.getImgHash()
        self.getImgCat()
        self.getImgPath()
        print(self)

    def getImgSite(self):
        self.site = self.url.hostname.split('.')[-2]
        print(self)

    def getImgUrl(self):
        self.adapter = SITEMAP.get(self.site, None)
        self.ext = getExt(self.url.path)

        if self.ext:
            self.imgURL = self.url
        else:
            if self.adapter:
                self.imgURL = urlparse(
                    self.adapter.getImgUrl(self.url.geturl(), self.http))
            else:
                raise Exception("URL is not supported")
        print(self)

    def getImgExt(self):
        if not self.ext:
            self.ext = getExt(self.imgURL.path)
        if not self.ext:
            raise Exception("Image format is not supported")
        print(self)

    def getImgData(self):
        headers = self.adapter.headers if self.adapter else {}
        self.data = download(self.imgURL.geturl(), headers=headers, http=self.http)
        print(self)

    def getImgHash(self):
        self.hash = hashimg(self.tmpPath)
        print(self)

    def getTmpPath(self):
        binhash = str(hash(self.data))
        self.tmpPath = self.root / "temp" / (binhash + self.ext)
        self.tmpPath.write_bytes(self.data)
        print(self)

    def getImgCat(self):
        self.category = classify(str(self.tmpPath), precision=self.precision)
        print(self)

    def getImgPath(self):
        self.path = self.root / self.category / (self.hash + self.ext)

        if self.path.exists():
            if self.path.stat().st_size < self.tmpPath.stat().st_size:
                self.tmpPath.replace(self.path)
            else:
                self.tmpPath.unlink()
        else:
            self.tmpPath.replace(self.path)

        print(self)

    def __repr__(self):
        return f"""Step: {inspect.stack()[1].function}
        url: {self.url.geturl() if self.url else None}
        site: {self.site}
        adapter: {self.adapter}
        imgURL: {self.imgURL.geturl() if self.imgURL else None}
        ext: {self.ext}
        data: {len(self.data) if self.data else 0}
        path: {self.path}
        tmpPath: {self.tmpPath}
        category: {self.category}
        hash: {self.hash}
        """


if __name__ == "__main__":
    process = Image()
    image = process.start("https://danbooru.donmai.us/posts/5108729")
    image = process.start("https://www.reddit.com/r/PaintedFaces/comments/slsw8b/mistaken_identity_by_ken_wong/")
