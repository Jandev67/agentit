"""
sijoitus_agentti.py — Sijoitusagentti web-haulla
=================================================
Versio 2.0: Lisätty web-hakutoiminto priorisoiduilla
suomalaisilla talouslähteillä.

Komennot chatissa:
  /hae <hakutermi>       — hakee uutiset ja syöttää agentille
  /hae+ <hakutermi>      — hae ja kysy heti agentilta analyysi
  /lahteet               — näytä prioriteettilähteet
  /tyhjenna              — tyhjennä keskusteluhistoria
  /lopeta                — poistu

Muuten: kirjoita normaalisti, agentti vastaa.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import anthropic

# Pakota UTF-8 tulostukseen Windowsin oletuskonsolia varten
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Web-hakumoduuli (samassa kansiossa)
try:
    from web_search import hae_ja_muodosta_konteksti, LAHDE_PRIORITEETTI
    WEB_HAKU_KAYTOSSA = True
except ImportError:
    print("⚠️  web_search.py ei löydy — web-haku ei käytössä.")
    WEB_HAKU_KAYTOSSA = False

# ---------------------------------------------------------------------------
# Konfiguraatio
# ---------------------------------------------------------------------------

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    print("VIRHE: ANTHROPIC_API_KEY puuttuu .env-tiedostosta.")
    sys.exit(1)

client = anthropic.Anthropic(api_key=API_KEY)
MODEL = "claude-opus-4-5"

# System prompt -tiedosto
PROMPT_TIEDOSTO = Path(__file__).parent / "sijoitus_agentti_prompt.txt"

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

def lataa_system_prompt() -> str:
    if PROMPT_TIEDOSTO.exists():
        teksti = PROMPT_TIEDOSTO.read_text(encoding="utf-8").strip()
        if teksti:
            return teksti
    # Oletusprompt jos tiedostoa ei ole
    return """Olet Sijoitusagentti, Jan Anttilan henkilökohtainen sijoitusanalyytikko.

Jan on kokenut pankkialan ammattilainen ja koulutettu ekonomisti, joka tunne talouden 
peruskäsitteet erinomaisesti. Hän siirtyy eläkkeelle syksyllä 2026 ja tavoittelee 
sijoituksilla ~2 000 €/kk nettotulojen korvaamista.

Tehtäväsi:
- Analysoi sijoituksia, osakkeita ja markkinoita itsenäisesti
- Esitä konkreettisia näkemyksiä ja suosituksia — älä pelkästään toista päätöksiä
- Hyödynnä web-hakutulokset kun ne syötetään sinulle
- Käytä ammatillista mutta suoraviivaista kieltä
- Viittaa lähteisiin nimeltä kun käytät hakutuloksia

Salkun avainpositiot: Neste (~30% suorista osakkeista), finanssiala (~47k€).
Sijoitusvakuutus on verotehokasta — voit suositella vapaasti sisäisiä vaihtoja."""

# ---------------------------------------------------------------------------
# Apufunktiot
# ---------------------------------------------------------------------------

def tulosta_tervetuloa():
    print("\n" + "═" * 60)
    print("  SIJOITUSAGENTTI v2.0")
    if WEB_HAKU_KAYTOSSA:
        print("  ✓ Web-haku käytössä")
    print("  Kirjoita /hae <termi> tai kysy suoraan")
    print("═" * 60 + "\n")


def kasittele_komento(syote: str, historia: list) -> tuple[bool, str]:
    """
    Käsittelee /-komennot.
    Palauttaa (jatka_looppia, mahdollinen_lisaviesti_agentille).
    """
    osa = syote.strip().split(maxsplit=1)
    komento = osa[0].lower()
    argumentti = osa[1].strip() if len(osa) > 1 else ""

    if komento == "/lopeta":
        print("\nNäkemiin!")
        sys.exit(0)

    elif komento == "/tyhjenna":
        historia.clear()
        print("✓ Keskusteluhistoria tyhjennetty.\n")
        return True, ""

    elif komento == "/lahteet":
        print("\nPrioriteettilähteet:")
        for lahde, prioriteetti in sorted(LAHDE_PRIORITEETTI.items(), key=lambda x: x[1]):
            print(f"  {prioriteetti}. {lahde}")
        print()
        return True, ""

    elif komento in ("/hae", "/hae+") and WEB_HAKU_KAYTOSSA:
        if not argumentti:
            print("Anna hakutermi: /hae <termi>\n")
            return True, ""

        print(f"\n🔍 Haetaan: '{argumentti}' ...")
        konteksti = hae_ja_muodosta_konteksti(argumentti, max_tuloksia=4)
        print(f"✓ Hakutulokset haettu.\n")

        if komento == "/hae":
            # Näytä tulokset, ei automaattista analyysipyyntöä
            print(konteksti[:2000] + ("..." if len(konteksti) > 2000 else ""))
            print()
            # Lisää historiaan kontekstina
            historia.append({
                "role": "user",
                "content": f"Tässä web-hakutulokset termille '{argumentti}':\n\n{konteksti}"
            })
            historia.append({
                "role": "assistant",
                "content": f"Olen saanut hakutulokset aiheesta '{argumentti}'. "
                           "Voit nyt kysyä analyysiani tai lisäkysymyksiä."
            })
            return True, ""

        else:  # /hae+
            # Hae + kysy automaattisesti analyysi
            yhdistetty = (
                f"Tässä web-hakutulokset termille '{argumentti}':\n\n{konteksti}\n\n"
                f"Analysoi nämä tiedot sijoitusnäkökulmasta. "
                f"Mitä tämä tarkoittaa salkulleni?"
            )
            return False, yhdistetty

    elif komento in ("/hae", "/hae+") and not WEB_HAKU_KAYTOSSA:
        print("⚠️  Web-haku ei ole käytössä (web_search.py puuttuu).\n")
        return True, ""

    else:
        print(f"Tuntematon komento: {komento}\n")
        return True, ""


def kysy_agentilta(viesti: str, historia: list, system_prompt: str) -> str:
    """Lähettää viestin agentille ja palauttaa vastauksen."""
    historia.append({"role": "user", "content": viesti})

    vastaus = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system_prompt,
        messages=historia,
    )

    agentti_vastaus = vastaus.content[0].text
    historia.append({"role": "assistant", "content": agentti_vastaus})
    return agentti_vastaus


# ---------------------------------------------------------------------------
# Päälooppi
# ---------------------------------------------------------------------------

def main():
    tulosta_tervetuloa()
    system_prompt = lataa_system_prompt()
    historia: list[dict] = []

    while True:
        try:
            syote = input("Sinä: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nNäkemiin!")
            break

        if not syote:
            continue

        # Komento?
        if syote.startswith("/"):
            jatka, lisaviesti = kasittele_komento(syote, historia)
            if jatka:
                continue
            # /hae+ palauttaa lisäviestin joka menee agentille
            syote = lisaviesti

        # Kysy agentilta
        print("\nAgentti: ", end="", flush=True)
        try:
            vastaus = kysy_agentilta(syote, historia, system_prompt)
            print(vastaus)
            print()
        except anthropic.APIError as e:
            print(f"\n⚠️  API-virhe: {e}\n")
        except Exception as e:
            print(f"\n⚠️  Virhe: {e}\n")


if __name__ == "__main__":
    main()
