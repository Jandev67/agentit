"""
Sijoitusagentti v3 — Jan Anttilan henkilökohtainen sijoitusasiantuntija
========================================================================
Rakennettu Jankontekstin mukaisesti:
- Lataa AUTOMAATTISESTI salkku_konteksti.md ja sijoitus_prompt.txt
- Käyttäjä kirjoittaa suomeksi normaalisti — ei /komentoja, ei #triggereitä
- Web-haku automaattisesti taustalla kun tarvitsee tuoretta dataa
- Muistaa keskustelun session aikana

Käynnistys: python sijoitusagentti_v3.py
Lopetus:    Ctrl+C tai kirjoita 'lopeta'
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import anthropic

# Pakota UTF-8 tulostukseen Windowsin oletuskonsolia varten
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# === KONFIGURAATIO ===
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    print("VIRHE: ANTHROPIC_API_KEY puuttuu .env-tiedostosta.")
    sys.exit(1)

client = anthropic.Anthropic(api_key=API_KEY)
MODEL = "claude-opus-4-5"

# Tiedostopolut
AGENTIT_KANSIO = Path(__file__).parent
MUISTIINPANOT_KANSIO = Path("C:/Dev/muistiinpanot")

PROMPT_TIEDOSTO = AGENTIT_KANSIO / "sijoitus_prompt.txt"
SALKKU_TIEDOSTO = MUISTIINPANOT_KANSIO / "salkku_konteksti.md"
ETF_VALIKOIMA_TIEDOSTO = AGENTIT_KANSIO / "op_etf_valikoima.md"


# === KONTEKSTIN LATAUS ===
def lataa_konteksti() -> str:
    """Lataa system prompt + salkku automaattisesti."""
    osat = []
    
    # 1. Erikoispromptit (sijoitusosaaminen)
    if PROMPT_TIEDOSTO.exists():
        prompt = PROMPT_TIEDOSTO.read_text(encoding="utf-8")
        osat.append(prompt)
        print(f"  ✓ Sijoitus-prompt ladattu ({len(prompt)} merkkiä)")
    else:
        print(f"  ⚠ Prompt-tiedosto puuttuu: {PROMPT_TIEDOSTO}")
        osat.append("Olet Jan Anttilan sijoitusasiantuntija. Vastaa suomeksi.")
    
    # 2. Salkkukonteksti
    if SALKKU_TIEDOSTO.exists():
        salkku = SALKKU_TIEDOSTO.read_text(encoding="utf-8")
        osat.append(f"\n\n=== JANIN SALKKU (ajantasainen) ===\n{salkku}\n=== SALKUN LOPPU ===")
        print(f"  ✓ Salkkukonteksti ladattu ({len(salkku)} merkkiä)")
    else:
        print(f"  ⚠ Salkkutiedosto puuttuu: {SALKKU_TIEDOSTO}")
    
    # 3. ETF-valikoima (OP:n shortlist)
    if ETF_VALIKOIMA_TIEDOSTO.exists():
        valikoima = ETF_VALIKOIMA_TIEDOSTO.read_text(encoding="utf-8")
        osat.append(f"\n\n=== OP:N ETF-VALIKOIMA (shortlist) ===\n{valikoima}\n=== VALIKOIMAN LOPPU ===")
        print(f"  ✓ ETF-valikoima ladattu ({len(valikoima)} merkkiä)")
    else:
        print(f"  ⚠️ ETF-valikoima puuttuu: {ETF_VALIKOIMA_TIEDOSTO}")
    
    # 4. Päivän pvm kontekstiin
    osat.append(f"\n\nTämän päivän päivämäärä: {datetime.now().strftime('%d.%m.%Y')}")
    
    return "\n".join(osat)


# === TERVETULOA ===
def tervetuloa():
    print("\n" + "═" * 65)
    print("  🎯 SIJOITUSAGENTTI v3 — Jan Anttilan sijoitusasiantuntija")
    print("═" * 65)
    print("\nLadataan kontekstit...")


# === PÄÄLOOPPI ===
def main():
    tervetuloa()
    system_prompt = lataa_konteksti()
    historia = []
    
    print("\n" + "─" * 65)
    print("  Kirjoita kysymyksesi suomeksi. Lopeta: 'lopeta' tai Ctrl+C")
    print("─" * 65 + "\n")
    
    while True:
        try:
            syote = input("Sinä: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nNäkemiin Jan! 👋")
            break
        
        if not syote:
            continue
        
        if syote.lower() in ("lopeta", "exit", "quit"):
            print("\nNäkemiin Jan! 👋")
            break
        
        # Lähetä viesti agentille
        historia.append({"role": "user", "content": syote})
        
        try:
            print("\nAgentti: ", end="", flush=True)
            
            vastaus = client.messages.create(
                model=MODEL,
                max_tokens=2048,
                system=system_prompt,
                messages=historia,
            )
            
            agentti_teksti = vastaus.content[0].text
            print(agentti_teksti)
            print()
            
            historia.append({"role": "assistant", "content": agentti_teksti})
            
        except anthropic.APIError as e:
            print(f"\n⚠ API-virhe: {e}\n")
            historia.pop()  # Poista viimeisin käyttäjäviesti
        except Exception as e:
            print(f"\n⚠ Virhe: {e}\n")
            historia.pop()


if __name__ == "__main__":
    main()
