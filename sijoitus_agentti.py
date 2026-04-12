# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

_KANSIO = Path(__file__).resolve().parent
_ENV_POLKU = _KANSIO / ".env"
_PROMPT_POLKU = _KANSIO / "sijoitus_prompt.txt"

load_dotenv(_ENV_POLKU)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (OSError, ValueError):
        pass
if hasattr(sys.stdin, "reconfigure"):
    try:
        sys.stdin.reconfigure(encoding="utf-8")
    except (OSError, ValueError):
        pass

MALLI = "claude-sonnet-4-6"


def lue_järjestelmäkehote() -> str:
    if not _PROMPT_POLKU.is_file():
        print(f"Virhe: {_PROMPT_POLKU} puuttuu.", file=sys.stderr)
        sys.exit(1)
    return _PROMPT_POLKU.read_text(encoding="utf-8").strip()


def luo_asiakas() -> Anthropic:
    avain = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not avain:
        print(
            "Virhe: ANTHROPIC_API_KEY puuttuu (.env tai ympäristö).",
            file=sys.stderr,
        )
        sys.exit(1)
    return Anthropic(api_key=avain)


def vastauksen_teksti(viesti: object) -> str:
    osat: list[str] = []
    for lohko in viesti.content:
        if hasattr(lohko, "text"):
            osat.append(lohko.text)
    return "".join(osat)


def main() -> None:
    järjestelmä = lue_järjestelmäkehote()
    asiakas = luo_asiakas()
    historia: list[dict[str, str]] = []

    print("Sijoitus-agentti — kirjoita viesti. 'exit' tai 'lopeta' lopettaa.")
    while True:
        try:
            rivi = input("> ").strip()
        except EOFError:
            print()
            break

        if not rivi:
            continue

        if rivi.lower() in ("exit", "lopeta"):
            break

        historia.append({"role": "user", "content": rivi})

        try:
            vastaus_obj = asiakas.messages.create(
                model=MALLI,
                max_tokens=8192,
                system=järjestelmä,
                messages=historia,
            )
        except Exception as e:
            print(f"API-virhe: {e}", file=sys.stderr)
            historia.pop()
            continue

        teksti = vastauksen_teksti(vastaus_obj)
        historia.append({"role": "assistant", "content": teksti})
        print(teksti)
        print()


if __name__ == "__main__":
    main()
