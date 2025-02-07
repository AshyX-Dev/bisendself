import googlesearch
import httpx
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent

def get_mp3_links_with_title(url):
    response = httpx.get(url, headers={
        "User-Agent": FakeUserAgent().random
    })
    if response.status_code != 200:
        print(f"Error: Unable to access {url}")
        return {}
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'
    links = soup.find_all('a')
    mp3_links = [link.get('href') for link in links if link.get('href') and link.get('href').endswith('.mp3')]
    if not mp3_links==[]:
        try:
            return {
        'name': title,
        'url': mp3_links[0]}
        except:...

music = "سوپرهیرو از مترو بومین"

result = [get_mp3_links_with_title(m) for m in googlesearch.search(music,num_results=5)]

print(result)