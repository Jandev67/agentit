# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

_KANSIO = Path(__file__).resolve().parent
_ENV_POLKU = _KANSIO / ".env"
_PROMPT_POLKU = _KANSIO / "jan_core_prompt.txt"
_MUISTI_KANSIO = _KANSIO / "muisti"
_HISTORIA_POLKU = _MUISTI_KANSIO / "jan_core_historia.json"
_TIEDOSTO_MAX_KIERROKSET = 500
_API_MAX_KIERROKSET = 10

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


def kierroksesta_historia(kierrokset: list[dict[str, object]]) -> list[dict[str, str]]:
    """Rakentaa Anthropic-viestilistauksen viimeisistä kierroksista."""
    historia: list[dict[str, str]] = []
    viimeiset = kierrokset[-_API_MAX_KIERROKSET:]
    for k in viimeiset:
        if not isinstance(k, dict):
            continue
        kä = k.get("käyttäjän_viesti")
        ag = k.get("agentin_vastaus")
        if not isinstance(kä, str) or not isinstance(ag, str):
            continue
        historia.append({"role": "user", "content": kä})
        historia.append({"role": "assistant", "content": ag})
    return historia


def lataa_kierrokset(polku: Path) -> list[dict[str, object]]:
    """Lukee tallennetut keskustelukierrokset; luo muisti-kansion tarvittaessa."""
    polku.parent.mkdir(parents=True, exist_ok=True)
    if not polku.is_file():
        return []
    try:
        raaka = polku.read_text(encoding="utf-8")
        data = json.loads(raaka)
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, dict):
        return []
    kierrokset = data.get("kierrokset")
    if not isinstance(kierrokset, list):
        return []
    return [k for k in kierrokset if isinstance(k, dict)]


def tallenna_kierrokset(polku: Path, kierrokset: list[dict[str, object]]) -> None:
    polku.parent.mkdir(parents=True, exist_ok=True)
    kierrokset = kierrokset[-_TIEDOSTO_MAX_KIERROKSET:]
    data = {
        "kierrokset": kierrokset,
        "viimeksi_paivitetty": datetime.now(timezone.utc).isoformat(),
    }
    try:
        polku.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as e:
        print(f"Varoitus: historian tallennus epäonnistui: {e}", file=sys.stderr)


def lue_viesti_agentille(rivi: str) -> tuple[str | None, str | None]:
    """
    Palauttaa (viestin_sisältö_APIlle, virheviesti).
    Jos rivi ei ole @tiedosto, palauttaa (rivi, None).
    """
    if not rivi.startswith("@"):
        return rivi, None

    tied_nimi = rivi[1:].strip()
    if not tied_nimi:
        return None, "Virhe: anna tiedostonimi @-merkin jälkeen (esim. @kysymys.txt)."

    kansi = _KANSIO.resolve()
    kohde = (_KANSIO / tied_nimi).resolve()
    if not kohde.is_relative_to(kansi):
        return None, f"Virhe: tiedosto ei ole kansiossa {_KANSIO}."

    if not kohde.is_file():
        return None, f"Virhe: tiedostoa ei löydy: {tied_nimi}"

    try:
        sisältö = kohde.read_text(encoding="utf-8")
    except OSError as e:
        return None, f"Virhe: tiedoston lukeminen epäonnistui ({e})."

    print(f"[Luettu tiedostosta: {kohde.name}]")
    print(sisältö)
    print()
    return sisältö, None


def main() -> None:
    järjestelmä = lue_järjestelmäkehote()
    asiakas = luo_asiakas()

    kierrokset = lataa_kierrokset(_HISTORIA_POLKU)
    if kierrokset:
        print("Muistin lataus onnistui — jatketaan edellisestä sessiosta")
        print()

    print("Jan core — kirjoita viesti. 'exit' tai 'lopeta' lopettaa.")
    while True:
        try:
            rivi = input("> ").strip()
        except EOFError:
            print()
            tallenna_kierrokset(_HISTORIA_POLKU, kierrokset)
            break

        if not rivi:
            continue

        if rivi.lower() in ("exit", "lopeta"):
            tallenna_kierrokset(_HISTORIA_POLKU, kierrokset)
            break

        viesti_sisältö, virhe = lue_viesti_agentille(rivi)
        if virhe is not None:
            print(virhe, file=sys.stderr)
            continue

        tausta = kierroksesta_historia(kierrokset)
        viestit = tausta + [{"role": "user", "content": viesti_sisältö}]

        try:
            vastaus_obj = asiakas.messages.create(
                model=MALLI,
                max_tokens=8192,
                system=järjestelmä,
                messages=viestit,
            )
        except Exception as e:
            print(f"API-virhe: {e}", file=sys.stderr)
            continue

        teksti = vastauksen_teksti(vastaus_obj)

        kierros = {
            "päivämäärä": datetime.now(timezone.utc).isoformat(),
            "käyttäjän_viesti": viesti_sisältö,
            "agentin_vastaus": teksti,
        }
        kierrokset.append(kierros)
        tallenna_kierrokset(_HISTORIA_POLKU, kierrokset)

        print(teksti)
        print()


if __name__ == "__main__":
    main()
