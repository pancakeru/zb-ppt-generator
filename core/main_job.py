from scrapers.duckduckscrape import get_card_updates
from core.pptgenerator import make_ppt
from core.util import emit, set_progress_logger

# ======= YouTube ========
from scrapers.youtube_scraper import yt_main

#====== Bilibili =======
from scrapers.bilibiliscraper import bili_scraper

def run_full_job(log) -> bytes:
    set_progress_logger(log)

    emit("Gathering data... / 正在抓取数据...", 5)
    #print("Gathering data...")
    updates = get_card_updates(log) 

    emit("Gathering Youtube videos... / 抓取YouTube视频...", 50)
    yt_data, yt_keywords = yt_main()
    emit("Gathering BiliBili videos... / 抓取B站视频...", 60)
    bb_data, bb_keywords = bili_scraper()
 
    #print(f"✅ Retrieved {len(updates)} entries.")
    emit("Building PPT... / 生成PPT...", 70)
    #make_ppt([], [], [], [], [])
    #make_ppt(updates, yt_data, yt_keywords, bb_data, bb_keywords)

    return make_ppt(updates, yt_data, yt_keywords, bb_data, bb_keywords)

