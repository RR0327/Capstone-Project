from icrawler.builtin import BingImageCrawler

keywords = [
    "CCTV suspicious activity",
    "shoplifting CCTV footage",
    "store robbery CCTV",
    "person breaking into shop CCTV",
    "night store intrusion CCTV",
]

for word in keywords:

    crawler = BingImageCrawler(storage={"root_dir": f"dataset/{word}"})

    crawler.crawl(keyword=word, max_num=100)
