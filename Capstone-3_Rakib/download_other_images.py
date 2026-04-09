from icrawler.builtin import GoogleImageCrawler

keywords = [
    "empty store CCTV",
    "empty street CCTV camera",
    "warehouse empty CCTV",
    "dog security camera footage",
    "cat security camera footage",
    "empty parking lot CCTV",
    "empty office CCTV",
    "empty hallway CCTV camera",
]

for word in keywords:

    crawler = GoogleImageCrawler(storage={"root_dir": "dataset/train/other"})

    crawler.crawl(keyword=word, max_num=200, min_size=(200, 200))

print("Other class images downloaded.")
