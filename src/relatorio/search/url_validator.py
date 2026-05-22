"""Validacao tecnica de URLs encontradas."""

from __future__ import annotations

import urllib.error
import urllib.request


def verify_url(url: str, timeout: int = 10) -> bool:
    """
    Verifica se uma URL responde com status HTTP valido (< 400).

    Tenta HEAD primeiro; se o servidor nao aceitar, cai para GET.
    """
    req = urllib.request.Request(url, method="HEAD")
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status < 400
    except urllib.error.HTTPError as exc:
        if exc.code != 405:
            return False

        req_get = urllib.request.Request(url, method="GET")
        req_get.add_header("User-Agent", "Mozilla/5.0")
        try:
            with urllib.request.urlopen(req_get, timeout=timeout) as response:
                return response.status < 400
        except Exception:
            return False
    except Exception:
        return False
