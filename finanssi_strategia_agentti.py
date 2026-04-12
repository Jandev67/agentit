# -*- coding: utf-8 -*-
"""
Jan Anttilan henkilökohtainen finanssi- ja strategia-agentti.
Käyttää Claude API:a (malli: claude-sonnet-4-6).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

# Lataa API-avain ympäristömuuttujaan: ensin .env (sama kansio kuin tämä skripti), sitten järjestelmä
_ENV_POLKU = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_POLKU)

# Varmista UTF-8 -tuloste Windows-konsolissa
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (OSError, ValueError):
        pass

MALLI = "claude-sonnet-4-6"

JÄRJESTELMÄKEHOTE = """Olet Jan Anttilan henkilökohtainen finanssi- ja strategia-agentti.

Tausta:
- Jan on työskennellyt 37 vuotta pankkialalla senior advisor -roolissa, lähes 30 vuotta johtotehtävissä.
- Tavoitteena on siirtyä itsenäiseksi yrittäjäksi vuoden sisällä.

Tehtäväsi:
1. Analysoida liiketoimintamahdollisuuksia finanssialan näkökulmasta.
2. Tehdä strategista tulevaisuusanalyysiä historian oppeja hyödyntäen.
3. Arvioida sijoitusmahdollisuuksia ja riskejä.
4. Tukea yrittäjyyspolun suunnittelua.

Anna vastaukset selkeästi ja käytännönläheisesti. Käytä suomea, ellei Jan pyydä muuta.
Tunnista rajoitteet: et ole lakimies tai veroneuvoja — ohjaa tarvittaessa ammattilaisiin."""


def luo_asiakas() -> Anthropic:
    """Luo Anthropic-asiakas ympäristömuuttujasta ANTHROPIC_API_KEY."""
    avain = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not avain:
        print(
            "Virhe: ANTHROPIC_API_KEY puuttuu. Aseta se ympäristömuuttujaksi tai .env-tiedostoon.",
            file=sys.stderr,
        )
        sys.exit(1)
    return Anthropic(api_key=avain)


def main() -> None:
    print("Finanssi- ja strategia-agentti (Claude Sonnet 4.6)")
    print("Kirjoita tehtävä (useita rivejä sallittu). Lopeta tyhjällä rivillä.")
    print()

    rivit: list[str] = []
    while True:
        try:
            rivi = input()
        except EOFError:
            break
        if rivi == "":
            break
        rivit.append(rivi)
    tehtävä = "\n".join(rivit).strip()

    if not tehtävä:
        print("Ei tehtävää — lopetetaan.")
        return

    asiakas = luo_asiakas()

    viesti = asiakas.messages.create(
        model=MALLI,
        max_tokens=8192,
        system=JÄRJESTELMÄKEHOTE,
        messages=[{"role": "user", "content": tehtävä}],
    )

    # Tekstisisältö voi olla useassa lohkossa
    osat: list[str] = []
    for lohko in viesti.content:
        if hasattr(lohko, "text"):
            osat.append(lohko.text)
    vastaus = "".join(osat)

    print()
    print("--- Vastaus ---")
    print(vastaus)


if __name__ == "__main__":
    main()
