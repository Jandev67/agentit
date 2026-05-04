def _suora_hae(hakutermi: str, lahde: str, max_tuloksia: int = 5) -> list[str]:
    """Hakee suoraan lähteen omalta hakusivulta tai RSS-syötteestä."""
    kysely = quote_plus(hakutermi)
    urlit: list[str] = []

    # Symbolitaulukko Yahoo Finance RSS:ää varten
    symbolit = {
        "neste": "NESTE.HE",
        "nordea": "NDA-FI.HE",
        "nokia": "NOKIA.HE",
        "fortum": "FORTUM.HE",
        "sampo": "SAMPO.HE",
        "elisa": "ELISA.HE",
        "upm": "UPM.HE",
        "mandatum": "MANTA.HE",
        "puuilo": "PUUILO.HE",
        "ssab": "SSAB-A.ST",
        "nokian": "TYRES.HE",
        "valmet": "VALMT.HE",
    }

    if "yahoo" in lahde or "finance.yahoo" in lahde:
        # Etsi symboli hakutermistä
        termi_lower = hakutermi.lower()
        symboli = None
        for avain, arvo in symbolit.items():
            if avain in termi_lower:
                symboli = arvo
                break

        if symboli:
            # RSS-syöte symbolilla
            rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symboli}"
            soup = _hae_sivu(rss_url)
            if soup:
                for item in soup.find_all("item"):
                    link = item.find("link")
                    if link and link.text.startswith("http"):
                        urlit.append(link.text.strip())
        else:
            # Yleinen Yahoo Finance haku
            haku_url = f"https://query1.finance.yahoo.com/v1/finance/search?q={kysely}&lang=fi&newsCount=5"
            try:
                resp = requests.get(haku_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
                data = resp.json()
                for uutinen in data.get("news", []):
                    if "url" in uutinen:
                        urlit.append(uutinen["url"])
            except Exception as e:
                logger.debug("Yahoo Finance haku epäonnistui: %s", e)

    elif "nordnet.fi" in lahde:
        haku_url = f"https://www.nordnet.fi/fi/market/search?query={kysely}"
        soup = _hae_sivu(haku_url)
        if soup:
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/news/" in href or "/uutiset/" in href:
                    if href.startswith("http"):
                        urlit.append(href)
                    else:
                        urlit.append("https://www.nordnet.fi" + href)

    elif "talouselama.fi" in lahde:
        haku_url = f"https://www.talouselama.fi/haku?q={kysely}"
        soup = _hae_sivu(haku_url)
        if soup:
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "talouselama.fi" in href and len(href) > 40:
                    urlit.append(href)

    elif "taloussanomat.fi" in lahde:
        haku_url = f"https://www.taloussanomat.fi/?search={kysely}"
        soup = _hae_sivu(haku_url)
        if soup:
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "taloussanomat.fi" in href and len(href) > 40:
                    urlit.append(href)

    return list(dict.fromkeys(urlit))[:max_tuloksia]