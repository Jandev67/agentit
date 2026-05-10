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
_MUISTI_KANSIO = _KANSIO / "muisti"
_KUVAUKSET_KANSIO = _KANSIO / "kuvaukset"
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

AGENTTI_TIEDOSTOT = {
    "sijoitus": ("sijoitus_prompt.txt", "sijoitus_historia.json", "Sijoitusagentti"),
    "juristi":  ("juristi_prompt.txt",  "juristi_historia.json",  "Juristi"),
    "assari":   ("assari_prompt.txt",   "assari_historia.json",   "Assari"),
}


def luo_asiakas() -> Anthropic:
    avain = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not avain:
        print("Virhe: ANTHROPIC_API_KEY puuttuu.", file=sys.stderr)
        sys.exit(1)
    return Anthropic(api_key=avain)


def lataa_kuvaukset() -> str:
    if not _KUVAUKSET_KANSIO.is_dir():
        return ""
    kuvaukset = []
    for tiedosto in sorted(_KUVAUKSET_KANSIO.glob("*_kuvaus.txt")):
        teksti = tiedosto.read_text(encoding="utf-8").strip()
        kuvaukset.append(teksti)
    return "\n\n---\n\n".join(kuvaukset)


def reititys_prompt(kuvaukset_teksti: str) -> str:
    return f"""Olet reititysagentti. Sinulle annetaan käyttäjän viesti ja lista käytettävissä olevista agenteista.

Tehtäväsi: Päätä mikä agentti on PÄÄAGENTTI ja mitkä ovat tarvittavat TUKIAGENTIT.

KÄYTETTÄVISSÄ OLEVAT AGENTIT:
{kuvaukset_teksti}

Vastaa AINOASTAAN JSON-muodossa, ei muuta tekstiä:
{{"pääagentti": "agentti_nimi", "tukiagentit": ["agentti_nimi2"]}}

Agentti_nimi on aina pienillä kirjaimilla: sijoitus, juristi tai assari.
Jos tukiagentteja ei tarvita, käytä tyhjää listaa: []
Jos sopivaa agenttia ei löydy, käytä "assari"."""


def luokittele_reititys(asiakas: Anthropic, viesti: str, kuvaukset_teksti: str) -> dict:
    try:
        vastaus = asiakas.messages.create(
            model=MALLI,
            max_tokens=100,
            system=reititys_prompt(kuvaukset_teksti),
            messages=[{"role": "user", "content": viesti}],
        )
        teksti = vastaus.content[0].text.strip()
        data = json.loads(teksti)
        pää = data.get("pääagentti", "assari").lower()
        tuki = [a.lower() for a in data.get("tukiagentit", []) if isinstance(a, str)]
        if pää not in AGENTTI_TIEDOSTOT:
            pää = "assari"
        tuki = [a for a in tuki if a in AGENTTI_TIEDOSTOT and a != pää]
        return {"pääagentti": pää, "tukiagentit": tuki}
    except Exception:
        return {"pääagentti": "assari", "tukiagentit": []}


def lue_prompt(tiedosto: str) -> str:
    polku = _KANSIO / tiedosto
    if not polku.is_file():
        return ""
    return polku.read_text(encoding="utf-8").strip()


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


def lataa_kierrokset(historia_tiedosto: str):
    polku = _MUISTI_KANSIO / historia_tiedosto
    polku.parent.mkdir(parents=True, exist_ok=True)
    if not polku.is_file():
        return []
    try:
        data = json.loads(polku.read_text(encoding="utf-8"))
        return [k for k in data.get("kierrokset", []) if isinstance(k, dict)]
    except Exception:
        return []


def tallenna_kierrokset(historia_tiedosto: str, kierrokset):
    polku = _MUISTI_KANSIO / historia_tiedosto
    polku.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "kierrokset": kierrokset[-_TIEDOSTO_MAX_KIERROKSET:],
        "viimeksi_paivitetty": datetime.now(timezone.utc).isoformat(),
    }
    try:
        polku.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as e:
        print(f"Varoitus: tallennus epäonnistui: {e}", file=sys.stderr)


def kysy_agentilta(asiakas: Anthropic, agentti_id: str, sisalto: str) -> str:
    if agentti_id not in AGENTTI_TIEDOSTOT:
        return ""
    prompt_tiedosto, historia_tiedosto, _ = AGENTTI_TIEDOSTOT[agentti_id]
    jarjestelma = lue_prompt(prompt_tiedosto)
    if not jarjestelma:
        return ""
    kierrokset = lataa_kierrokset(historia_tiedosto)
    viestit = kierroksesta_historia(kierrokset) + [{"role": "user", "content": sisalto}]
    try:
        vastaus_obj = asiakas.messages.create(
            model=MALLI,
            max_tokens=8192,
            system=jarjestelma,
            messages=viestit,
        )
        teksti = vastauksen_teksti(vastaus_obj)
        kierrokset.append({
            "paivays": datetime.now(timezone.utc).isoformat(),
            "kayttajan_viesti": sisalto,
            "agentin_vastaus": teksti,
        })
        tallenna_kierrokset(historia_tiedosto, kierrokset)
        return teksti
    except Exception as e:
        print(f"API-virhe ({agentti_id}): {e}", file=sys.stderr)
        return ""


def lue_tiedosto(rivi: str):
    if not rivi.startswith("@"):
        return rivi, None
    nimi = rivi[1:].strip()
    polku = (_KANSIO / nimi).resolve()
    if not polku.is_relative_to(_KANSIO):
        return None, "Virhe: tiedosto kansion ulkopuolella."
    if not polku.is_file():
        return None, f"Virhe: tiedostoa ei löydy: {nimi}"
    return polku.read_text(encoding="utf-8").strip(), None


def main() -> None:
    asiakas = luo_asiakas()
    kuvaukset_teksti = lataa_kuvaukset()
    print("Assari — kirjoita viesti. 'exit' tai 'lopeta' lopettaa.")
    print()

    while True:
        try:
            rivi = input("> ").strip()
        except EOFError:
            break
        if not rivi:
            continue
        if rivi.lower() in ("exit", "lopeta"):
            break

        sisalto, virhe = lue_tiedosto(rivi)
        if virhe:
            print(virhe)
            continue
        if rivi.startswith("@"):
            print(f"[Luettu tiedostosta: {rivi[1:].strip()}]")

        reititys = luokittele_reititys(asiakas, sisalto, kuvaukset_teksti)
        pää = reititys["pääagentti"]
        tuki = reititys["tukiagentit"]

        _, _, pää_nimi = AGENTTI_TIEDOSTOT[pää]
        tuki_nimet = [AGENTTI_TIEDOSTOT[a][2] for a in tuki if a in AGENTTI_TIEDOSTOT]

        if tuki_nimet:
            print(f"[→ {pää_nimi} + {', '.join(tuki_nimet)}]")
        else:
            print(f"[→ {pää_nimi}]")

        pää_vastaus = kysy_agentilta(asiakas, pää, sisalto)

        tuki_vastaukset = []
        for tuki_id in tuki:
            prompt_tiedosto = AGENTTI_TIEDOSTOT[tuki_id][0]
            if (_KANSIO / prompt_tiedosto).is_file():
                tv = kysy_agentilta(asiakas, tuki_id, sisalto)
                if tv:
                    tn = AGENTTI_TIEDOSTOT[tuki_id][2]
                    tuki_vastaukset.append(f"---\n**{tn}:**\n{tv}")

        print(pää_vastaus)
        for tv in tuki_vastaukset:
            print(tv)
        print()


if __name__ == "__main__":
    main()
