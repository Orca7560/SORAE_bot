import json
import os
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import requests


RSS_URL = "https://sorae.info/feed"
SEEN_FILE = Path("data/sorae_seen.json")
MAX_NEWS = 10


def load_seen() -> set[str]:
    if not SEEN_FILE.exists():
        return set()
    return set(json.loads(SEEN_FILE.read_text(encoding="utf-8")))


def save_seen(seen: set[str]) -> None:
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_news() -> list[dict[str, str]]:
    response = requests.get(RSS_URL, timeout=30, headers={"User-Agent": "sorae-discord-digest/1.0"})
    response.raise_for_status()
    root = ET.fromstring(response.content)
    items = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        categories = [c.text.strip() for c in item.findall("category") if c.text]
        if title and link:
            items.append({
                "id": link,
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "category": " / ".join(categories[:2]),
            })
    return items


def post_discord(message: str) -> None:
    response = requests.post(
        os.environ["DISCORD_WEBHOOK_URL"],
        json={"content": message},
        timeout=30,
    )
    response.raise_for_status()


def format_message(news: dict[str, str]) -> str:
    category = f"[{news['category']}] " if news["category"] else ""
    return f"🛰️ **sorae 新着ニュース**\n\n{category}{news['title']}\n公開日時: {news['pub_date']}\n🔗 {news['link']}"


def main() -> int:
    seen = load_seen()
    new_items = [item for item in fetch_news() if item["id"] not in seen]

    for item in new_items[:MAX_NEWS]:
        post_discord(format_message(item))
        seen.add(item["id"])

    save_seen(seen)
    print(f"soraeニュースを{min(len(new_items), MAX_NEWS)}件投稿しました。")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        raise
