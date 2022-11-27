import requests
from lxml import etree
from io import StringIO
from bottle import get, run

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'})

def magic_text(tree, magic):
    return ["".join(x.itertext()) for x in tree.xpath(magic)]

def magic_href(tree, magic):
    return [x.get('href') for x in tree.xpath(magic)]

def parse_html(html):
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser=parser)
    results = []
    names = magic_text(tree, "//div[@class='torrent_name']")
    files = magic_text(tree, "//span[@class='torrent_files']")
    sizes = magic_text(tree, "//span[@class='torrent_size']")
    magnets = magic_href(tree, "//a[@title='Download via magnet-link']")
    for n, f, s, m in zip(names, files, sizes, magnets):
        results.append({
            'name': n,
            'files': int(f),
            'sizes': s,
            'magnet': m
        })

    return results

@get('/search/<query>')
def search(query):
    result = s.get(f"https://btdig.com/search?order=0&q={query}")
    return {'results': parse_html(result.text)}

if __name__ == "__main__":
    run(host='0.0.0.0', port=10101, server="gunicorn", workers=8)
