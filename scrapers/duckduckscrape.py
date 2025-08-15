import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional, Callable

#======= Pokemon =============
def test_site_access(url, log: Optional[Callable[[str], None]] = None):
    log = log or (lambda *_: None)

    log("Scraping Pokemon... / 抓取宝可梦...")
    print("Scraping Pokemon...")
    poke_updates = []

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

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string.strip() if soup.title else "No title found"
            #html = response.text
            print(f"Page title: {title}")
           # print(html)

            # === Step 1: Locate the card list body ===
            card_list = soup.find("ul", class_="card-list__body")
            if not card_list:
                print("⚠️ Could not find <ul class='card-list__body'>")
                return
            cards = soup.select("li.card__element")
            log(f"Pokemon: {len(cards)} new entries / 宝可梦：{len(cards)}新文件")

            for card in cards:
                link_tag = card.find("a")
                rel_url = link_tag["href"] if link_tag else None
                full_url = f"https://www.pokemon.cn{rel_url}" if rel_url else "N/A"

                text_block = card.find("p")
                category_tag = card.find("div", class_="card__header--category")
                date_block = card.find("time")
                date_str = date_block.text

                if text_block:
                    lines = list(text_block.stripped_strings)
                    name = lines[1] if len(lines) > 1 else "N/A"
                    flavor = lines[2] if len(lines) > 2 else ''

                    # Past 10 days
                    try:
                        date_obj = datetime.strptime(date_str, "%m/%d/%Y")
                        days_diff = (datetime.now() - date_obj).days
                        if days_diff > 10:
                           continue  
                    except:
                       pass

                    tag = classify_entry(name, flavor, category_tag)
                    if tag == "周边":
                        name = lines[0]

                    img_url = extract_additional_info(full_url, tag)
                    info_text = extract_info_text(full_url, tag)

                    entry = {
                        "date": date_str,
                        "name": name,
                        "flavor": flavor,
                        "type": tag,
                        "link": full_url,
                        "image": f"https://www.pokemon.cn{img_url}" if img_url else 'None found',
                        "info": info_text
                    }
                    poke_updates.append(entry)
                   # print(entry)
                   # print(f"Length: {len(poke_updates)}")
                   
                else:
                    print("⚠️ Could not find <p> tag in card.")

        else:
            print("❌ Access failed. Site returned a non-200 status code.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

    #print(type(poke_updates))
    return poke_updates

def classify_entry(name_text, flavor_text, category_tag):
    if "赛" in name_text or "赛" in flavor_text:
        return "赛事" 
    elif "商品" in name_text or "商品" in flavor_text or "套" in name_text or "套" in flavor_text or "补充包" in name_text or "补充包" in flavor_text:
        return "商品"
    elif "活动" in name_text or "参加" in name_text or "活动" in flavor_text or "参加" in flavor_text:
        return "活动"
    
    if category_tag:
        category_text = category_tag.get_text(strip=True)
        if category_text != "集换式卡牌游戏":
            return "周边"
    
    return "其他" 

# Visiting the links
def extract_additional_info(url, content_type):
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

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"❌ Failed to access {url}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        image_url = None

        if content_type in ["赛事", "活动", "商品", "其他"]:
            body_div = soup.find("div", class_="content-detail-area")
            if body_div:
                img_tag = body_div.find("img")
                if img_tag and img_tag.get("src"):
                    image_url = img_tag["src"]
        elif content_type == "周边":
            body_div = soup.find("figure", class_="article-detail__mv")
            if body_div:
                img_tag = body_div.find("img")
                if img_tag and img_tag.get("src"):
                    image_url = img_tag["src"]
        return image_url

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None
    
def extract_info_text(url, content_type):
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
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"❌ Failed to access {url}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        if content_type in ["赛事", "活动", "其他"]:
            body_div = soup.find("div", class_="t-body")
            if body_div:
                return body_div.get_text(strip=True)
        
        elif content_type in ["商品", "周边"]:
           table = soup.find("table")
           if table:
                rows = table.find_all("tr")
                info_lines = []
                for row in rows:
                    cols = row.find_all(["td", "th"])
                    line = ": ".join(col.get_text(strip=True) for col in cols)
                    info_lines.append(line)
                return "\n\n".join(info_lines)
        return None
        
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

# ======= One Piece ========
from scrapers.optcg2 import Scrape_Products
from scrapers.optcg2 import Scrape_Activities

# ======= Gundam =========
from scrapers.gdscraper import news_scraper

#======== return everything ============
def get_card_updates(log):
    all_entries = test_site_access("https://www.pokemon.cn/")+ Scrape_Products() + Scrape_Activities() + news_scraper()
    return all_entries

