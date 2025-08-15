from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import Optional, Callable

def news_scraper():
    #log = log or (lambda *_: None)
    #log("Scraping Gundam... / 抓取高达...")
    print("Scraping Gundam...")
    results = []

    now = datetime.now()
    year = now.year
    month = now.month

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.gundam-gcg.com/zh-tw/news/")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    items = soup.select('div[class*="newsDetail"]')

    #print(f"Items found: {len(items)}")

    for item in items:
        title_tag = item.find("dd", class_="cardLead")
        title_text = title_tag.get_text()
        type_tag = item.get("data-tags")
        date_tag = item.find("dt", class_="cardDate")
        date_text = date_tag.get_text(strip=True)
    
        info_text = None

        if len(date_text) >= 7:
            item_year = int(date_text[:4])
            item_month = int(date_text[5:7])
            if item_year < year or (item_year == year and item_month < month):
                continue
        else:
            print("Invalid date_text")
            continue

        link = item.find("a").get("href")
        img_tag = item.find("img")
        img_src = img_tag["src"] if img_tag else "No image"
        img_link = f"https://www.gundam-gcg.com{img_src}"

        entry = {
            "date": date_text,
            "name": f"高达 {title_text}",
            "flavor": '',
            "type": type_tag,
            "link": link,
            "image": img_link,
            "info": info_text
        }
        results.append(entry)
    #print(results)

    for entry in results:
        driver.get(entry["link"])
        time.sleep(1) 
        info_text = ""

        try:
            divs = driver.find_elements(By.CLASS_NAME, "detailColStatus")
            for div in divs:
                dt_tags = div.find_elements(By.TAG_NAME, "dt")
                dd_tags = div.find_elements(By.TAG_NAME, "dd")

                for dt, dd in zip(dt_tags, dd_tags):
                    if "is-hide" in dt.get_attribute("class"):
                        continue

                    dt_text = dt.text.strip()
                    dd_text = dd.text.strip()
                    info_text += f"{dt_text}: {dd_text}\n"
                break  
        except Exception as e:
            print(f"⚠️ Error extracting info from link {entry['link']}: {e}")
            info_text = "Failed to extract info"

        entry["info"] = info_text

    driver.quit()
    #print(results)
    log(f"Gundam: {len(results)} new entries / 高达：{len(results)}新文件")
    return results

#news_scraper()