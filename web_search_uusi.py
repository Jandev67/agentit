"""
web_search.py — Sijoitusagentin web-hakumoduuli
================================================
Priorisoi suomalaiset talousuutislähteet ja palauttaa
jäsennellyn hakutuloksen agentin käyttöön.

Käyttö:
    from web_search import hae_uutiset, hae_kurssi

Vaatimukset:
    pip install requests beautifulsoup4
"""

import re
import sys
import time
import logging
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import quote_plus, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Pakota UTF-8 tulostukseen Windowsin oletuskonsolia varten
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Konfiguraatio
# ---------------------------------------------------------------------------

# Lähdeprioriteetti — alempi numero = korkeampi prioriteetti
LAHDE_PRIORITEETTI: dict[str, int] = {
    "kauppalehti.fi": 1,
    "inderes.fi": 2,
    "nordnet.fi": 3,
    "taloussanomat.fi": 4,
    "talouselama.fi": 5,
    "hs.fi": 6,       # talousosio
    "reuters.com": 7,
    "ft.com": 8,
    "bloomberg.com": 9,
}

# Sivukohtaiset CSS-selektorit sisällönpoimintaan
SISALTO_SELEKTORIT: dict[str, list[str]] = {
    "kauppalehti.fi": [
        "div.article-body",
        "div.article__body",
        "section.article-content",
        "div[class*='articleBody']",
    ],
    "inderes.fi": [
        "div.article-content",
        "div.post-content",
        "div[class*='content']",
    ],
    "nordnet.fi": [
        "div.article__body",
        "main article",
    ],
    "_default": [
        "article",
        "div[class*='article']",
        "div[class*='content']",
        "main",
        "div.entry-content",
    ],
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

REQUEST_TIMEOUT = 10      # sekuntia
MAX_SISALTO_MERKIT = 3000 # maksimimerkkimäärä per artikkeli agentille
HAKUTULOSTEN_MAX = 5      # montako tulosta palautetaan per haku

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("web_search")


# ---------------------------------------------------------------------------
# Tietorakenteet
# ---------------------------------------------------------------------------

@dataclass
class HakuTulos:
    url: str
    otsikko: str
    sisalto: str          # katkaistu artikkelin teksti
    lahde: str            # domain, esim. "kauppalehti.fi"
    paivamaara: str = ""  # jos löytyy sivulta
    prioriteetti: int = 99
    virhe: Optional[str] = None

    def __str__(self) -> str:
        paiva = f" [{self.paivamaara}]" if self.paivamaara else ""
        return (
            f"[{self.lahde}{paiva}] {self.otsikko}\n"
            f"{self.url}\n"
            f"{self.sisalto[:500]}..."
        )

    def agentille(self) -> str:
        """Palauttaa agentille optimoidun tekstimuodon."""
        paiva = f" ({self.paivamaara})" if self.paivamaara else ""
        return (
            f"LÄHDE: {self.lahde}{paiva}\n"
            f"OTSIKKO: {self.otsikko}\n"
            f"URL: {self.url}\n"
            f"SISÄLTÖ:\n{self.sisalto}\n"
            f"{'─' * 60}"
        )


# ---------------------------------------------------------------------------
# Apufunktiot
# ---------------------------------------------------------------------------

def _domain(url: str) -> str:
    """Palauttaa URL:n domainin ilman www-etuliitettä."""
    netloc = urlparse(url).netloc
    return netloc.removeprefix("www.")


def _prioriteetti(url: str) -> int:
    domain = _domain(url)
    for avain, arvo in LAHDE_PRIORITEETTI.items():
        if avain in domain:
            return arvo
    return 99


def _hae_sivu(url: str) -> Optional[BeautifulSoup]:
    """Hakee sivun ja palauttaa BeautifulSoup-objektin tai None."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.exceptions.HTTPError as e:
        logger.debug("HTTP-virhe %s: %s", url, e)
    except requests.exceptions.ConnectionError:
        logger.debug("Yhteysvirhe: %s", url)
    except requests.exceptions.Timeout:
        logger.debug("Aikakatkaisu: %s", url)
    except Exception as e:
        logger.debug("Tuntematon virhe %s: %s", url, e)
    return None


def _poimi_teksti(soup: BeautifulSoup, domain: str) -> str:
    """Poimii artikkelin tekstin sivukohtaisilla selektoreilla."""
    # Poista script, style, nav, footer -elementit
    for tag in soup(["script", "style", "nav", "footer", "header",
                     "aside", "form", "button", "noscript"]):
        tag.decompose()

    # Kokeile sivukohtaisia selektoreita
    selektorit = SISALTO_SELEKTORIT.get(domain, []) + SISALTO_SELEKTORIT["_default"]

    for sel in selektorit:
        elementti = soup.select_one(sel)
        if elementti:
            teksti = elementti.get_text(separator=" ", strip=True)
            teksti = re.sub(r"\s+", " ", teksti)
            if len(teksti) > 200:  # Riittävästi sisältöä
                return teksti[:MAX_SISALTO_MERKIT]

    # Fallback: koko body
    body = soup.find("body")
    if body:
        teksti = body.get_text(separator=" ", strip=True)
        return re.sub(r"\s+", " ", teksti)[:MAX_SISALTO_MERKIT]

    return ""


def _poimi_otsikko(soup: BeautifulSoup) -> str:
    """Poimii sivun otsikon."""
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return og_title["content"].strip()
    if soup.title:
        return soup.title.string.strip() if soup.title.string else ""
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else ""


def _poimi_paivamaara(soup: BeautifulSoup) -> str:
    """Yrittää poimia julkaisupäivämäärän."""
    # Open Graph / meta
    for meta_attr in [
        {"property": "article:published_time"},
        {"name": "date"},
        {"name": "pubdate"},
        {"itemprop": "datePublished"},
    ]:
        tag = soup.find("meta", meta_attr)
        if tag and tag.get("content"):
            arvo = tag["content"]
            # Ota vain päivämääräosa (YYYY-MM-DD)
            match = re.search(r"\d{4}-\d{2}-\d{2}", arvo)
            if match:
                return match.group()

    # time-elementti
    time_tag = soup.find("time")
    if time_tag:
        dt = time_tag.get("datetime", time_tag.get_text(strip=True))
        match = re.search(r"\d{4}-\d{2}-\d{2}", dt)
        if match:
            return match.group()

    return ""


# ---------------------------------------------------------------------------
# Google-haku (site:-rajoituksella)
# ---------------------------------------------------------------------------

def _google_hae(hakutermi: str, site: Optional[str] = None,
                max_tuloksia: int = 5) -> list[str]:
    """
    Hakee DuckDuckGo JSON API:lla ja palauttaa URL-listan.
    Kokeilee ensin JSON API:a, fallback HTML-parsintaan.
    """
    if site:
        kysely = f"site:{site} {hakutermi}"
    else:
        kysely = hakutermi

    # Yritys 1: DuckDuckGo JSON API
    try:
        url = f"https://api.duckduckgo.com/?q={quote_plus(kysely)}&format=json&no_redirect=1&no_html=1"
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        urlit = []
        # RelatedTopics sisältää hakutulokset
        for item in data.get("RelatedTopics", []):
            if isinstance(item, dict) and "FirstURL" in item:
                urlit.append(item["FirstURL"])
            # Joskus tulokset ovat sisäkkäisiä
            elif isinstance(item, dict) and "Topics" in item:
                for sub in item["Topics"]:
                    if "FirstURL" in sub:
                        urlit.append(sub["FirstURL"])

        if urlit:
            return urlit[:max_tuloksia]

    except Exception as e:
        logger.debug("DDG JSON API epäonnistui: %s", e)

    # Yritys 2: DuckDuckGo Lite (kevyempi kuin HTML, vähemmän blokkauksia)
    try:
        url = f"https://lite.duckduckgo.com/lite/?q={quote_plus(kysely)}"
        headers = {**HEADERS, "Referer": "https://lite.duckduckgo.com/"}
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        urlit = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("http") and "duckduckgo.com" not in href:
                urlit.append(href)

        if urlit:
            return list(dict.fromkeys(urlit))[:max_tuloksia]

    except Exception as e:
        logger.warning("DDG Lite epäonnistui: %s", e)

    return []


def _priorisoi_urlit(urlit: list[str]) -> list[str]:
    """Järjestää URL-listan lähdeprioriteettijärjestykseen."""
    return sorted(urlit, key=_prioriteetti)


# ---------------------------------------------------------------------------
# Julkiset funktiot
# ---------------------------------------------------------------------------

def hae_artikkeli(url: str) -> HakuTulos:
    """Hakee yksittäisen artikkelin URL:n perusteella."""
    domain = _domain(url)
    soup = _hae_sivu(url)

    if soup is None:
        return HakuTulos(
            url=url,
            otsikko="",
            sisalto="",
            lahde=domain,
            prioriteetti=_prioriteetti(url),
            virhe="Sivua ei voitu hakea",
        )

    return HakuTulos(
        url=url,
        otsikko=_poimi_otsikko(soup),
        sisalto=_poimi_teksti(soup, domain),
        lahde=domain,
        paivamaara=_poimi_paivamaara(soup),
        prioriteetti=_prioriteetti(url),
    )


def hae_uutiset(
    hakutermi: str,
    lahteet: Optional[list[str]] = None,
    max_tuloksia: int = HAKUTULOSTEN_MAX,
    viive_sekuntia: float = 1.0,
) -> list[HakuTulos]:
    """
    Hakee uutisia hakutermillä, priorisoi määritellyt lähteet.

    Args:
        hakutermi:      Esim. "Neste SAF lentopolttoaine"
        lahteet:        Lista domaineista, esim. ["kauppalehti.fi", "inderes.fi"]
                        Jos None, käyttää oletusprioriteettilistaa.
        max_tuloksia:   Montako artikkelia haetaan yhteensä.
        viive_sekuntia: Viive pyyntöjen välillä (älä spammaa).

    Returns:
        Lista HakuTulos-objekteja prioriteettijärjestyksessä.
    """
    if lahteet is None:
        lahteet = list(LAHDE_PRIORITEETTI.keys())

    kaikki_urlit: list[str] = []

    # Hae ensin prioriteettilähteiden kautta
    for lahde in lahteet[:3]:  # Haetaan kolmesta tärkeimmästä
        urlit = _google_hae(hakutermi, site=lahde, max_tuloksia=3)
        kaikki_urlit.extend(urlit)
        if urlit:
            time.sleep(viive_sekuntia)

    # Täydennä yleisellä haulla jos tuloksia vähän
    if len(kaikki_urlit) < max_tuloksia:
        taydennys = _google_hae(
            f"{hakutermi} talous sijoitus",
            max_tuloksia=max_tuloksia - len(kaikki_urlit)
        )
        kaikki_urlit.extend(taydennys)

    # Poista duplikaatit, priorisoi
    uniikit = list(dict.fromkeys(kaikki_urlit))
    priorisoidut = _priorisoi_urlit(uniikit)[:max_tuloksia]

    # Hae artikkelit
    tulokset: list[HakuTulos] = []
    for url in priorisoidut:
        logger.info("Haetaan: %s", url)
        tulos = hae_artikkeli(url)
        if not tulos.virhe:
            tulokset.append(tulos)
        time.sleep(viive_sekuntia * 0.5)

    # Järjestä prioriteetin mukaan
    tulokset.sort(key=lambda t: t.prioriteetti)
    return tulokset


def muodosta_hakukonteksti(tulokset: list[HakuTulos]) -> str:
    """
    Muodostaa agentille syötettävän kontekstiblokin hakutuloksista.
    Tämä syötetään system promptin lisäksi tai user-viestinä.
    """
    if not tulokset:
        return "Hakutuloksia ei löytynyt."

    osat = [
        f"WEBBI-HAKUTULOKSET ({len(tulokset)} artikkelia, "
        f"haettu juuri äsken):\n{'═' * 60}"
    ]
    for i, tulos in enumerate(tulokset, 1):
        osat.append(f"\n[{i}/{len(tulokset)}]\n{tulos.agentille()}")

    return "\n".join(osat)


def hae_ja_muodosta_konteksti(
    hakutermi: str,
    lahteet: Optional[list[str]] = None,
    max_tuloksia: int = HAKUTULOSTEN_MAX,
) -> str:
    """
    Kätevä kaikessa-yhdessä -funktio: hakee ja palauttaa
    agentille valmiin kontekstiblokin.

    Esimerkki:
        konteksti = hae_ja_muodosta_konteksti("Neste Q1 2025")
        # → syötetään agentin user-viestiin hakutuloksina
    """
    tulokset = hae_uutiset(hakutermi, lahteet=lahteet, max_tuloksia=max_tuloksia)
    return muodosta_hakukonteksti(tulokset)


# ---------------------------------------------------------------------------
# Nopea testaus komentoriviltä
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    termi = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Neste osavuosikatsaus 2025"
    print(f"\n🔍 Haetaan: '{termi}'\n")

    tulokset = hae_uutiset(termi, max_tuloksia=3)

    if not tulokset:
        print("Ei tuloksia.")
    else:
        for t in tulokset:
            print(t.agentille())
            print()
