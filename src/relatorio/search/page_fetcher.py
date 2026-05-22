"""Download e extracao de texto das paginas candidatas."""

from __future__ import annotations

from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
import re
import urllib.error
import urllib.request

from relatorio.search.cache import JsonCache
from relatorio.search.types import PageEvidence, RankedSearchHit


class _VisibleTextParser(HTMLParser):
    """Extrai texto visivel de HTML usando apenas a biblioteca padrao."""

    def __init__(self) -> None:
        super().__init__()
        self._hidden_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg"}:
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg"} and self._hidden_depth:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._hidden_depth:
            return
        text = data.strip()
        if text:
            self.parts.append(text)


class PageFetcher:
    """Valida URLs e baixa um trecho textual para enriquecer o ranking."""

    def __init__(
        self,
        cache_dir: Path | None = None,
        timeout: int = 12,
        max_chars: int = 4000,
    ) -> None:
        self.cache = JsonCache(cache_dir) if cache_dir else None
        self.timeout = timeout
        self.max_chars = max_chars

    def fetch_many(self, ranked_hits: list[RankedSearchHit]) -> dict[str, PageEvidence]:
        evidences: dict[str, PageEvidence] = {}
        for item in ranked_hits:
            url = item.hit.url
            if not url:
                continue
            evidences[url] = self.fetch(url)
        return evidences

    def fetch(self, url: str) -> PageEvidence:
        cached = self.cache.get("pages", url) if self.cache else None
        if cached:
            return PageEvidence(**{**cached, "from_cache": True})

        evidence = self._fetch_uncached(url)
        if self.cache:
            self.cache.set("pages", url, {
                "url": evidence.url,
                "final_url": evidence.final_url,
                "status_code": evidence.status_code,
                "ok": evidence.ok,
                "content_excerpt": evidence.content_excerpt,
                "error": evidence.error,
                "fetched_at": evidence.fetched_at,
                "from_cache": False,
            })
        return evidence

    def _fetch_uncached(self, url: str) -> PageEvidence:
        fetched_at = datetime.now().isoformat(timespec="seconds")
        req = urllib.request.Request(url, method="GET")
        req.add_header("User-Agent", "Mozilla/5.0")
        req.add_header("Accept", "text/html,application/xhtml+xml,text/plain,*/*")

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                status = getattr(response, "status", None)
                final_url = response.geturl()
                content_type = response.headers.get("Content-Type", "")
                raw = response.read(1_000_000)
                text = self._decode_body(raw, content_type)
                excerpt = self.extract_visible_text(text)
                return PageEvidence(
                    url=url,
                    final_url=final_url,
                    status_code=status,
                    ok=bool(status is None or status < 400),
                    content_excerpt=excerpt[: self.max_chars],
                    fetched_at=fetched_at,
                )
        except urllib.error.HTTPError as exc:
            return PageEvidence(
                url=url,
                final_url=url,
                status_code=exc.code,
                ok=False,
                error=f"HTTP {exc.code}",
                fetched_at=fetched_at,
            )
        except Exception as exc:
            return PageEvidence(
                url=url,
                final_url=url,
                status_code=None,
                ok=False,
                error=str(exc),
                fetched_at=fetched_at,
            )

    def _decode_body(self, raw: bytes, content_type: str) -> str:
        charset_match = re.search(r"charset=([\w-]+)", content_type, re.I)
        encoding = charset_match.group(1) if charset_match else "utf-8"
        try:
            return raw.decode(encoding, errors="replace")
        except LookupError:
            return raw.decode("utf-8", errors="replace")

    def extract_visible_text(self, html: str) -> str:
        parser = _VisibleTextParser()
        parser.feed(html)
        text = " ".join(parser.parts)
        return " ".join(text.split())
