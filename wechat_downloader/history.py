from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Optional

from .downloader import WechatArticleDownloader


class WechatHistoryDownloader:
    """从链接清单中批量下载微信公众号文章。"""

    def __init__(self, cookie: Optional[str] = None, timeout: int = 20):
        self.downloader = WechatArticleDownloader(cookie=cookie, timeout=timeout)

    def download_urls(self, urls: Iterable[str], output_dir: str = "output", fmt: str = "markdown") -> list[str]:
        saved = []
        for url in urls:
            item = self.downloader.download(url.strip(), output_dir=output_dir, fmt=fmt)
            saved.append(item.saved_path or "")
        return saved

    def download_csv(self, csv_path: str, output_dir: str = "output", fmt: str = "markdown") -> list[str]:
        file_path = Path(csv_path)
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        rows = []
        with file_path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                raise ValueError("CSV file is empty or missing header row.")
            for row in reader:
                if "url" in row and row["url"]:
                    rows.append(row["url"].strip())
                elif "link" in row and row["link"]:
                    rows.append(row["link"].strip())

        if not rows:
            raise ValueError("CSV file does not contain any URL field like 'url' or 'link'.")

        return self.download_urls(rows, output_dir=output_dir, fmt=fmt)
