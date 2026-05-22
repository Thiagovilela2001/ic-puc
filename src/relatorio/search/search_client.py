"""Clientes de busca web usados pela camada semantica."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from time import perf_counter

from relatorio.search.cache import JsonCache
from relatorio.search.types import SearchHit, SearchStats


class SearchClient:
    """
    Executa consultas em APIs reais e retorna resultados estruturados.

    Prioriza Serper quando `SERPER_API_KEY` esta configurada. Se nao houver chave
    ou se a chamada falhar, usa DuckDuckGo como fallback gratuito.
    """

    def __init__(self, cache_dir: Path | None = None) -> None:
        self.cache = JsonCache(cache_dir) if cache_dir else None

    def search_many(
        self,
        queries: list[str],
        max_per_query: int = 5,
    ) -> tuple[list[SearchHit], list[str], SearchStats]:
        started = perf_counter()
        errors: list[str] = []
        cache_hits = 0
        source = ""

        if os.getenv("SERPER_API_KEY"):
            hits, cache_hits = self._search_serper(queries, max_per_query, errors)
            if hits:
                source = "serper"
                return hits, errors, SearchStats(
                    source=source,
                    raw_hits_total=len(hits),
                    cache_hits=cache_hits,
                    duration_seconds=round(perf_counter() - started, 3),
                )

        hits, cache_hits = self._search_duckduckgo(queries, max_per_query, errors)
        source = "duckduckgo"
        return hits, errors, SearchStats(
            source=source,
            raw_hits_total=len(hits),
            cache_hits=cache_hits,
            duration_seconds=round(perf_counter() - started, 3),
        )

    def _search_serper(
        self,
        queries: list[str],
        max_per_query: int,
        errors: list[str],
    ) -> tuple[list[SearchHit], int]:
        key = os.getenv("SERPER_API_KEY")
        if not key:
            return [], 0

        print(f"  [busca] Usando Serper API — {len(queries)} queries...")
        hits: list[SearchHit] = []
        cache_hits = 0

        for i, query in enumerate(queries, 1):
            cached = self._load_cached_hits("serper", query, max_per_query)
            if cached is not None:
                cache_hits += 1
                hits.extend(cached)
                print(f"    [{i}/{len(queries)}] CACHE ({len(cached)}) — {query[:60]}")
                continue

            try:
                payload = json.dumps({
                    "q": query,
                    "gl": "br",
                    "hl": "pt-br",
                    "num": max_per_query,
                }).encode("utf-8")
                req = urllib.request.Request(
                    "https://google.serper.dev/search",
                    data=payload,
                    method="POST",
                    headers={
                        "X-API-KEY": key,
                        "Content-Type": "application/json",
                    },
                )
                with urllib.request.urlopen(req, timeout=20) as response:
                    data = json.loads(response.read().decode("utf-8"))

                query_hits = self._parse_serper_results(query, data)
                hits.extend(query_hits[:max_per_query])
                self._save_cached_hits("serper", query, max_per_query, query_hits[:max_per_query])
                print(f"    [{i}/{len(queries)}] OK ({len(query_hits[:max_per_query])}) — {query[:60]}")
                time.sleep(0.2)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                message = f"Serper falhou para query {i}: {exc}"
                errors.append(message)
                print(f"    [{i}/{len(queries)}] FALHA — {exc}")
            except Exception as exc:
                message = f"Serper falhou para query {i}: {exc}"
                errors.append(message)
                print(f"    [{i}/{len(queries)}] FALHA — {exc}")

        return hits, cache_hits

    def _parse_serper_results(self, query: str, data: dict) -> list[SearchHit]:
        hits: list[SearchHit] = []
        for item in data.get("organic", []):
            url = item.get("link", "") or item.get("url", "")
            if not url:
                continue
            hits.append(
                SearchHit(
                    query=query,
                    title=item.get("title", ""),
                    url=url,
                    snippet=item.get("snippet", ""),
                    source="serper",
                )
            )
        return hits

    def _search_duckduckgo(
        self,
        queries: list[str],
        max_per_query: int,
        errors: list[str],
    ) -> tuple[list[SearchHit], int]:
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            errors.append("duckduckgo-search nao esta instalado.")
            print("  [busca] duckduckgo-search não instalado.")
            return [], 0

        print(f"  [busca] Usando DuckDuckGo — {len(queries)} queries...")
        hits: list[SearchHit] = []
        cache_hits = 0

        for i, query in enumerate(queries, 1):
            cached = self._load_cached_hits("duckduckgo", query, max_per_query)
            if cached is not None:
                cache_hits += 1
                hits.extend(cached)
                print(f"    [{i}/{len(queries)}] CACHE ({len(cached)}) — {query[:60]}")
                continue

            last_error = ""
            for attempt in range(3):
                try:
                    with DDGS() as ddg:
                        results = list(ddg.text(query, max_results=max_per_query))
                    query_hits = [
                        SearchHit(
                            query=query,
                            title=item.get("title", ""),
                            url=item.get("href", ""),
                            snippet=item.get("body", ""),
                            source="duckduckgo",
                        )
                        for item in results
                        if item.get("href")
                    ]
                    hits.extend(query_hits)
                    self._save_cached_hits("duckduckgo", query, max_per_query, query_hits)
                    print(f"    [{i}/{len(queries)}] OK ({len(query_hits)}) — {query[:60]}")
                    time.sleep(0.5)
                    break
                except Exception as exc:
                    last_error = str(exc)
                    if attempt < 2:
                        time.sleep(2 ** attempt)
                    else:
                        message = f"DuckDuckGo falhou para query {i}: {last_error}"
                        errors.append(message)
                        print(f"    [{i}/{len(queries)}] FALHA — {last_error}")

        return hits, cache_hits

    def _cache_key(self, source: str, query: str, max_per_query: int) -> str:
        return f"{source}:{max_per_query}:{query}"

    def _load_cached_hits(
        self,
        source: str,
        query: str,
        max_per_query: int,
    ) -> list[SearchHit] | None:
        if not self.cache:
            return None
        cached = self.cache.get("search", self._cache_key(source, query, max_per_query))
        if not cached:
            return None
        try:
            return [SearchHit(**item) for item in cached.get("hits", [])]
        except TypeError:
            return None

    def _save_cached_hits(
        self,
        source: str,
        query: str,
        max_per_query: int,
        hits: list[SearchHit],
    ) -> None:
        if not self.cache:
            return
        self.cache.set(
            "search",
            self._cache_key(source, query, max_per_query),
            {
                "source": source,
                "query": query,
                "max_per_query": max_per_query,
                "fetched_at": datetime.now().isoformat(timespec="seconds"),
                "hits": [asdict(hit) for hit in hits],
            },
        )
