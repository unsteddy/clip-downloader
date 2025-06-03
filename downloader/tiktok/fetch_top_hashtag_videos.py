# downloader/tiktok/fetch_top_hashtag_videos.py

import asyncio
from downloader.tiktok.tiktok_scraper import scrape_tiktok_hashtag
# from db.clip_dao import save_tiktok_clips  # Uncomment if using DB

def main():
    hashtag = "funny"
    max_results = 20

    print(f"\nFetching top {max_results} videos for hashtag #{hashtag}...")
    results = asyncio.run(scrape_tiktok_hashtag(hashtag, max_results))

    top_results = results[:10]  # Placeholder: replace with engagement sort if needed

    print("\nTop 10 videos:")
    for i, item in enumerate(top_results):
        print(f"{i+1}. {item['title']} | {item['url']}")

    # Optional: Save to DB
    # save_tiktok_clips(top_results)

if __name__ == "__main__":
    main()
