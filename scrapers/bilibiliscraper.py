import requests
from bs4 import BeautifulSoup
import urllib.parse

def search_bilibili(keyword, pages=1):
    results = []
    base_url = "https://search.bilibili.com/all?vt=49034532&keyword=%E7%AC%A6%E6%96%87%E6%88%98%E5%9C%BA&from_source=webtop_search&spm_id_from=333.1387&search_source=5&order=pubdate"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }

    for page in range(1, pages + 1):
        params = {
            "keyword": keyword,
            "page": page,
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        #print(soup.select('div[class*="video-list-item"]'))
        for item in soup.select('div[class*="video-list-item"]'):
            title = item.find("h3")
            link_tag = item.find("a")
            views = item.select_one(".bili-video-card__stats--item:nth-child(1) span")
            author = item.find("span",class_="bili-video-card__info--date").get_text()

            #print(author)

            if title and link_tag:
                results.append({
                    "title": title.text.strip(),
                    "channel": author,
                    "views": views.text.strip(),
                    "url": "https:" + link_tag["href"],
                })
    #print(results)
    return results

from collections import Counter
import re

# Optional: A basic Chinese + English stopword list (you can expand it)
STOPWORDS = set([
    "的", "了", "是", "我", "你", "他", "她", "在", "和", "就", "都", "也",
    "符文战场"
])

def extract_keywords_from_titles(titles, top_n=10):
    all_words = []

    for title in titles:
        words = re.findall(r'\b\w+\b|[\u4e00-\u9fff]', title.lower())

        for word in words:
            if word not in STOPWORDS and len(word) > 1:
                all_words.append(word)

    counter = Counter(all_words)
    return counter.most_common(top_n)

def bili_scraper():
    videos = search_bilibili("riftbound", pages=1)
    video_titles = [v['title'] for v in videos]
    video_results = videos[:5]
    top_keywords = extract_keywords_from_titles(video_titles)

    #print(top_keywords)
    return video_results, top_keywords

#bili_scraper()
