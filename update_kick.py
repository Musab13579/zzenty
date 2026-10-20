#!/usr/bin/env python3
"""Best-effort public VOD metadata fetcher for a Kick channel.
This uses a public website endpoint, not a guaranteed/stable official VOD API.
It does not download video files and does not expose secrets.
"""
import json, os, sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

CHANNEL = os.environ.get("KICK_CHANNEL", "r7-zenty")
OUT = "vods.json"
ENDPOINTS = [
    f"https://kick.com/api/v2/channels/{CHANNEL}/videos",
    f"https://kick.com/api/v2/channels/{CHANNEL}/videos/latest",
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ZentyyVODIndexer/1.0)",
    "Accept": "application/json",
    "Referer": f"https://kick.com/{CHANNEL}",
}

def first(d, *keys):
    for key in keys:
        val = d.get(key)
        if val is not None:
            return val
    return None

def normalize(item):
    if not isinstance(item, dict):
        return None
    vid = first(item, "uuid", "id", "video_id", "slug")
    title = first(item, "session_title", "title", "name") or "Başlıksız yayın"
    created = first(item, "created_at", "published_at", "start_time", "updated_at")
    duration = first(item, "duration", "duration_seconds", "length")
    views = first(item, "views", "view_count", "views_count")
    thumb = first(item, "thumbnail", "thumbnail_url", "preview")
    if isinstance(thumb, dict):
        thumb = first(thumb, "url", "src")
    category = first(item, "category", "category_name")
    if isinstance(category, dict):
        category = first(category, "name", "slug")
    # Keep the known Kick VOD page URL as metadata only. Kick does not document
    # a stable public VOD iframe URL; do not invent one.
    vod_url = f"https://kick.com/{CHANNEL}/videos/{vid}" if vid else None
    {
        "id": str(vid) if vid is not None else None,
        "title": str(title),
        "created_at": created,
        "duration": int(duration) if str(duration or "").isdigit() else None,
        "views": int(views) if str(views or "").isdigit() else None,
        "thumbnail": thumb if isinstance(thumb, str) and thumb.startswith("https://") else None,
        "category": str(category) if category else None,
        "url": vod_url,
        "embed_url": None
    }

def extract_list(payload):
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    # common response shapes used by Kick's web API
    for key in ("videos", "data", "items", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            for sub in ("videos", "data", "items", "results"):
                if isinstance(value.get(sub), list):
                    return value[sub]
    return []

def fetch():
    errors = []
    for url in ENDPOINTS:
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=25) as response:
                payload = json.loads(response.read().decode("utf-8"))
            items = extract_list(payload)
            if items:
                normalized = [v for v in (normalize(x) for x in items) if v]
                # De-duplicate by id and preserve newest first where dates are comparable.
                seen, unique = set(), []
                for item in normalized:
                    key = item["id"] or (item["title"], item["created_at"])
                    if key not in seen:
                        seen.add(key); unique.append(item)
                return unique, None
            errors.append(f"{url}: yanıt içinde video listesi bulunamadı")
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            errors.append(f"{url}: {exc}")
    return None, "; ".join(errors)

def main():
    vods, error = fetch()
    if vods is None:
        # Keep last known-good data if Kick changes or blocks the endpoint.
        if os.path.exists(OUT):
            print("Kick VOD listesi alınamadı; mevcut vods.json korunuyor. " + str(error), file=sys.stderr)
            return 0
        vods = []
    data = {
        "channel": CHANNEL,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Kick public website endpoint; availability/schema may change",
        "notice": "Only fields returned by the source are included. VOD embedding and full private analytics are not guaranteed.",
        "vods": vods
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(vods)} VOD metadata records written.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
