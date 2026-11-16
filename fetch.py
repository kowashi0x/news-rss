import urllib.request
import xml.etree.ElementTree as ET
import re
import json

rss_url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
xml_data = urllib.request.urlopen(req, timeout=10).read()
root = ET.fromstring(xml_data)

articles = []
for item in root.findall(".//item")[:8]:
    title = item.findtext("title", "")
    link = item.findtext("link", "")
    pub_date = item.findtext("pubDate", "")
    image_url = ""

    try:
        art_req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(art_req, timeout=10).read().decode("utf-8", errors="ignore")
        m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html)
        if m:
            image_url = m.group(1)
    except Exception:
        pass

    articles.append({
        "title": title,
        "link": link,
        "pubDate": pub_date,
        "image": image_url
    })

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
