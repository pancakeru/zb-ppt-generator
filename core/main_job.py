from scrapers.duckduckscrape import get_card_updates
from core.pptgenerator import make_ppt
from typing import Callable, Optional

# ======= YouTube ========
from scrapers.youtube_scraper import yt_main

#====== Bilibili =======
from scrapers.bilibiliscraper import bili_scraper

def run_full_job(log: Optional[Callable[[str], None]] = None):
    log = log or (lambda *_: None)

    log("Gathering data... / 正在抓取数据...", 10)
    print("Gathering data...")
    updates = get_card_updates(log=log) 

    log("Gathering Youtube videos... / 抓取YouTube视频...", 25)
    yt_data, yt_keywords = yt_main()
    log("Gathering BiliBili videos... / 抓取B站视频...", 45)
    bb_data, bb_keywords = bili_scraper()
 
    #print(f"✅ Retrieved {len(updates)} entries.")
    log("Building PPT... / 生成PPT...", 70)
    #make_ppt([], [], [], [], [])
    #make_ppt(updates, yt_data, yt_keywords, bb_data, bb_keywords)

    return make_ppt(updates, yt_data, yt_keywords, bb_data, bb_keywords)

