# Jan Anttilan AI-kehitysympäristö — Konteksti

## Käyttöohje
Liitä tämän tiedoston sisältö uuden Claude-session alkuun avainsanalla
#JANKONTEKSTI

---

## Henkilö
- Nimi: Jan Anttila
- Tausta: 37 vuotta pankkiuraa, lähes 30 vuotta johtotehtävissä
- Nykyrooli: Koko pankin Senior Advisor — eläköityy syksyllä 2026 (~5 kk)
- Nettotulot putoavat ~2000 €/kk eläkkeellä
- Vahvuudet: Finanssialan syvä osaaminen, johtamiskokemus, sijoittaminen, strateginen ajattelu
- Perhe: Poika hammaslääkäriyrittäjä, tytär AMK-opinnoissa, kaksi lastenlasta (Ukki)

### Tavoitteet
1. Paikata tulovaje sijoitusvarallisuudella
2. Rakentaa konsulttibisnes Senior Advisor -osaamisella
3. Kehittyä AI-kehittäjäksi ja hyödyntää sitä liiketoiminnassa

### Tärkein kysymys juuri nyt
Miten rakennan taloudellisen vapauden seuraavan 5 kk aikana
(ennen eläköitymistä syksyllä 2026)?

---

## Identiteetit (vain KAKSI tällä kehityskoneella)
- HENKILÖMINÄ: perhe, lastenlapset, harrastukset, henkilökohtainen elämä
- KEHITYSMINÄ: AI-kehitys, agenttiverkosto, syksyllä 2026 alkava yrittäjyys
- TYÖMINÄ asuu eri koneella — EI KOSKAAN tähän koneeseen
- Kehitysminän ympärille rakennetaan syksyllä 2026 yrittäjyys

---

## Sijoittajaprofiili (tärkeä — älä unohda)
- LUONTEELTAAN RISKINOTTAJA JA TUOTTOJEN JANOAJA
- 30 vuoden varainhoitokokemus, ei tarvitse defensiivistä profiilia
- Pitkä sijoitushorisontti (lastenlapset)
- Hyväksyy korkeamman volatiliteetin tavoitellessaan tuottoa
- Megatrendit (semiconductor, defence, AI) OK — ei pelkkää Health Carea/bondeja
- Claude EI saa olettaa defensiivistä profiilia automaattisesti vaikka eläköitymisestä puhutaan — kysy aina jos epävarma

---

## Kehitysympäristö
- Kone: Lenovo Yoga Slim 7 14Q8X9 (ARM64, Snapdragon)
- OS: Windows 11 — kehitystili: aicore-dev (ei koskaan pankkityöhön)
- Sähköposti: jandev2026@gmail.com
- GitHub: Jandev67
- Cursor Pro: jandev2026@gmail.com
- Git, Python 3.14.3 (ARM64), Node.js v24.14.1 (ARM64), Bitwarden

## Kansiorakenne
- C:\Dev\agentit\ — kaikki agentit ja promptit
- C:\Dev\projektit\ — koodiprojektit
- C:\Dev\muistiinpanot\ — kontekstitiedostot

---

## Cursorin nelitasoinen merkintä (Claude käyttää aina ohjeissaan)
- 🖥️ TERMINAL = PowerShell (lyhyet komennot, näkyy PS C:\Dev\...)
- 🤖 CURSOR EDITOR = pitkät tekstit ja tiedostosisällöt, ääkköset toimivat
- 🤖 CURSOR AGENT (vasen paneeli, Plan/Build) = itsenäinen, tallentaa heti, EI Accept-nappia, näyttää Review jälkikäteen
- 🤖 CURSOR CHAT (Ctrl+L) = diff-pohjainen, vaatii Acceptin

---

## Työtavat Clauden kanssa

### Vastuujako
- Claude OHJAA askel askeleelta — Jan TOTEUTAA
- Jan EI halua kirjoittaa /komentoja, #triggereitä eikä polkuja
- Jan haluaa puhua suomeksi yhdelle paikalle (tavoitteena Assari)
- Päätökset Janin puolesta — kysy vain isoista, älä joka pikkuasiasta

### Ohjeistuksen tarkkuus (Claude antaa AINA)
- Tarkka polku ja askelmat
- Esim. "Avaa Cursor → File Explorer → navigoi C:\Dev\agentit\ → klikkaa..."
- Esim. "Liimaa tämä 🤖 CURSOR AGENT -kenttään, paina Enter, hyväksy Run"
- Ei oletuksia siitä mitä Jan jo tietää käyttöliittymästä
- Käytä yllä olevia merkintöjä joista Jan tietää kumpaan kirjoittaa

### Cursorin Review-nappi (sääntö)
- ÄLÄ klikkaa Reviewia, Acceptia tai Pushia kunnes Claude on YHDESSÄ Janin kanssa päättänyt
- Claude tarkistaa diffin ennen hyväksyntää
- Jos epävarma: kysy ennen kuin painat

### Conversation_search ennen suosituksia
- Claude käyttää conversation_search-toolia ENNEN toimenpidesuosituksia, kun aihe koskee kehitysympäristöä, agenttiverkostoa, salkkua tai aiemmin sovittuja toimintatapoja
- Erityisesti jos Jan viittaa sanoihin "eilen", "aiemmin", "viime kerralla", "edellisessä sessiossa" — search ensin, suositus vasta sitten

### Istuntohallinta (~70 % kapasiteetista)
Claude seuraa keskustelun pituutta ja antaa Janille hyvissä ajoin (EI viime tipassa) signaalin kontrolloidusta siirtymästä uudelle välilehdelle.

Siirtymäpaketti sisältää KOLME komponenttia:
1. Päivitysehdotus jan_konteksti.md:hen (uudet asiat sessiosta)
2. Session keskeiset lopputulemat (mitä saatiin valmiiksi, mitä jäi kesken)
3. Valmis copy-paste-aloitussanoitus uudelle välilehdelle #JANKONTEKSTI-triggerillä ja lyhyellä tilannekatsauksella

Jan ei muista komentoja — Claude hoitaa saumakohdan kokonaan.

---

## Agenttiverkosto — tavoitetila

### Ydinajatus
Assari on portinvartija jolle Jan kirjoittaa kaikki asiat aihealueesta riippumatta. Assari tunnistaa aiheen ja ohjaa oikealle erikoisagentille.
Erikoisagentit ovat AGENTIN kutsumia työkaluja, eivät erillisiä skriptejä joita Jan käynnistää itse.

### Taso 1 — Ydinagentti
- Jan-Core: alter ego, strateginen kumppani, tuntee Janin syvällisesti

### Taso 2 — Asiantuntija-agentit (15 kpl) ja heidän lähteensä
- Sijoitus: kauppalehti.fi, talouselama.fi, investing.com, inderes.fi, nordnet.fi, morningstar.com, yahoo finance, tradingview.com
- Juristi: finlex.fi, oikeus.fi, vero.fi, edilex.fi, KHO.fi, KKO.fi
- Strategia: tulevaisuusajattelu, yrittäjyyspolku
- Liiketoiminta: konsulttibisneksen rakentaminen
- EU-juridiikka: regulaatio, direktiivit
- Vero FI/kv: verosuunnittelu
- Sääntely: finanssiala, compliance
- Markkinointi: konsulttibrändi
- Viestintä: tekstit, esitykset
- Pedagogia: osaamisen siirtäminen
- Hallinto: yrityksen pyörittäminen
- Talousanalyysi: tilinpäätökset, due diligence
- Muutosjohtaminen: organisaatiomuutokset
- Verkosto: referenssit, kumppanuudet
- Raportointi: asiakasraportit, esitykset

### Taso 3 — Tukiagentit
- Assari (portinvartija), Tietoturva, Laatu

### Vaatimukset jokaiselle agentille
- Käyttää omia luotettavia lähteitään, ei hallusinoi
- Muistaa aiemmat sessiot
- Tukee @tiedosto.txt pitkille viesteille

### Isompi tavoite
Agenttiverkosto tukee Jania taloudellisen vapauden rakentamisessa:
- 2000 €/kk tulovajeen paikkaaminen sijoituksilla
- Konsulttibisneksen rakentaminen ennen eläköitymistä syksyllä 2026

---

## NYKYTILANNE 16.5.2026

### TOIMII ✅
- sijoitusagentti_v3.py — Jankontekstin mukainen, lataa AUTOMAATTISESTI salkku_konteksti.md, sijoitus_prompt.txt JA op_etf_valikoima.md.
  Käynnistys: 🖥️ TERMINAL → cd C:\Dev\agentit && python sijoitusagentti_v3.py
- salkku_konteksti.md — täydellinen, ajantasainen (Neste-myynti mukana)
- sijoitus_prompt.txt — 5846 merkkiä, päivitetty 20.4.2026
- juristi_prompt.txt — Oral-tapaus mukana
- Kontekstien lataus testattu (3.5.2026): kolme ✓-riviä toimii (Sijoitus-prompt 5462 mrk, Salkkukonteksti 3077 mrk, ETF-valikoima 21733 mrk)
- UTF-8 toimii Windowsin oletuskonsolissa kaikissa agenteissa

### VALMIIT (3.5.2026)
- ETF-valikoima rakennettu OP:n koko 940 ETF/ETP-listasta:
  - op_etf_kaikki.csv (koko data, varakopio)
  - op_etf_valikoima.md (144 ETF:n suodatettu shortlist 13 kategoriassa)
  - Pois suodatettu: vipu, inverssi, kapeat hyödykkeet, kryptot, sektori-Eurooppa
- Sijoitusagentti_v3.py päivitetty lataamaan ETF-valikoima automaattisesti (uusi vakio ETF_VALIKOIMA_TIEDOSTO + uusi if-lohko lataa_konteksti()-funktiossa)
- UTF-8-korjaus tehty kolmeen tiedostoon (sijoitusagentti_v3.py, sijoitus_agentti.py, web_search_uusi.py): sys.stdout.reconfigure(encoding="utf-8")
- Git-commit 5baff10 sisältää koko 3.5.2026 työn

### VALMIIT (5.5.2026 iltapäivä)
- Juristi-agentin tiedostoviittaukset KORJATTU
  (juristi_agentti.py): aiemmin viittasi vahingossa Assariin
  (assari_prompt.txt + assari_historia.json), nyt viittaa oikein:
  - _PROMPT_POLKU = _KANSIO / "juristi_prompt.txt"
  - _HISTORIA_POLKU = _MUISTI_KANSIO / "juristi_historia.json"
  - Tervehtii nyt "Juristi" eikä "Assari"
  - Vanha keskusteluhistoria kopioitu uuteen
    juristi_historia.json -tiedostoon (ei menetetty)
- AVI-pöytäkirja 4.6.2021 lisätty pysyvästi juristi_prompt.txt:hen.
  Agentti tietää nyt automaattisesti:
  - Tarkastaja Kauno Salminen (AVI:n valtuuttama tarkastaja,
    Kalajoen kaupungin terveyspalvelujohtaja)
  - Osallistujat: Valtteri Anttila, Kauno Salminen, EHL Tuomo
    Heikkinen
  - Sisältö: ilmanvaihto määräysten mukainen, ei huomautettavaa,
    huomautuskenttä tyhjä
  - Neljä kumottua Oralin argumenttia: virheellinen ilmanvaihto,
    pintapuolinen tarkastus, SUP 1 -pakollisuus, myyjän tietoisuus
  - Kauppaoikeudellinen merkitys ja vasta-argumentit Oralin
    mahdollisiin vastauksiin (skenaariot A, B, C)
- jan_konteksti.md päivitetty täysin (henkilö, identiteetit,
  riskinottoprofiili, työtavat, agenttiverkosto, ETF-päätös,
  salkku, Cursorin nelitasoinen merkintä)
- Claude-pitkäkestoinen muisti siivottu — projektidata siirretty
  jan_konteksti.md:hen, muistissa vain työtaparyhmät
  (Cursor-merkinnät, editori vs terminaali, istuntohallinta,
  conversation_search-sääntö)

### VALMIIT (10.5.2026)
- ✅ GitHub-push autentikointi valmis — PAT-token Bitwardenissa
  ("GitHub PAT token - agentit"), .gitignore suojattu
- ✅ assari_v2.py — semanttinen JSON-reititys käytössä
  Ei avainsanoja — lataa kuvaukset/ kansiosta automaattisesti
  Rakenne: `{"pääagentti": "x", "tukiagentit": ["y"]}`
- ✅ kuvaukset/-kansio luotu: sijoitus_kuvaus.txt,
  juristi_kuvaus.txt, assari_kuvaus.txt
  Uusi agentti = uusi kuvaus.txt, ei koodimuutoksia
- ✅ Juristi päivitetty kahdella tiedolla:
  — oral_sisailma_uusi_tieto.md (siivousfirman kausaliteettikatko)
  — juristi_tapaus_oral.md (Oral kokonaistilannekuva)
- ✅ Testattu ja toimii:
  — Neste → Sijoitusagentti ✅
  — Oral-tapaus → Juristi ✅

### KAIKKI 15 AGENTTIA VALMIIT (16.5.2026)
Strategia, Talousanalyysi, Liiketoiminta, Vero,
EU-juridiikka, Sääntely, Hallinto, Markkinointi,
Viestintä, Verkosto, Muutosjohtaminen, Pedagogia,
Raportointi + Sijoitus + Juristi

### ETF-PÄÄTÖS 5.5.2026 (lukittu, EI VIELÄ TOIMEKSIANTOA)
30 000 € OST-allokaatio (Neste-myynti 11 800 € + aiempi käteinen ~18 000 €):
- VWCE — Vanguard FTSE All-World UCITS ETF Acc — 15 000 € (50 %) — IE00BK5BQT80
- IS3N — iShares Core MSCI EM IMI UCITS ETF — 9 000 € (30 %) — IE00BKM4GZ66
- ASWC — HANetf Future of Defence UCITS ETF — 6 000 € (20 %) — IE000OJ5TQP4

Kokonais-TER ~0,25 %, vuosittaiset kulut ~75 €.
Päätös syntyi sijoitusagentin + Claude-synteesin kautta kahden kierroksen kautta, riskinottoprofiili huomioiden.

### ORAL-AINEISTO 5.5.2026 (valmis kokonaisanalyysiin)
Sijainti: C:\Dev\agentit\oral_tapaus\liitteet\oral_tapaus_kansio\

Sisältö:
- Kauppakirja
- Vuokrasopimus
- AVI-pöytäkirja 4.6.2021 (käyttöönottotarkastus)
- Reklamaatio 1 (16.1.2026)
- Vastine 1 (30.1.2026)
- Reklamaatio 2 (25.2.2026)
- Vastine 2 (18.3.2026)
- Koneiden huoltohistoria

Kokonaisanalyysi siirtyy uudelle välilehdelle: vahvuudet,
heikkoudet, todennäköiset Oralin seuraavat liikkeet, strateginen
suositus.

### SEURAAVAT VAIHEET
1. Testaa Assari kaikilla uusilla agenteilla
2. Rakenna moniagenttisynteesin Assariin
3. ETF-toimeksiannot OP:hen (päätös lukittu)
4. Tietoturva- ja Laatu-tukiagentit
5. ORAL-tapauksen kokonaisanalyysi juristi-agentilla —
   ydintehtävä uudella välilehdellä
6. Sähköposti Valtterille AVI-pöytäkirjan merkityksestä
   (voidaan tehdä Oral-analyysin jälkeen jolloin pohja on laajempi)
7. Myöhemmin: webkäyttöliittymä (selain + puhe), sessio-välinen muisti, konsulttibisneksen valmistelu

---

## SALKKU 30.4.2026 — KOKONAISTILANNE 460 700 €
- OST: 113 834 € (15 positiota) — Neste-myynnin jälkeen ~11 800 € käteistä
- Sijoitusvakuutus: 208 055 € — vaihdot tehty 20.4.2026
- Eläkevakuutus: 92 791 € — nostovaihe alkaa 31.5.2027
- Vapaat rahastot: 16 128 €
- Käteinen: 29 892 € (ennen ETF-päätöstä — 30 000 € siirtyy ETF-allokaatioon)

### OST top 5 Neste-myynnin jälkeen
1. Nordea: 22 445 € (suurin)
2. Neste: ~21 100 € (myyty 400 kpl @ 29,50 € — 29.4.2026)
3. Mandatum: 13 509 €
4. Nokia: 8 667 €
5. Fortum: 6 427 €

### Joulukisa 🎄
Kreate (149 €), Afarak (47 €), Revenio (32 €) — perheen tuottokisa, EI MYYDÄ ennen 24.12.2026.

---

## LEPÄÄ (vanhoja, ei aktiivisesti käytössä) 🟡
- sijoitus_agentti.py (vanha versio, korvattu v3:lla)
- jan_core.py, juristi_agentti.py, finanssi_strategia_agentti.py, tulevaisuus_strategia_agentti.py, web_search.py, web_search_uusi.py (ovat olemassa mutta odottavat aktivoimista Assari-reitityksessä)
- assari.py (ei vielä portinvartijana toimiva)

---

## TÄRKEÄT OPETUKSET (älä unohda)
- Jan EI halua kirjoittaa /komentoja, #triggereitä tai polkuja
- Jan haluaa puhua suomeksi yhdelle paikalle (tavoitteena Assari)
- Erikoisagentit ovat AGENTIN kutsumia työkaluja, eivät erillisiä skriptejä joita Jan käynnistää itse
- "Kehitysympäristö valmis" = toimivat agentit; kaikki 15 Taso 2 -agenttia valmiit 16.5.2026
- Pidä keskustelumaksimi mielessä, tee siirtymä hyvissä ajoin
- Päätökset Janin puolesta — kysy vain isoista, älä joka pikkuasiasta
- Riskinottajaprofiili — älä oleta defensiivistä vaikka eläköitymisestä puhutaan
- Käytä conversation_search ennen suosituksia kun aihe koskee aiempia sopimuksia
- Cursorissa Review-nappi: ÄLÄ klikkaa kunnes yhdessä päätetty
