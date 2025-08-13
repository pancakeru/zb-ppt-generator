from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import time

def Scrape_Products():
    print("Scraping One Piece Products...")
    results = []
# --- Setup ---
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://onepiece-cardgame.cn/products")
    time.sleep(5)

    # --- Parse page ---
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ul = soup.find("ul", class_="productsInfo xl-w")
    items = ul.find_all("li")

    # --- Setup type mapping ---
    type_map = {
        "卡组": "1",   
        "补充包": "2",   
        "其他": "3"     
    }

    # --- Get current date ---
    now = datetime.now()
    year = now.year
    month = now.month

    # --- Loop and extract --- on the products page
    starting_id = len(items)
    print(f"✅ Total products found: {starting_id}\n")

    for i, item in enumerate(items):
        title_tag = item.find("div", class_="proName")
        type_tag = item.find("div", class_="protit")
        time_tag = item.find("div", class_="time")
        spans = time_tag.find_all("span") if time_tag else []
        date_text = spans[1].get_text(strip=True) if len(spans) > 1 else ""
        info_text = None

        try:
            item_year = int(date_text[:4])
            item_month = int(date_text[5:7])
            if item_year < year or (item_year == year and item_month < month):
                continue
        except:
            continue

        title = title_tag.get_text(strip=True) if title_tag else "No title"
        ptype = type_tag.get_text(strip=True) if type_tag else "No type"
        type_num = type_map.get(ptype, "3")  # fallback to "其他"

        item_id = starting_id - i + 17
        link = f"https://onepiece-cardgame.cn/products/detail?id={item_id}&type={type_num}"

        # Optional: get image src
        img_tag = item.find("img")
        img_src = img_tag["src"] if img_tag else "No image"

        entry = {
            "date": date_text,
            "name": title,
            "flavor": '',
            "type": ptype,
            "link": link,
            "image": img_src,
            "info": info_text
        }
        print(type(entry))
        results.append(entry)

    for entry in results:
        driver.get(entry["link"])
        time.sleep(1)  # small delay if needed

        # Find the correct div with 商品内容
        divs = driver.find_elements(By.CLASS_NAME, "prodstatusBox")
        info_text = ""

        for div in divs:
            if "商品内容" in div.text:
                paragraphs = div.find_elements(By.TAG_NAME, "p")
                info_text = "\n".join(p.text for p in paragraphs)
                break
        entry["info"] = info_text

    driver.quit()
    #print(results)
    return results

def Scrape_Activities():
    print("Scraping One Piece Activities...")
    results = []
# --- Setup ---
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://onepiece-cardgame.cn/activity")
    time.sleep(5)

    # --- Parse page ---
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ul = soup.find("ul", class_="activityInfo xl-w")
    items = ul.find_all("li")

    # --- Get current date ---
    now = datetime.now()
    year = now.year
    month = now.month

    # --- Loop and extract --- on the products page
    starting_id = len(items)
    print(f"✅ Total products found: {starting_id}\n")

    for i, item in enumerate(items):
        title_tag = item.find("div", class_="actName")
        time_tag = item.find("div", class_="time")
        spans = time_tag.find_all("span") if time_tag else []
        date_text = spans[1].get_text(strip=True) if len(spans) > 1 else ""
        info_text = None

        try:
            item_year = int(date_text[:4])
            item_month = int(date_text[5:7])
            if item_year < year or (item_year == year and item_month < month):
                continue
        except:
            continue

        title = title_tag.get_text(strip=True) if title_tag else "No title"
        ptype = "活动"
        type_num = 3

        item_id = starting_id - i + 9
        link = f"https://onepiece-cardgame.cn/activity/detail?id={item_id}&type={type_num}"

        # Optional: get image src
        img_tag = item.find("img")
        img_src = img_tag["src"] if img_tag else "No image"

        entry = {
            "date": date_text,
            "name": title,
            "flavor": '',
            "type": ptype,
            "link": link,
            "image": img_src,
            "info": info_text
        }
        print(type(entry))
        results.append(entry)

    for entry in results:
        driver.get(entry["link"])
        time.sleep(1)  # small delay if needed

        # Find the correct div with 商品内容
        divs = driver.find_elements(By.CLASS_NAME, "BodyTitle")
        info_text = ""

        for div in divs:
            paragraphs = div.find_elements(By.TAG_NAME, "h3")
            info_text = "\n".join(p.text for p in paragraphs)
            break
        entry["info"] = info_text

    driver.quit()
    #print(results)
    return results

#Scrape_Activities()
#Scrape_Products()