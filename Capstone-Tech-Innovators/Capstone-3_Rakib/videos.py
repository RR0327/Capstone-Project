"""import yt_dlp

urls = [
    "https://www.youtube.com/results?search_query=shop+robbery+CCTV",
]

ydl_opts = {
    "outtmpl": "videos/%(title)s.%(ext)s",
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(urls)
"""

# updated version
"""
import yt_dlp

search_queries = [
    "shop robbery CCTV",
    "shoplifting CCTV footage",
    "store burglary CCTV",
    "night shop intrusion CCTV",
    "suspicious activity CCTV camera",
]

ydl_opts = {
    "outtmpl": "videos/%(title)s.%(ext)s",
    "format": "mp4",
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for query in search_queries:
        ydl.download([f"ytsearch10:{query}"])
"""

# More updated version with error handling

import yt_dlp

search_queries = [
    "shop robbery CCTV",
    "shoplifting CCTV footage",
    "store burglary CCTV",
    "night shop intrusion CCTV",
    "suspicious activity CCTV camera",
]

ydl_opts = {
    "outtmpl": "videos/%(title)s.%(ext)s",
    "format": "mp4",
    "ignoreerrors": True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for query in search_queries:
        ydl.download([f"ytsearch20:{query}"])
