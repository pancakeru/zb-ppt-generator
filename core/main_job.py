from scrapers.duckduckscrape import get_card_updates
from core.pptgenerator import make_ppt

# ======= YouTube ========
from scrapers.youtube_scraper import yt_main

#====== Bilibili =======
from scrapers.bilibiliscraper import bili_scraper

def run_full_job():
    print("🧹 Scraping data from Pokemon site...")
    updates = get_card_updates() 

    print("Scraping YouTube for Riftbound Trends...")
    yt_data, yt_keywords = yt_main()
    print("Scraping BiliBili for Riftbound...")
    bb_data, bb_keywords = bili_scraper()
 
    #print(f"✅ Retrieved {len(updates)} entries.")
    print("📄 Generating PowerPoint report...")
    #make_ppt([], [], [], [], [])
    #make_ppt(updates, yt_data, yt_keywords, bb_data, bb_keywords)

    return make_ppt(updates, yt_data, yt_keywords, bb_data, bb_keywords)

