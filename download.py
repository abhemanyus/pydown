from urllib.error import URLError, HTTPError
from urllib3 import PoolManager

def download(url: str, http: PoolManager, headers: dict[str, str]={}):
    data: bytes
    try:
        response = http.request('get', url, headers=headers, preload_content=True)
        return response.data
    except ValueError as e:
        print("Invalid url", url)
    except URLError as e:
        print("Couldn't connect to", url)
    except HTTPError as e:
        print("Request rejected by", url)
    
    


if __name__ == "__main__":
    http = PoolManager()
    print(download("https://jsonplaceholder.typicode.com/todos/1", http))