#!/usr/bin/env python3
"""Search Unsplash images and return Markdown with attribution.

Usage:
    python image_search.py --object "<english keyword>" --number 1

Requires UNSPLASH_ACCESS_KEY, loaded from a `.env` file at the skill root
(`.claude/skills/project-blog/.env`), which is git-ignored. See `.env.example`.
"""
import argparse
import os
import warnings
from pathlib import Path
from urllib.parse import quote

import requests

warnings.filterwarnings("ignore")

# .env lives at the skill root, one level above this `tools/` directory.
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def load_env(path: Path) -> None:
    """Load KEY=VALUE lines from a .env file into os.environ (does not overwrite)."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def image_search(query: str, count: int = 1) -> str:
    clean_query = quote(" ".join(query.split()[:5]))
    access_key = os.getenv("UNSPLASH_ACCESS_KEY", "").strip()
    if not access_key:
        return (
            "错误：未设置 UNSPLASH_ACCESS_KEY。\n"
            "请复制 .env.example 为 .env，并填入你的 Unsplash Access Key。"
        )

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": clean_query,
        "per_page": count,
        "client_id": access_key,
    }

    try:
        res = requests.get(url, params=params, timeout=15)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        return f"Error: {e}"

    results = data.get("results", [])
    if not results:
        return f"No images found for query: {clean_query}"

    output = []
    for item in results[:count]:
        raw = item["urls"]["raw"]
        sep = "&" if "?" in raw else "?"
        img_url = raw + sep + "w=600&h=400&fit=crop&q=80"
        author = item["user"]["name"]
        profile = item["user"]["links"]["html"]
        output.append(
            f"![{clean_query}]({img_url})\n"
            f"*Photo by [{author}]({profile}) on [Unsplash](https://unsplash.com)*"
        )
    return "\n\n".join(output)


if __name__ == "__main__":
    load_env(ENV_FILE)
    parser = argparse.ArgumentParser(description="Search Unsplash images")
    parser.add_argument("--object", required=True)
    parser.add_argument("--number", type=int, default=1)
    args = parser.parse_args()
    print(image_search(args.object, args.number))
