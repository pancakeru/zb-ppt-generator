from scrapers.duckduckscrape import test_site_access
from core.pptgenerator import make_ppt
from core.util import emit, set_progress_logger

# ====== Pokemon =======
from scrapers.duckduckscrape import test_site_access

# ======= One Piece ========
from scrapers.optcg2 import Scrape_Products
from scrapers.optcg2 import Scrape_Activities

# ======= Gundam =========
from scrapers.gdscraper import news_scraper

# ======= YouTube ========
from scrapers.youtube_scraper import yt_main

#====== Bilibili =======
from scrapers.bilibiliscraper import bili_scraper

def run_full_job(log) -> bytes:
    set_progress_logger(log)
    combined = []

    emit("Gathering data... / 正在抓取数据...", 5)
    #print("Gathering data...")
    
    combined = []

    emit("Pokemon... / 宝可梦...", 10)
    poke = test_site_access("https://www.pokemon.cn/")

    emit("One Piece Products... / 航海王商品...", 20)
    opp = Scrape_Products()

    emit("One Piece Activities... / 航海王活动...", 30)
    opa = Scrape_Activities()

    emit("Gundam... / 高达...", 40)
    gd = news_scraper()

    combined.extend(poke)
    combined.extend(opp)
    combined.extend(opa)
    combined.extend(gd)

    emit("Gathering Youtube videos... / 抓取YouTube视频...", 50)
    yt_data, yt_keywords = yt_main()
    emit("Gathering BiliBili videos... / 抓取B站视频...", 60)
    bb_data, bb_keywords = bili_scraper()
 
    #print(f"✅ Retrieved {len(updates)} entries.")
    emit("Building PPT... / 生成PPT...", 70)
    #make_ppt([], [], [], [], [])
    #make_ppt(combined, yt_data, yt_keywords, bb_data, bb_keywords)

    return make_ppt(combined, yt_data, yt_keywords, bb_data, bb_keywords, log)
