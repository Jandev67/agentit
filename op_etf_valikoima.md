# OP:n ETF-valikoima — relevanttien shortlist

**Päivitetty:** 1.5.2026  
**Lähde:** OP:n verkkopalvelu, ETF-listaus (703 laajemmasta valikoimasta 144 valittu shortlistille)  
**Käyttö:** sijoitusagentti_v3.py lataa tämän automaattisesti ostosuositusten pohjaksi

## Suodatusperiaatteet

- **Pois:** vipu-ETF:t (2x/3x), inverssit, kapeat hyödykkeet, kryptot, sektori-Eurooppa (pahentaisi Nordea+Mandatum-keskittymää)
- **Pois:** AUM < kategoriakohtainen kynnys, juoksevat kulut yli kategoriakohtaisen kynnyksen
- **Mukana:** globaalit/USA broad-indeksit, EM, Japani, Aasia, faktori-ETF:t, korkokorit, megatrendit, REIT, kulta

## Salkkukonteksti (huomioi suosituksissa)

- **OST-allokaatiopäätös:** noin 30 000 € (Neste-myynti 11 800 € + aiempi käteinen) → 3 ETF:ää
- **OST-keskittymä Eurooppaan ja finanssiin:** Nordea n. 22 445 €, Mandatum n. 13 509 € → vältä lisäämästä Eurooppa-finanssipainoa
- **Neste edelleen ~30 % suorista osakkeista** → energia-/öljysektoria ei tarvita lisää
- **Sijoitusvakuutuksessa jo n. 195 283 €**, eläkevakuutuksessa n. 87 506 € → kokonaissalkun riskinkanto on jo merkittävä

## Yhteensä shortlistilla: 144 tuotetta

Sarakkeet: **Tunnus** | **Nimi** | **ISIN** | **AUM** | **TER** | **Toteutus** | **Osinko**

> Toteutus: *Arvopaperi* = fyysinen replikaatio (yleensä turvallisempi), *Johdannainen* = swap-pohjainen


## 📊 Korot ja korkokorit

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| VECP | Vanguard EUR Corporate Bond UCITS ETF | IE00BZ163G84 | 2 988,79 M€ | 0,07 % | Arvopaperi | Kuukausittain |
| XGLE | Xtrackers II Eurozone Government Bond UCITS ETF | LU0290355717 | 2 247,59 M€ | 0,07 % | Arvopaperi | Akkumuloiva |
| IUSU | iShares USD Treasury Bond 1-3yr UCITS ETF USD | IE00B14X4S71 | 2 423,71 M$ | 0,07 % | Arvopaperi | Puolivuosittain |
| IUSM | iShares USD Treasury Bond 7-10yr UCITS ETF | IE00B1FZS798 | 3 387,69 M$ | 0,07 % | Arvopaperi | Puolivuosittain |
| SXRM | iShares USD Treasury Bond 7-10yr UCITS ETF USD (Acc) USD | IE00B3VWN518 | 4 762,21 M$ | 0,07 % | Arvopaperi | Akkumuloiva |
| VUCE | Vanguard USD Corporate Bond UCITS ETF Accum Unhedged USD | IE00BGYWFK87 | 3 102,4 M$ | 0,09 % | Arvopaperi | Akkumuloiva |
| EUNH | iShares Core EUR Govt Bond UCITS ETF | IE00B4WXJJ64 | 4 919,8 M€ | 0,09 % | Arvopaperi | Puolivuosittain |
| IBCI | iShares PLC - iShares Euro Inflation Linked Government Bond UCITS ETF AccumEUR | IE00B0M62X26 | 1 823,08 M€ | 0,09 % | Arvopaperi | Akkumuloiva |
| L8I3 | Amundi EUR Overnight Return UCITS ETF -Acc- | FR0010510800 | 2 951,67 M€ | 0,10 % | Johdannainen | Akkumuloiva |
| VAGF | Vanguard Global Aggregate Bond UCITS ETF Accum Shs Hedged EUR | IE00BG47KH54 | 1 961,95 M£ | 0,10 % | Arvopaperi | Akkumuloiva |
| XEON | Xtrackers II EUR Overnight Rate Swap UCITS ETF | LU0290358497 | 20 402,2 M€ | 0,10 % | Johdannainen | Akkumuloiva |
| EUNA | iShares Core Global Aggregate Bond UCITS ETF Accum Hedged EUR | IE00BDBRDM35 | 2 379,64 M$ | 0,10 % | Arvopaperi | Akkumuloiva |
| IUST | iShares USD TIPS UCITS ETF | IE00B1FZSC47 | 2 843,03 M$ | 0,10 % | Arvopaperi | Akkumuloiva |
| D5BG | Xtrackers II EUR Corporate Bond UCITS ETF | LU0478205379 | 4 213,58 M€ | 0,12 % | Arvopaperi | Akkumuloiva |
| IBCN | iShares EUR Govt Bond 3-5 Year UCITS ETF | IE00B1FZS681 | 2 186,98 M€ | 0,15 % | Arvopaperi | Puolivuosittain |
| QDVL | iShares II PLC - iShares EUR Corp Bond 0-3Yr ESG SRI UCITS ETF Shs EUR | IE00BYZTVV78 | 2 168,5 M€ | 0,15 % | Arvopaperi | Puolivuosittain |
| SUA0 | iShares II PLC - iShares Euro Corp Bond ESG SRI UCITS ETF Accum Shs EUR | IE000L2TO2T2 | 1 519,02 M€ | 0,15 % | Arvopaperi | Akkumuloiva |

## 🌍 Globaalit osakemarkkinat (broad)

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| SC0J | Invesco MSCI World UCITS ETF | IE00B60SX394 | 7 283,08 M$ | 0,05 % | Johdannainen | Akkumuloiva |
| WEBG | Amundi Prime All Country World UCITS ETF USD | IE0009HF1MK9 | 4 436,68 M$ | 0,07 % | Arvopaperi | Vuosittain |
| VGVE | Vanguard FTSE Developed World UCITS ETF | IE00BKX55T58 | 4 282,12 M$ | 0,12 % | Arvopaperi | Neljännesvuosittain |
| VGVF | Vanguard FTSE Developed World UCITS ETF USD | IE00BK5BQV03 | 6 393,54 M$ | 0,12 % | Arvopaperi | Akkumuloiva |
| XDWD | Xtrackers MSCI World UCITS ETF | IE00BJ0KDQ92 | 21 048,9 M$ | 0,12 % | Arvopaperi | Akkumuloiva |
| MWRE | Amundi Core MSCI World UCITS ETF Accum USD | IE000BI8OT95 | 15 259,4 M$ | 0,14 % | Arvopaperi | Akkumuloiva |
| EXUS | Xtrackers MSCI World ex USA UCITS ETF 1C USD | IE0006WW1TQ4 | 6 115,42 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| XAMB | Amundi MSCI World SRI Climate Paris Aligned UCITS ETF Accum EUR | IE000Y77LGG9 | 3 214,28 M$ | 0,18 % | Arvopaperi | Akkumuloiva |
| VGWL | Vanguard FTSE All-World UCITS ETF | IE00B3RBWM25 | 24 015,7 M$ | 0,19 % | Arvopaperi | Neljännesvuosittain |
| VWCE | Vanguard FTSE All-World UCITS ETF Accum USD | IE00BK5BQT80 | 41 406,1 M$ | 0,19 % | Arvopaperi | Akkumuloiva |
| XDWL | Xtrackers MSCI World UCITS ETF | IE00BK1PV551 | 5 079,33 M$ | 0,19 % | Arvopaperi | Neljännesvuosittain |
| EUNL | iShares Core MSCI World UCITS ETF | IE00B4L5Y983 | 135 308 M$ | 0,20 % | Arvopaperi | Akkumuloiva |
| EDMW | iShares IV PLC - iShares MSCI World CTB Enhanced ESG UCITS ETF Accum Shs Unhedged USD | IE00BHZPJ569 | 4 437,71 M$ | 0,20 % | Arvopaperi | Akkumuloiva |
| IUSQ | iShares MSCI ACWI UCITS ETF | IE00B6R52259 | 30 098 M$ | 0,20 % | Arvopaperi | Akkumuloiva |

## 🇺🇸 USA-osakemarkkinat (broad)

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| WEBH | Amundi Core MSCI USA UCITS ETF Accum USD | IE000FSN19U2 | 3 558,96 M$ | 0,03 % | Arvopaperi | Akkumuloiva |
| — | SSGA SPDR ETFs Europe I PLC - State Street SPDR S&P 500 UCITS ETF Accum shs - USD | IE000XZSV718 | 16 103,5 M$ | 0,03 % | Arvopaperi | Akkumuloiva |
| SPY5 | SSGA SPDR ETFs Europe I PLC - State Street SPDR S&P 500 UCITS ETF USD | IE00B6YX5C33 | 19 419,7 M$ | 0,03 % | Arvopaperi | Neljännesvuosittain |
| SPPY | State Street SPDR S&P 500 Leaders UCITS ETF Accum Shs USD | IE00BH4GPZ28 | 5 252,81 M$ | 0,03 % | Arvopaperi | Akkumuloiva |
| SC0H | Invesco MSCI USA UCITS ETF Acc | IE00B60SX170 | 8 193,65 M$ | 0,05 % | Johdannainen | Akkumuloiva |
| P500 | Invesco S&P 500 UCITS ETF | IE00B3YCGJ38 | 37 708,7 M$ | 0,05 % | Johdannainen | Akkumuloiva |
| I500 | iShares S&P 500 Swap UCITS ETF AccumUSD | IE00BMTX1Y45 | 11 957,4 M$ | 0,05 % | Johdannainen | Akkumuloiva |
| VUSA | Vanguard S&P 500 UCITS ETF | IE00B3XXRP09 | 49 556 M$ | 0,07 % | Arvopaperi | Neljännesvuosittain |
| XD9U | Xtrackers MSCI USA UCITS ETF | IE00BJ0KDR00 | 11 742,6 M$ | 0,07 % | Arvopaperi | Akkumuloiva |
| SXR8 | iShares Core S&P 500 UCITS ETF | IE00B5BMR087 | 139 993 M$ | 0,07 % | Arvopaperi | Akkumuloiva |
| IUSA | iShares Core S&P 500 UCITS ETF USD (Dist) | IE0031442068 | 20 754,7 M$ | 0,07 % | Arvopaperi | Neljännesvuosittain |
| EDMU | iShares IV PLC - iShares MSCI USA CTB Enhanced ESG UCITS ETF Accum Shs Unhedged USD | IE00BHZPJ908 | 8 393,55 M$ | 0,07 % | Arvopaperi | Akkumuloiva |
| SGAS | iShares IV PLC - iShares MSCI USA Screened UCITS ETF Accum Shs Unhedged USD | IE00BFNM3G45 | 16 387,5 M$ | 0,07 % | Arvopaperi | Akkumuloiva |
| SXR4 | iShares MSCI USA UCITS ETF | IE00B52SFT06 | 4 368,33 M$ | 0,07 % | Arvopaperi | Akkumuloiva |
| XZMU | Xtrackers MSCI USA ESG UCITS ETF Accum Shs -1C- USD | IE00BFMNPS42 | 8 140,72 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| XMUS | Xtrackers MSCI USA SWAP UCITS ETF Capitalisation 1C | LU0274210672 | 5 085,02 M$ | 0,15 % | Johdannainen | Akkumuloiva |
| D5BM | Xtrackers S&P 500 SWAP UCITS ETF Capitalisation 1C | LU0490618542 | 4 701,74 M$ | 0,15 % | Johdannainen | Akkumuloiva |

## 🇨🇳 Aasia & Tyynimeri

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| XCS5 | Xtrackers MSCI INDIA SWAP UCITS ETF Capitalisation 1C | LU0514695187 | 640,32 M$ | 0,19 % | Johdannainen | Akkumuloiva |
| UIMT | UBS (Lux) Fund Solutions SICAV - UBS MSCI Pacific Socially Responsible UCITS ETF USD dis- Distribution | LU0629460832 | 731,73 M$ | 0,28 % | Arvopaperi | Puolivuosittain |
| ICGA | iShares MSCI China UCITS ETF AccumUSD | IE00BJ5JPG56 | 3 186,57 M$ | 0,28 % | Arvopaperi | Akkumuloiva |
| 36BZ | iShares MSCI China A UCITS ETF | IE00BQT3WG13 | 3 211,24 M$ | 0,40 % | Arvopaperi | Akkumuloiva |

## 🇪🇺 Eurooppa (broad — vain isoimmat, jotta OST-keskittymä ei pahene)

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| LYP6 | Amundi Core Stoxx Europe 600 -UCITS ETF Acc- Capitalisation | LU0908500753 | 17 814,3 M€ | 0,07 % | Arvopaperi | Akkumuloiva |
| IUSZ | iShares Core FTSE 100 UCITS ETF GBP (Dist) | IE0005042456 | 15 286,5 M£ | 0,07 % | Arvopaperi | Neljännesvuosittain |
| DBXD | Xtrackers DAX UCITS ETF | LU0274211480 | 6 793,03 M€ | 0,09 % | Arvopaperi | Akkumuloiva |
| XESC | Xtrackers EURO STOXX 50 UCITS ETF Capitalisation 1C | LU0380865021 | 6 031,17 M€ | 0,09 % | Arvopaperi | Akkumuloiva |
| XESX | Xtrackers EURO STOXX 50 UCITS ETF Distribution 1D | LU0274211217 | 5 598,95 M€ | 0,09 % | Arvopaperi | Neljännesvuosittain |
| SXRT | iShares Core EURO STOXX 50 UCITS ETF | IE00B53L3W79 | 7 038,61 M€ | 0,10 % | Arvopaperi | Akkumuloiva |
| EUN2 | iShares Core EURO STOXX 50 UCITS ETF (Irl) | IE0008471009 | 5 323,34 M€ | 0,10 % | Arvopaperi | Neljännesvuosittain |
| SPYY | SSGA SPDR ETFs Europe I Plc - MSCI All Con. Wld. UCITS ETF | IE00B44Z5B48 | 11 325 M$ | 0,12 % | Arvopaperi | Akkumuloiva |
| IQQY | iShares Core MSCI Europe UCITS ETF | IE00B1YZSC51 | 10 494,1 M€ | 0,12 % | Arvopaperi | Neljännesvuosittain |
| EUNK | iShares Core MSCI Europe UCITS ETF EUR (Acc) | IE00B4K48X80 | 14 804,2 M€ | 0,12 % | Arvopaperi | Akkumuloiva |

## 🇯🇵 Japani

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| LCUJ | Multi Units Luxembourg SICAV - Amundi Core MSCI Japan UCITS ETF Acc | LU1781541252 | 933 000 MJPY | 0,12 % | Arvopaperi | Akkumuloiva |
| EUNN | iShares Core MSCI Japan IMI UCITS ETF | IE00B4L5YX21 | 7 366,09 M$ | 0,12 % | Arvopaperi | Akkumuloiva |
| IQQJ | iShares MSCI Japan UCITS ETF USD (Dist) | IE00B02KXH56 | 2 546,92 M$ | 0,12 % | Arvopaperi | Puolivuosittain |
| VJPA | Vanguard FTSE Japan UCITS ETF Accum Shs USD | IE00BFMXYX26 | 1 340,74 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| EDMJ | iShares IV PLC - iShares MSCI Japan CTB Enhanced ESG UCITS ETF Accum Shs Unhedged USD | IE00BHZPJ452 | 1 352,41 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| SGAJ | iShares IV PLC - iShares MSCI Japan Screened UCITS ETF AccumUnhedged USD | IE00BFNM3L97 | 1 965,48 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| EJAP | BNP Paribas Easy SICAV - MSCI Japan Min TE UCITS ETF- Capitalisation | LU1291102447 | 1 628,1 M€ | 0,17 % | Arvopaperi | Akkumuloiva |
| XZMJ | Xtrackers MSCI Japan ESG UCITS ETF Accum Shs -1C- USD | IE00BG36TC12 | 3 074,96 M$ | 0,20 % | Arvopaperi | Akkumuloiva |
| SXR1 | iShares Core MSCI Pacific ex Japan UCITS ETF | IE00B52MJY50 | 3 740,83 M$ | 0,20 % | Arvopaperi | Akkumuloiva |
| XZW0 | Xtrackers(IE)PLC - Xtrackers MSCI Japan ESG UCITS ETF Accum-1C- USD | IE00BZ02LR44 | 5 931,76 M€ | 0,25 % | Arvopaperi | Akkumuloiva |

## 🌏 Kehittyvät markkinat

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| SXR7 | iShares Core MSCI EMU UCITS ETF | IE00B53QG562 | 6 565,59 M€ | 0,12 % | Arvopaperi | Akkumuloiva |
| EDM4 | iShares IV PLC - iShares MSCI EMU CTB Enhanced ESG UCITS ETF Accum Shs Unhedged EUR | IE00BHZPJ015 | 3 130,43 M€ | 0,12 % | Arvopaperi | Akkumuloiva |
| XD5E | Xtrackers MSCI EMU UCITS ETF Distribution 1D | LU0846194776 | 1 862,04 M€ | 0,14 % | Arvopaperi | Puolivuosittain |
| EMXC | Amundi MSCI Emerging Ex China ETF Acc Capitalisation | LU2009202107 | 5 074,46 M$ | 0,15 % | Johdannainen | Akkumuloiva |
| SPYM | State Street SPDR MSCI Emerging Markets UCITS ETF Accum.Shs USD | IE00B469F816 | 1 942,55 M$ | 0,18 % | Arvopaperi | Akkumuloiva |
| XMME | Xtrackers MSCI Emerging Markets UCITS ETF | IE00BTJRMP35 | 12 336,4 M$ | 0,18 % | Arvopaperi | Akkumuloiva |
| IS3N | iShares Core MSCI EM IMI UCITS ETF | IE00BKM4GZ66 | 39 950,6 M$ | 0,18 % | Arvopaperi | Akkumuloiva |
| EUNM | iShares MSCI EM UCITS ETF USD (Acc) | IE00B4L5YC18 | 8 955,71 M$ | 0,18 % | Arvopaperi | Akkumuloiva |
| IQQE | iShares MSCI EM UCITS ETF USD (Dist) | IE00B0M63177 | 9 593,99 M$ | 0,18 % | Arvopaperi | Neljännesvuosittain |
| AMEM | Amundi MSCI Emerging Markets Swap -UCITS ETF EUR C- Capitalisation | LU1681045370 | 3 928,23 M€ | 0,20 % | Johdannainen | Akkumuloiva |
| CEBL | iShares MSCI EM Asia UCITS ETF | IE00B5L8K969 | 7 528,75 M$ | 0,20 % | Arvopaperi | Akkumuloiva |
| IUSC | iShares MSCI EM Latin America UCITS ETF USD | IE00B27YCK28 | 2 267,18 M$ | 0,20 % | Arvopaperi | Puolivuosittain |
| AYEM | iShares IV PLC - iShares MSCI EM IMI Screened UCITS ETF AccumUnhedged USD | IE00BFNM3P36 | 6 490,74 M$ | 0,21 % | Arvopaperi | Akkumuloiva |
| VFEM | Vanguard FTSE Emerging Markets UCITS ETF | IE00B3VVMM84 | 3 467,16 M$ | 0,22 % | Arvopaperi | Neljännesvuosittain |
| VFEA | Vanguard FTSE Emerging Markets UCITS ETF AccumUSD | IE00BK5BR733 | 2 122,01 M$ | 0,22 % | Arvopaperi | Akkumuloiva |
| UEF5 | UBS MSCI EM Socially Responsible UCITS ETF USD dis Distribution | LU1048313891 | 2 745,57 M$ | 0,24 % | Arvopaperi | Puolivuosittain |
| XZEM | Xtrackers MSCI Emerging Markets ESG UCITS ETF Accum Shs -1C- USD | IE00BG370F43 | 1 744,63 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| 84X0 | iShares MSCI EM ex-China UCITS ETF | IE00BMG6Z448 | 5 325 M$ | 0,25 % | Arvopaperi | Akkumuloiva |

## 🏭 USA-sektorit (eivät pahenna Eurooppa-keskittymää)

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| IU5C | iShares S&P 500 Communication Sector UCITS ETF | IE00BDDRF478 | 1 122,09 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| QDVK | iShares S&P 500 Consumer Discretionary Sector UCITS ETF | IE00B4MCHD36 | 741,67 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| QDVF | iShares S&P 500 Energy Sector UCITS ETF | IE00B42NKQ00 | 2 030,06 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| QDVH | iShares S&P 500 Financials Sector UCITS ETF | IE00B4JNQZ49 | 2 163,17 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| QDVG | iShares S&P 500 Health Care Sector UCITS ETF | IE00B43HR379 | 2 444,24 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| 2B7C | iShares S&P 500 Industrials Sector UCITS ETF | IE00B4LN9N13 | 715,22 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| QDVE | iShares S&P 500 Information Technology Sector UCITS ETF | IE00B3WJKG14 | 16 915,3 M$ | 0,15 % | Arvopaperi | Akkumuloiva |
| 2B7A | iShares S&P 500 Utilities Sector UCITS ETF | IE00B4KBBD01 | 1 174,75 M$ | 0,15 % | Arvopaperi | Akkumuloiva |

## 🌐 Globaalit sektorit

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| WELH | Amundi ETF ICAV - Amundi S&P World Industrials Screened UCITS ETF Accum DR EUR | — | 861,67 M€ | 0,18 % | Arvopaperi | Akkumuloiva |
| WELI | Amundi ETF ICAV - Amundi S&P World Materials Screened UCITS ETF Accum Shs -DR- EUR | — | 644,63 M€ | 0,18 % | Arvopaperi | Akkumuloiva |
| WELX | Amundi S&P World Communication Services Screened UCITS ETF Accum -DR- EUR | IE000EFHIFG3 | 512,99 M€ | 0,18 % | Arvopaperi | Akkumuloiva |
| CBUF | iShares MSCI World Health Care Sector Advanced UCITS ETF USD | IE00BJ5JNZ06 | 565,64 M$ | 0,18 % | Arvopaperi | Puolivuosittain |
| XWTS | Xtrackers MSCI World Communication Services UCITS ETF | IE00BM67HR47 | 530,4 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| XDWS | Xtrackers MSCI World Consumer Staples UCITS ETF | IE00BM67HN09 | 859,34 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| XDWH | Xtrackers MSCI World Health Care UCITS ETF | IE00BM67HK77 | 3 140,11 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| XDWI | Xtrackers MSCI World Industrials UCITS ETF | IE00BM67HV82 | 957,45 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| XDWT | Xtrackers MSCI World Information Technology UCITS ETF | IE00BM67HT60 | 5 552,31 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| XDWM | Xtrackers MSCI World Materials UCITS ETF | IE00BM67HS53 | 722,98 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| XDWU | Xtrackers MSCI World Utilities UCITS ETF | IE00BM67HQ30 | 935,97 M€ | 0,25 % | Arvopaperi | Akkumuloiva |
| AYEW | iShares MSCI World Information Technology Sector Advanced UCITS ETF USD | IE00BJ5JNY98 | 894,62 M$ | 0,25 % | Arvopaperi | Puolivuosittain |
| LYPE | Amundi MSCI World Health Care UCITS ETF EUR ACC | LU0533033238 | 673,63 M€ | 0,30 % | Johdannainen | Akkumuloiva |
| LYPG | Multi Units Luxembourg SICAV - Amundi MSCI World Information Technology UCITS ETF EUR ACC | LU0533033667 | 2 450,71 M€ | 0,30 % | Johdannainen | Akkumuloiva |
| XDWF | Xtrackers MSCI World Financials UCITS ETF | IE00BM67HL84 | 871,95 M$ | 0,30 % | Arvopaperi | Akkumuloiva |

## 🎯 Faktorit (quality, value, dividend, low vol, small cap)

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| MWEQ | Invesco MSCI World Equal Weight UCITS ETF Acc AccumUSD | IE000OEF25S1 | 1 409,36 M$ | 0,20 % | Arvopaperi | Akkumuloiva |
| XDEB | Xtrackers MSCI World Minimum Volatility UCITS ETF | IE00BL25JN58 | 1 024,41 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| XDEM | Xtrackers MSCI World Momentum UCITS ETF | IE00BL25JP72 | 1 964 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| XDEQ | Xtrackers MSCI World Quality UCITS ETF | IE00BL25JL35 | 2 923,85 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| XDEV | Xtrackers MSCI World Value UCITS ETF | IE00BL25JM42 | 4 562,8 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| IS3R | iShares Edge MSCI World Momentum Factor UCITS ETF | IE00BP3QZ825 | 4 434,85 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| IS3Q | iShares Edge MSCI World Quality Factor UCITS ETF | IE00BP3QZ601 | 4 959,58 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| IS3S | iShares Edge MSCI World Value Factor UCITS ETF | IE00BP3QZB59 | 6 321,78 M$ | 0,25 % | Arvopaperi | Akkumuloiva |
| VGWD | Vanguard FTSE All-World High Dividend Yield UCITS ETF USD | IE00B8GKDB10 | 9 251,86 M$ | 0,29 % | Arvopaperi | Neljännesvuosittain |
| VGWE | Vanguard Funds PLC - Vanguard FTSE All-World High Dividend Yield UCITS ETF AccumUSD | IE00BK5BR626 | 2 480,48 M$ | 0,29 % | Arvopaperi | Akkumuloiva |
| TSWE | VanEck World Equal Weight Screened UCITS ETF | NL0010408704 | 1 229,61 M€ | 0,30 % | Arvopaperi | Neljännesvuosittain |
| IQQ0 | iShares Edge MSCI World Minimum Volatility UCITS ETF USD | IE00B8FHGS14 | 2 463,02 M$ | 0,30 % | Arvopaperi | Akkumuloiva |
| IUSN | iShares MSCI World Small Cap UCITS ETF | IE00BF4RFH31 | 7 633,3 M$ | 0,35 % | Arvopaperi | Akkumuloiva |

## 🚀 Megatrendit (AI, robotics, clean energy, defence, infra ym.)

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| LYTR | Amundi Bloomberg Equal-weight Commodity ex-Agriculture UCITS ETF Shs -Acc- Capitalisation | LU1829218749 | 1 604,81 M€ | 0,35 % | Johdannainen | Akkumuloiva |
| LSMC | Multi Units Luxembourg SICAV - Amundi MSCI Semiconductors | LU1900066033 | 1 534,52 M$ | 0,35 % | Arvopaperi | Akkumuloiva |
| VVSM | VanEck Semiconductor UCITS ETF Accum A USD | IE00BMC38736 | 6 062,53 M$ | 0,35 % | Arvopaperi | Akkumuloiva |
| XAIX | Xtrackers Artificial Intelligence & Big Data UCITS ETF | IE00BGV5VN51 | 7 184,1 M$ | 0,35 % | Arvopaperi | Akkumuloiva |
| AIFS | iShares AI Infrastructure UCITS ETF Accum USD | IE000X59ZHE2 | 889,36 M | 0,35 % | Arvopaperi | Akkumuloiva |
| WTI2 | WisdomTree Artificial Intelligence UCITS ETF USD Acc | IE00BDVPNG13 | 1 149,24 M$ | 0,40 % | Arvopaperi | Akkumuloiva |
| 2B76 | iShares Automation & Robotics UCITS ETF | IE00BYZK4552 | 4 370,84 M$ | 0,40 % | Arvopaperi | Akkumuloiva |
| 2B78 | iShares Healthcare Innovation UCITS ETF | IE00BYZK4776 | 964,66 M$ | 0,40 % | Arvopaperi | Akkumuloiva |
| ASWC | Future of Defence UCITS ETF Accum USD | IE000OJ5TQP4 | 3 038,99 M$ | 0,49 % | Arvopaperi | Akkumuloiva |
| BATE | L&G Battery Value-Chain UCITS ETF | IE00BF0M2Z96 | 964,25 M$ | 0,49 % | Arvopaperi | Akkumuloiva |
| XMLC | Legal & General Clean Water UCITS ETF Accum USD | IE00BK5BC891 | 669,37 M$ | 0,49 % | Arvopaperi | Akkumuloiva |
| XMLD | Legal & General UCITS ETF Plc - Artificial Intelligence | IE00BK5BCD43 | 1 689,33 M$ | 0,49 % | Arvopaperi | Akkumuloiva |
| RENW | Legal & General UCITS ETF Plc - L&G Clean EnergyUCITS ETF AccumUSD | IE00BK5BCH80 | 737,31 M$ | 0,49 % | Arvopaperi | Akkumuloiva |
| OD7U | WisdomTree Agriculture | GB00B15KYH63 | 930,18 M$ | 0,49 % | Johdannainen | Akkumuloiva |
| GOAI | Amundi MSCI Robotics & AI -UCITS ETF Acc- Capitalisation | LU1861132840 | 1 041,67 M€ | 0,50 % | Arvopaperi | Akkumuloiva |

## 🏘️ Kiinteistöt (REIT)

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| IQQ7 | iShares US Property Yield UCITS ETF | IE00B1FZSF77 | 639,86 M$ | 0,40 % | Arvopaperi | Neljännesvuosittain |

## 🥇 Kulta (turvasatama)

| Tunnus | Nimi | ISIN | AUM | TER | Toteutus | Osinko |
|---|---|---|---|---|---|---|
| PPFB | iShares Physical Gold ETC | IE00B4ND3602 | 37 989,8 M$ | 0,12 % | Arvopaperi | Akkumuloiva |
| GZUR | WisdomTree Physical Swiss Gold | JE00B588CD74 | 5 192 M$ | 0,15 % | Arvopaperi | Akkumuloiva |

---

## Käyttöohje agentille

Kun käyttäjä pyytää ETF-suositusta:

1. Lue salkun nykytila `salkku_konteksti.md`-tiedostosta
2. Lue tämä shortlist (`op_etf_valikoima.md`)
3. Suosittele 3 ETF:ää tästä listasta — älä keksi tunnuksia listan ulkopuolelta
4. Perustele jokainen valinta: rooli salkussa, korrelaatio nykyisiin sijoituksiin, kulut, AUM
5. Anna allokaatiojakauma euroissa ja prosentteina pyydetylle summalle
6. Mainitse riskit ja vaihtoehdot

---
*Tiedosto luotu: 1.5.2026 — Jan + Claude session A1*