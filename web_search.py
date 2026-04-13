# -*- coding: utf-8 -*-
"""
web_search.py - Sijoitusagentin web-hakumoduuli
Hakee suoraan prioriteettilahteilta ilman hakumoottoria.
"""

import re
import time
import logging
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus, urlparse

import requests
from bs4 import BeautifulSoup

LAHDE_PRIORITEETTI = {
    "kauppalehti.fi": 1,
    "inderes.fi": 2,
    "nordnet.fi": 3,
    "taloussanomat.fi": 4,
    "talouselama.fi": 5,
    "hs.fi": 6,
    "reuters.com": 7,
    "ft.com": 8,
    "bloomberg.com": 9,
}

LAHDE_HAKUURL = {
    "kauppalehti.fi":  "https://www.kauppalehti.fi/uutiset/haku?query={q}",
    "inderes.fi":      "https://www.inderes.fi/?s={q}",
    "taloussanomat.fi":"https://www.is.fi/haku/?query={q}&category=taloussanomat",
    "talouselama.fi":  "https://www.talouselama.fi/haku?q={q}",
    "hs.fi":           "https://www.hs.fi/haku/?query={q}",
    "reuters.com":     "https://www.reuters.com/search/news?blob={q}",
}

SISALTO_SELEKTORIT = {
    "kauppalehti.fi": ["div.article-body", "div.article__body", "section.article-content"],
    "inderes.fi":     ["div.article-content", "div.post-content"],
    "_default":       ["article", "main", "div.entry-content", "div.content"],
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fi-FI,fi;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

REQUEST_TIMEOUT = 10
MAX_SISALTO = 3000
MAX_TULOKSIA = 5

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger("web_search")


@dataclass
class HakuTulos:
    url: str
    otsikko: str
    sisalto: str
    lahde: str
    paivamaara: str = ""
    prioriteetti: int = 99
    virhe: Optional[str] = None

    def agentille(self) -> str:
        paiva = f" ({self.paivamaara})" if self.paivamaara else ""
        return (
            f"LAHDE: {self.lahde}{paiva}\n"
            f"OTSIKKO: {self.otsikko}\n"
            f"URL: {self.url}\n"
            f"SISALTO:\n{self.sisalto}\n"
            f"{'-' * 60}"
        )


def _domain(url: str) -> str:
    netloc = urlparse(url).netloc
    return netloc.removeprefix("www.")


def _prioriteetti(url: str) -> int:
    domain = _domain(url)
    for avain, arvo in LAHDE_PRIORITEETTI.items():
        if avain in domain:
            return arvo
    return 99


def _hae_sivu(url: str) -> Optional[BeautifulSoup]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        logger.debug("Virhe haussa %s: %s", url, e)
    return None


def _poimi_linkit(soup: BeautifulSoup, base_domain: str) -> list:
    linkit = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/"):
            href = f"https://www.{base_domain}{href}"
        if not href.startswith("http"):
            continue
        if base_domain not in href:
            continue
        if href in linkit:
            continue
        linkit.append(href)
    return linkit


def _poimi_teksti(soup: BeautifulSoup, domain: str) -> str:
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.decompose()
    selektorit = SISALTO_SELEKTORIT.get(domain, []) + SISALTO_SELEKTORIT["_default"]
    for sel in selektorit:
        el = soup.select_one(sel)
        if el:
            teksti = re.sub(r"\s+", " ", el.get_text(separator=" ", strip=True))
            if len(teksti) > 200:
                return teksti[:MAX_SISALTO]
    body = soup.find("body")
    if body:
        return re.sub(r"\s+", " ", body.get_text(separator=" ", strip=True))[:MAX_SISALTO]
    return ""


def _poimi_otsikko(soup: BeautifulSoup) -> str:
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else ""


def _poimi_paivamaara(soup: BeautifulSoup) -> str:
    for attr in [{"property": "article:published_time"}, {"name": "date"}, {"itemprop": "datePublished"}]:
        tag = soup.find("meta", attr)
        if tag and tag.get("content"):
            m = re.search(r"\d{4}-\d{2}-\d{2}", tag["content"])
            if m:
                return m.group()
    time_tag = soup.find("time")
    if time_tag:
        dt = time_tag.get("datetime", time_tag.get_text(strip=True))
        m = re.search(r"\d{4}-\d{2}-\d{2}", dt)
        if m:
            return m.group()
    return ""


def _hae_lahteelta(hakutermi: str, domain: str, max_tuloksia: int = 3) -> list:
    hakuurl_pohja = LAHDE_HAKUURL.get(domain)
    if not hakuurl_pohja:
        return []
    url = hakuurl_pohja.format(q=quote_plus(hakutermi))
    soup = _hae_sivu(url)
    if not soup:
        return []
    linkit = _poimi_linkit(soup, domain)
    artikkelit = [
        l for l in linkit
        if any(x in l for x in ["/uutiset/a/", "/artikkelit/", "/news/", "/article/"])
    ]
    return artikkelit[:max_tuloksia]


def hae_artikkeli(url: str) -> HakuTulos:
    domain = _domain(url)
    soup = _hae_sivu(url)
    if soup is None:
        return HakuTulos(url=url, otsikko="", sisalto="", lahde=domain,
                         prioriteetti=_prioriteetti(url), virhe="Sivua ei voitu hakea")
    return HakuTulos(
        url=url,
        otsikko=_poimi_otsikko(soup),
        sisalto=_poimi_teksti(soup, domain),
        lahde=domain,
        paivamaara=_poimi_paivamaara(soup),
        prioriteetti=_prioriteetti(url),
    )


def hae_uutiset(hakutermi, lahteet=None, max_tuloksia=MAX_TULOKSIA, viive=1.0):
    if lahteet is None:
        lahteet = list(LAHDE_PRIORITEETTI.keys())
    kaikki_urlit = []
    for lahde in lahteet[:4]:
        print(f"  Haetaan {lahde}...")
        urlit = _hae_lahteelta(hakutermi, lahde, max_tuloksia=3)
        kaikki_urlit.extend(urlit)
        if urlit:
            time.sleep(viive)
    uniikit = list(dict.fromkeys(kaikki_urlit))
    priorisoidut = sorted(uniikit, key=_prioriteetti)[:max_tuloksia]
    tulokset = []
    for url in priorisoidut:
        tulos = hae_artikkeli(url)
        if not tulos.virhe:
            tulokset.append(tulos)
        time.sleep(viive * 0.5)
    tulokset.sort(key=lambda t: t.prioriteetti)
    return tulokset


def muodosta_hakukonteksti(tulokset):
    if not tulokset:
        return "Hakutuloksia ei loytynyt."
    osat = [f"WEB-HAKUTULOKSET ({len(tulokset)} artikkelia):\n{'=' * 60}"]
    for i, t in enumerate(tulokset, 1):
        osat.append(f"\n[{i}/{len(tulokset)}]\n{t.agentille()}")
    return "\n".join(osat)


def hae_ja_muodosta_konteksti(hakutermi, lahteet=None, max_tuloksia=MAX_TULOKSIA):
    tulokset = hae_uutiset(hakutermi, lahteet=lahteet, max_tuloksia=max_tuloksia)
    return muodosta_hakukonteksti(tulokset)


if __name__ == "__main__":
    import sys
    termi = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Neste osavuosikatsaus 2025"
    print(f"\nHaetaan: '{termi}'\n")
    tulokset = hae_uutiset(termi, max_tuloksia=3)
    if not tulokset:
        print("Ei tuloksia.")
    else:
        for t in tulokset:
            print(t.agentille())
            print()