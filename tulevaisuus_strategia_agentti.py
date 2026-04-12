# -*- coding: utf-8 -*-
"""
Jan Anttilan tulevaisuusstrategia-agentti.
Käyttää Claude API:a (malli: claude-sonnet-4-6) ja samaa .env-tiedostoa kuin finanssi_strategia_agentti.py.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

# Sama .env kuin finanssi_strategia_agentti.py (C:\Dev\agentit\.env)
_ENV_POLKU = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_POLKU)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (OSError, ValueError):
        pass

MALLI = "claude-sonnet-4-6"

JÄRJESTELMÄKEHOTE = """Olet Jan Anttilan tulevaisuusstrategia-agentti.

Tausta:
- Jan on työskennellyt 37 vuotta pankkialalla senior advisor -roolissa ja siirtymässä yrittäjäksi.
- Kiinnostukset: tulevaisuussuuntautunut konsultointi, ratkaisukeskeisyys, tehokkuus ja tuottavuus.

Erikoisalueet:
1. Heikkojen signaalien tunnistaminen — mitä muutoksia on tulossa.
2. Historian syklien analysointi — mitä historia opettaa tästä tilanteesta.
3. Skenaarioanalyysi — mitkä ovat todennäköiset tulevaisuudet.
4. Strategisten toimenpiteiden suosittelu — mitä tehdä nyt.

Anna vastaukset jäsenneltyinä, käytännönläheisesti ja suomea käyttäen, ellei toisin pyydetä.
Tunnista epävarmuudet ja oletukset. Et ole lakimies — ohjaa tarvittaessa asiantuntijoihin."""


def luo_asiakas() -> Anthropic:
    """Luo Anthropic-asiakas ympäristömuuttujasta ANTHROPIC_API_KEY."""
    avain = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not avain:
        print(
            "Virhe: ANTHROPIC_API_KEY puuttuu. Aseta se .env-tiedostoon (C:\\Dev\\agentit\\.env) tai ympäristömuuttujaksi.",
            file=sys.stderr,
        )
        sys.exit(1)
    return Anthropic(api_key=avain)


def lue_tehtävä() -> str:
    """Lukee monirivisen tehtävän; tyhjä rivi päättää syötteen."""
    rivit: list[str] = []
    while True:
        try:
            rivi = input()
        except EOFError:
            break
        if rivi == "":
            break
        rivit.append(rivi)
    return "\n".join(rivit).strip()


def kysy_vahvistus(tehtävä: str) -> bool:
    """Pyytää vahvistuksen ennen analyysin lähettämistä API:lle."""
    print()
    print("--- Lähetettävä analyysitehtävä ---")
    esikatselu = tehtävä if len(tehtävä) <= 2000 else tehtävä[:2000] + "\n... [teksti katkaistu]"
    print(esikatselu)
    print()
    while True:
        vastaus = input(
            "Lähetetäänkö tämä analyysi? Kirjoita 'kyllä' tai 'k' hyväksyäksesi, 'ei' tai 'e' peruuttaaksesi: "
        ).strip().lower()
        if vastaus in ("k", "kyllä", "j", "joo"):
            return True
        if vastaus in ("e", "ei", "n", "ei kiitos"):
            return False
        print("Anna vastaus: k / kyllä (hyväksy) tai e / ei (peruuta).")


def suorita_analyysi(asiakas: Anthropic, tehtävä: str) -> str:
    """Lähettää tehtävän Claudelle ja palauttaa tekstivastauksen."""
    viesti = asiakas.messages.create(
        model=MALLI,
        max_tokens=8192,
        system=JÄRJESTELMÄKEHOTE,
        messages=[{"role": "user", "content": tehtävä}],
    )
    osat: list[str] = []
    for lohko in viesti.content:
        if hasattr(lohko, "text"):
            osat.append(lohko.text)
    return "".join(osat)


def main() -> None:
    print("Tulevaisuusstrategia-agentti (Claude Sonnet 4.6)")
    print("Jokaisen analyysin edellytyksenä on vahvistus ennen lähetystä.")
    print()

    asiakas = luo_asiakas()

    while True:
        print("Kirjoita analyysitehtävä (useita rivejä). Tyhjä rivi päättää syötteen.")
        print("Jätä tehtävä kokonaan tyhjäksi (vain Enter) lopettaaksesi ohjelman.")
        print()

        tehtävä = lue_tehtävä()
        if not tehtävä:
            print("Lopetetaan.")
            break

        if not kysy_vahvistus(tehtävä):
            print("Analyysi peruutettu — voit syöttää uuden tehtävän.")
            print()
            continue

        print()
        print("Lähetetään... Odota hetki.")
        try:
            vastaus = suorita_analyysi(asiakas, tehtävä)
        except Exception as virhe:
            print(f"Virhe API-kutsussa: {virhe}", file=sys.stderr)
            print()
            continue

        print()
        print("--- Analyysin vastaus ---")
        print(vastaus)
        print()
        print("—" * 40)
        print()


if __name__ == "__main__":
    main()
