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
_PROMPT_POLKU = _KANSIO / "juristi_prompt.txt"
_MUISTI_KANSIO = _KANSIO / "muisti"
_HISTORIA_POLKU = _MUISTI_KANSIO / "juristi_historia.json"
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

def lue_jarjestelma() -> str:
    if not _PROMPT_POLKU.is_file():
        print(f"Virhe: {_PROMPT_POLKU} puuttuu.", file=sys.stderr)
        sys.exit(1)
    return _PROMPT_POLKU.read_text(encoding="utf-8").strip()

def luo_asiakas() -> Anthropic:
    avain = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not avain:
        print("Virhe: ANTHROPIC_API_KEY puuttuu.", file=sys.stderr)
        sys.exit(1)
    return Anthropic(api_key=avain)

def vastauksen_teksti(viesti: object) -> str:
    return "".join(b.text for b in viesti.content if hasattr(b, "text"))

def kierroksesta_historia(kierrokset):
    historia = []
    for k in kierrokset[-_API_MAX_KIERROKSET:]:
        if not isinstance(k, dict):
            continue
        ka = k.get("kayttajan_viesti")
        ag = k.get("agentin_vastaus")
        if isinstance(ka, str) and isinstance(ag, str):
            historia.append({"role": "user", "content": ka})
            historia.append({"role": "assistant", "content": ag})
    return historia

def lataa_kierrokset(polku: Path):
    polku.parent.mkdir(parents=True, exist_ok=True)
    if not polku.is_file():
        return []
    try:
        data = json.loads(polku.read_text(encoding="utf-8"))
        return [k for k in data.get("kierrokset", []) if isinstance(k, dict)]
    except Exception:
        return []

def tallenna_kierrokset(polku: Path, kierrokset):
    polku.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "kierrokset": kierrokset[-_TIEDOSTO_MAX_KIERROKSET:],
        "viimeksi_paivitetty": datetime.now(timezone.utc).isoformat(),
    }
    try:
        polku.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as e:
        print(f"Varoitus: tallennus epaonnistui: {e}", file=sys.stderr)

def lue_tiedosto(rivi: str):
    if not rivi.startswith("@"):
        return rivi, None
    nimi = rivi[1:].strip()
    polku = (_KANSIO / nimi).resolve()
    if not polku.is_relative_to(_KANSIO):
        return None, f"Virhe: tiedosto kansion ulkopuolella."
    if not polku.is_file():
        return None, f"Virhe: tiedostoa ei loydy: {nimi}"
    return polku.read_text(encoding="utf-8").strip(), None

def main() -> None:
    jarjestelma = lue_jarjestelma()
    asiakas = luo_asiakas()
    kierrokset = lataa_kierrokset(_HISTORIA_POLKU)
    if kierrokset:
        print("Muistin lataus onnistui — jatketaan edellisestä sessiosta")
        print()
    print("Juristi — kirjoita viesti. 'exit' tai 'lopeta' lopettaa.")
    while True:
        try:
            rivi = input("> ").strip()
        except EOFError:
            tallenna_kierrokset(_HISTORIA_POLKU, kierrokset)
            break
        if not rivi:
            continue
        if rivi.lower() in ("exit", "lopeta"):
            tallenna_kierrokset(_HISTORIA_POLKU, kierrokset)
            break
        sisalto, virhe = lue_tiedosto(rivi)
        if virhe:
            print(virhe)
            continue
        if rivi.startswith("@"):
            print(f"[Luettu tiedostosta: {rivi[1:].strip()}]")
        viestit = kierroksesta_historia(kierrokset) + [{"role": "user", "content": sisalto}]
        try:
            vastaus_obj = asiakas.messages.create(
                model=MALLI,
                max_tokens=8192,
                system=jarjestelma,
                messages=viestit,
            )
        except Exception as e:
            print(f"API-virhe: {e}", file=sys.stderr)
            continue
        teksti = vastauksen_teksti(vastaus_obj)
        kierrokset.append({
            "paivays": datetime.now(timezone.utc).isoformat(),
            "kayttajan_viesti": sisalto,
            "agentin_vastaus": teksti,
        })
        tallenna_kierrokset(_HISTORIA_POLKU, kierrokset)
        print(teksti)
        print()

if __name__ == "__main__":
    main()
