from imagehash import phash
from PIL import Image

def hashimg(filepath:str=None):
    img = Image.open(filepath)
    return str(phash(img))

if __name__ == "__main__":
    print(hashimg('test/one.jpg'))
    print(hashimg('test/onecrop.jpg'))
    print(hashimg('test/one1000.jpg'))
    print(hashimg('test/one.webp'))
    print(hashimg('test/two.jpeg'))