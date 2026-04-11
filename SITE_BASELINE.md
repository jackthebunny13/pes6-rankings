# SITE_BASELINE.md

## Canonical Rule

Questa release del sito è la baseline canonica attuale.

Da qui in poi:
- nessuna modifica futura può rimuovere o regressare feature esistenti senza richiesta esplicita di Jack
- ogni change al sito va fatto sopra questa baseline, non sopra file presi da release vecchie o mismatchate
- prima di pushare, verificare sempre che root e `tools/pes6-rankings/` siano coerenti per i file del sito

## Feature che devono restare

- Ranking Squadre con ordinamenti attivi
- Vista Squadre con toggle **Formazione / Rosa**
- Vista Rosa con toggle **OVR / Ruoli**
- Persistenza formazione
- Sub-position filters in Ranking Ruoli
- Sezione Skills completa
- Top 10 Skills
- Badge piede, incluso **AX** per ambidestri forti
- Capitani visibili
- Panchina + Tribuna
- Click-to-swap / gestione formazione interattiva
- Powered by Zio Tore

## Data Source Map

### Arriva da `data.json`
- OVR giocatori
- stats giocatori
- dati nazionalità / flag esportati
- liste giocatori per team
- ranking dati-based

### È hardcoded in `index.html`
- `leagues`
- `teamConfigs`
- `_defaultLineupNames`
- `subtitle`
- `captain`
- `pitchHtml`
- parte della UI e dei toggle
- parte delle etichette e della logica di rendering del team view

## Critical Risk

Il sito NON è guidato solo da `data.json`.

Per questo motivo, cambiare solo il JSON o solo l'HTML può creare regressioni invisibili.

## Working Rule

Quando si modifica il sito:
1. partire dalla baseline attuale
2. toccare il minimo possibile
3. non prendere `index.html` o `data.json` da commit vecchi senza audit
4. se si cambia una feature UI, verificare che non spariscano:
   - ordinamenti Ranking Squadre
   - toggle OVR/Ruoli
   - Titolari / Rosa
   - formazione interattiva
   - sub-filter ruoli
   - skills section
5. pushare solo dopo verifica di coerenza tra root e `tools/pes6-rankings/`

## Note operative

- `Desktop/use_this_file.csv` resta la source of truth del database giocatori
- `tools/pes6-rankings/gen.py` genera il `data.json`
- il sito GitHub Pages serve i file in root, quindi root va trattata come release effettiva pubblicata
