from duckduckscrape import get_card_updates
from pptgenerator import make_ppt

# ======= YouTube ========
from youtube_scraper import yt_main

#====== Bilibili =======
from bilibiliscraper import bili_scraper

def main():
    print("🧹 Scraping data from Pokemon site...")
    #updates = get_card_updates() 

    print("Scraping YouTube for Riftbound Trends...")
   # yt_data, yt_keywords = yt_main()
    print("Scraping BiliBili for Riftbound...")
    #bb_data, bb_keywords = bili_scraper()

    #if not updates:
        #print("⚠️ No data found. Check the scraper or site access.")
        #return
 
    #print(f"✅ Retrieved {len(updates)} entries.")
    print("📄 Generating PowerPoint report...")
    #make_ppt(updates, yt_data, yt_keywords, bb_data, bb_keywords)
    make_ppt([], [], [], [], [])
    print("🎉 PowerPoint created successfully!")

if __name__ == "__main__":
    main()
