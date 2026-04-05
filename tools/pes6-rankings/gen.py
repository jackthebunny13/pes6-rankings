#!/usr/bin/env python3
"""
PES6 Rankings Generator - HYBRID OVR SYSTEM
40% Core universale + 60% Specifico per ruolo = OVR 0-99 stile FIFA
"""
import csv, json
from collections import defaultdict

CSV = '/Users/ziotore/Desktop/use_this_file.csv'
OUT = '/Users/ziotore/.openclaw/workspace/tools/pes6-rankings/data.json'

POS = {'0':'GK','2':'SW','3':'CB','4':'SB','5':'DMF','6':'WB','7':'CMF','8':'SMF','9':'AMF','10':'WF','11':'SS','12':'CF'}
NAMES = {'GK':'Portieri','CB':'Difensori Centrali','SW':'Liberi','SB':'Terzini','WB':'Esterni Bassi','DMF':'Centrocampisti','CMF':'Centrocampisti','SMF':'Esterni','AMF':'Trequartisti','WF':'Ali','SS':'Attaccanti','CF':'Attaccanti'}

# Descrizioni formule per il sito
FORMULAS = {
    'GK': {
        'desc': 'Per i portieri conta soprattutto la parata (GK), poi riflessi e posizionamento.',
        'primary': ['Parata (GK)', 'Riflessi', 'Elevazione'],
        'secondary': ['Altezza', 'Equilibrio', 'Mentalità']
    },
    'CB': {
        'desc': 'Per i centrali (CB/SW) la difesa è fondamentale, seguita da colpo di testa e posizionamento.',
        'primary': ['Difesa', 'Colpo di testa', 'Reattività', 'Mentalità'],
        'secondary': ['Elevazione', 'Equilibrio', 'Velocità', 'Aggressività']
    },
    'SB': {
        'desc': 'I terzini (SB/WB) devono difendere ma anche spingere: velocità, resistenza e cross sono cruciali.',
        'primary': ['Difesa', 'Velocità', 'Resistenza', 'Accelerazione'],
        'secondary': ['Passaggio corto', 'Attacco', 'Dribbling', 'Equilibrio']
    },
    'DMF': {
        'desc': 'Il mediano difensivo fa da filtro: difesa, passaggio e lettura del gioco.',
        'primary': ['Difesa', 'Passaggio corto', 'Passaggio lungo', 'Reattività'],
        'secondary': ['Resistenza', 'Equilibrio', 'Mentalità', 'Aggressività']
    },
    'CMF': {
        'desc': 'Il centrocampista centrale è il regista: passaggio, tecnica e visione di gioco.',
        'primary': ['Passaggio corto', 'Passaggio lungo', 'Tecnica', 'Resistenza'],
        'secondary': ['Equilibrio', 'Reattività', 'Dribbling', 'Difesa', 'Attacco']
    },
    'SMF': {
        'desc': 'Gli esterni (SMF/WF) saltano l\'uomo: velocità, dribbling e cross sono le armi principali.',
        'primary': ['Velocità', 'Dribbling', 'Accelerazione', 'Tecnica'],
        'secondary': ['Passaggio corto', 'Resistenza', 'Agilità', 'Tiro']
    },
    'AMF': {
        'desc': 'Il trequartista crea gioco: tecnica, passaggio e visione per l\'ultimo passaggio.',
        'primary': ['Tecnica', 'Passaggio corto', 'Dribbling', 'Passaggio lungo'],
        'secondary': ['Reattività', 'Attacco', 'Tiro', 'Agilità', 'Punizioni']
    },
    'SS': {
        'desc': 'La seconda punta si muove tra le linee: movimento, tecnica e finalizzazione.',
        'primary': ['Attacco', 'Tecnica', 'Tiro', 'Dribbling'],
        'secondary': ['Velocità', 'Accelerazione', 'Reattività', 'Passaggio']
    },
    'CF': {
        'desc': 'L\'attaccante deve segnare: tiro, colpo di testa, potenza e posizionamento.',
        'primary': ['Tiro', 'Attacco', 'Colpo di testa', 'Potenza tiro'],
        'secondary': ['Velocità', 'Tecnica', 'Elevazione', 'Equilibrio']
    }
}
FORMULAS['SW'] = FORMULAS['CB']
FORMULAS['WB'] = FORMULAS['SB']
FORMULAS['WF'] = FORMULAS['SMF']

def g(p, f, d=50):
    try:
        v = p.get(f, d)
        return d if v == '' or v is None else int(v)
    except:
        return d

# =====================================================
# HYBRID OVR SYSTEM - FIFA STYLE (0-99)
# 40% Core Universale + 60% Specifico per Ruolo
# =====================================================

def core_universal(p):
    """
    CORE UNIVERSALE (40% del OVR totale)
    Stats che servono a TUTTI i giocatori
    """
    technique = g(p, 'TECHNIQUE')
    balance = g(p, 'BALANCE')
    stamina = g(p, 'STAMINA')
    response = g(p, 'RESPONSE')
    agility = g(p, 'AGILITY')
    
    # Media pesata delle 5 stats core
    core = (
        technique * 0.25 +
        balance * 0.20 +
        stamina * 0.20 +
        response * 0.20 +
        agility * 0.15
    )
    return core

def core_gk(p):
    """Core per portieri - diverso dagli altri"""
    gk_skill = g(p, 'GOAL KEEPING')
    response = g(p, 'RESPONSE')
    balance = g(p, 'BALANCE')
    mentality = g(p, 'MENTALITY')
    jump = g(p, 'JUMP')
    
    core = (
        gk_skill * 0.35 +
        response * 0.25 +
        jump * 0.15 +
        balance * 0.15 +
        mentality * 0.10
    )
    return core

# === POSITION-SPECIFIC SCORES (60% del OVR) ===

def pos_gk(p):
    """GK: parate, riflessi, uscite"""
    return (
        g(p, 'GOAL KEEPING') * 0.45 +
        g(p, 'RESPONSE') * 0.25 +
        g(p, 'JUMP') * 0.15 +
        g(p, 'MENTALITY') * 0.15
    )

def pos_cb(p):
    """CB/SW: difesa, aereo, posizionamento"""
    return (
        g(p, 'DEFENSE') * 0.35 +
        g(p, 'HEADING') * 0.20 +
        g(p, 'RESPONSE') * 0.15 +
        g(p, 'MENTALITY') * 0.15 +
        g(p, 'JUMP') * 0.10 +
        g(p, 'AGGRESSION') * 0.05
    )

def pos_sb(p):
    """SB/WB: difesa + spinta"""
    return (
        g(p, 'DEFENSE') * 0.25 +
        g(p, 'TOP SPEED') * 0.20 +
        g(p, 'ACCELERATION') * 0.15 +
        g(p, 'STAMINA') * 0.15 +
        g(p, 'SHORT PASS ACCURACY') * 0.10 +
        g(p, 'DRIBBLE ACCURACY') * 0.10 +
        g(p, 'ATTACK') * 0.05
    )

def pos_dmf(p):
    """CM (merged DMF+CMF): centrocampista completo"""
    return (
        g(p, 'SHORT PASS ACCURACY') * 0.20 +
        g(p, 'DEFENSE') * 0.18 +
        g(p, 'LONG PASS ACCURACY') * 0.15 +
        g(p, 'STAMINA') * 0.12 +
        g(p, 'MENTALITY') * 0.12 +
        g(p, 'ATTACK') * 0.08 +
        g(p, 'DRIBBLE ACCURACY') * 0.08 +
        g(p, 'RESPONSE') * 0.07
    )

pos_cmf = pos_dmf  # Merged: same formula for both

def pos_smf(p):
    """SMF/WF: velocità, dribbling, cross"""
    return (
        g(p, 'TOP SPEED') * 0.20 +
        g(p, 'DRIBBLE ACCURACY') * 0.25 +
        g(p, 'ACCELERATION') * 0.15 +
        g(p, 'DRIBBLE SPEED') * 0.15 +
        g(p, 'LONG PASS ACCURACY') * 0.10 +  # crossing
        g(p, 'SHORT PASS ACCURACY') * 0.10 +
        g(p, 'ATTACK') * 0.05
    )

def pos_amf(p):
    """AMF: creatività, ultimo passaggio"""
    return (
        g(p, 'SHORT PASS ACCURACY') * 0.25 +
        g(p, 'DRIBBLE ACCURACY') * 0.20 +
        g(p, 'LONG PASS ACCURACY') * 0.15 +
        g(p, 'ATTACK') * 0.15 +
        g(p, 'SHOT ACCURACY') * 0.10 +
        g(p, 'FREE KICK ACCURACY') * 0.10 +
        g(p, 'SHOT TECHNIQUE') * 0.05
    )

def pos_ss(p):
    """FW (merged SS+CF): attaccante completo"""
    return (
        g(p, 'ATTACK') * 0.22 +
        g(p, 'SHOT ACCURACY') * 0.18 +
        g(p, 'HEADING') * 0.10 +
        g(p, 'DRIBBLE ACCURACY') * 0.10 +
        g(p, 'TOP SPEED') * 0.10 +
        g(p, 'SHOT TECHNIQUE') * 0.08 +
        g(p, 'SHOT POWER') * 0.07 +
        g(p, 'ACCELERATION') * 0.05 +
        g(p, 'SHORT PASS ACCURACY') * 0.05 +
        g(p, 'JUMP') * 0.05
    )

pos_cf = pos_ss  # Merged: same formula for both

POS_FUNCS = {
    'GK': pos_gk, 'CB': pos_cb, 'SW': pos_cb,
    'SB': pos_sb, 'WB': pos_sb,
    'DMF': pos_dmf, 'CMF': pos_cmf,
    'SMF': pos_smf, 'WF': pos_smf,
    'AMF': pos_amf, 'SS': pos_ss, 'CF': pos_cf
}

def calculate_ovr(p, pos):
    """
    HYBRID OVR FORMULA
    GK: 100% specifico (il core è già dentro pos_gk)
    Altri: 40% Core + 60% Position-specific
    """
    if pos == 'GK':
        # Portieri: formula speciale
        ovr = pos_gk(p)
    else:
        # Tutti gli altri: ibrido
        core = core_universal(p)
        pos_score = POS_FUNCS.get(pos, pos_cmf)(p)
        # Attaccanti: meno core, più posizione (un tank non deve avere tech/agility altissimi)
        if pos in ('CF', 'SS'):
            ovr = core * 0.30 + pos_score * 0.70
        else:
            ovr = core * 0.40 + pos_score * 0.60
    
    # Clamp a 99 max
    return min(99, max(1, int(round(ovr))))

# === LEGACY SCORING (per rankings di ruolo, punteggi più alti per differenziare) ===

def gk_legacy(p):
    return int(g(p,'GOAL KEEPING') * 4.0 + g(p,'RESPONSE') * 1.5 + g(p,'JUMP') * 1.2 +
               g(p,'BALANCE') * 0.6 + g(p,'MENTALITY') * 0.8 + max(0, (g(p,'HEIGHT',180) - 180) * 0.8))

def cb_legacy(p):
    return int(g(p,'DEFENSE') * 4.0 + g(p,'HEADING') * 2.0 + g(p,'RESPONSE') * 1.5 +
               g(p,'MENTALITY') * 1.2 + g(p,'JUMP') * 1.0 + g(p,'BALANCE') * 0.8)

def sb_legacy(p):
    return int(g(p,'DEFENSE') * 2.5 + g(p,'TOP SPEED') * 1.8 + g(p,'STAMINA') * 1.5 +
               g(p,'ACCELERATION') * 1.3 + g(p,'SHORT PASS ACCURACY') * 1.0)

def dmf_legacy(p):
    return int(g(p,'DEFENSE') * 2.5 + g(p,'SHORT PASS ACCURACY') * 1.8 + 
               g(p,'LONG PASS ACCURACY') * 1.5 + g(p,'RESPONSE') * 1.3 + g(p,'STAMINA') * 1.0)

def cmf_legacy(p):
    return int(g(p,'SHORT PASS ACCURACY') * 2.0 + g(p,'LONG PASS ACCURACY') * 1.8 +
               g(p,'TECHNIQUE') * 1.5 + g(p,'STAMINA') * 1.3 + g(p,'BALANCE') * 0.9)

def smf_legacy(p):
    return int(g(p,'TOP SPEED') * 1.8 + g(p,'DRIBBLE ACCURACY') * 1.8 + 
               g(p,'ACCELERATION') * 1.5 + g(p,'TECHNIQUE') * 1.3 + g(p,'SHORT PASS ACCURACY') * 1.2)

def amf_legacy(p):
    return int(g(p,'TECHNIQUE') * 2.0 + g(p,'SHORT PASS ACCURACY') * 1.8 +
               g(p,'DRIBBLE ACCURACY') * 1.5 + g(p,'LONG PASS ACCURACY') * 1.3 + g(p,'RESPONSE') * 1.0)

def ss_legacy(p):
    return int(g(p,'ATTACK') * 2.0 + g(p,'TECHNIQUE') * 1.6 + g(p,'SHOT ACCURACY') * 1.5 +
               g(p,'DRIBBLE ACCURACY') * 1.3 + g(p,'TOP SPEED') * 1.2)

def cf_legacy(p):
    return int(g(p,'SHOT ACCURACY') * 2.2 + g(p,'ATTACK') * 2.0 + g(p,'HEADING') * 1.5 +
               g(p,'SHOT POWER') * 1.2 + g(p,'TOP SPEED') * 1.0)

LEGACY_FUNCS = {
    'GK': gk_legacy, 'CB': cb_legacy, 'SW': cb_legacy,
    'SB': sb_legacy, 'WB': sb_legacy,
    'DMF': dmf_legacy, 'CMF': cmf_legacy,
    'SMF': smf_legacy, 'WF': smf_legacy,
    'AMF': amf_legacy, 'SS': ss_legacy, 'CF': cf_legacy
}

# === MAIN ===
with open(CSV, 'r', encoding='latin-1') as f:
    raw = list(csv.DictReader(f))

print(f"Loaded {len(raw)} players")

proc = []
for p in raw:
    pos = POS.get(p.get('REGISTERED POSITION', ''))
    if not pos:
        continue
    
    # NEW: Hybrid OVR (0-99 FIFA style)
    ovr = calculate_ovr(p, pos)
    
    # Legacy score for position rankings
    legacy_func = LEGACY_FUNCS.get(pos, cmf_legacy)
    legacy_score = legacy_func(p)
    
    # Secondary positions
    pos_map = {'GK  0':'GK','CWP  2':'SW','CBT  3':'CB','SB  4':'SB','DMF  5':'DMF','WB  6':'WB','CMF  7':'CMF','SMF  8':'SMF','AMF  9':'AMF','WF 10':'WF','SS  11':'SS','CF  12':'CF'}
    pos2 = []
    for col_name, pos_name in pos_map.items():
        if pos_name != pos and str(p.get(col_name, '0')).strip() == '1':
            pos2.append(pos_name)

    # Nationality flag
    nat_flags = {
        'Italy':'🇮🇹','Brazil':'🇧🇷','Argentina':'🇦🇷','France':'🇫🇷','Germany':'🇩🇪',
        'Spain':'🇪🇸','England':'🏴󠁧󠁢󠁥󠁮󠁧󠁿','Netherlands':'🇳🇱','Portugal':'🇵🇹','Croatia':'🇭🇷',
        'Uruguay':'🇺🇾','Czech Republic':'🇨🇿','Switzerland':'🇨🇭','Macedonia':'🇲🇰',
        'Belgium':'🇧🇪','Colombia':'🇨🇴','Sweden':'🇸🇪','Denmark':'🇩🇰','Japan':'🇯🇵',
        'Mexico':'🇲🇽','Chile':'🇨🇱','Serbia':'🇷🇸','Cameroon':'🇨🇲','Nigeria':'🇳🇬',
        'Ghana':'🇬🇭','Senegal':'🇸🇳','Ivory Coast':'🇨🇮',"Cote D'Ivoire":'🇨🇮',"Cote d'Ivoire":'🇨🇮',
        'Romania':'🇷🇴','Turkey':'🇹🇷','Austria':'🇦🇹','Paraguay':'🇵🇾','Peru':'🇵🇪',
        'Morocco':'🇲🇦','Tunisia':'🇹🇳','Algeria':'🇩🇿','Poland':'🇵🇱','Greece':'🇬🇷',
        'Ireland':'🇮🇪','Scotland':'🏴󠁧󠁢󠁳󠁣󠁴󠁿','Wales':'🏴󠁧󠁢󠁷󠁬󠁳󠁿','Northern Ireland':'🇬🇧','Norway':'🇳🇴','Finland':'🇫🇮',
        'Russia':'🇷🇺','Ukraine':'🇺🇦','Czech':'🇨🇿','Serbia and Montenegro':'🇷🇸',
        'Bosnia-Herzegovina':'🇧🇦','Slovenia':'🇸🇮','Slovakia':'🇸🇰','Hungary':'🇭🇺',
        'Bulgaria':'🇧🇬','Israel':'🇮🇱','South Korea':'🇰🇷','Australia':'🇦🇺',
        'USA':'🇺🇸','Canada':'🇨🇦','Costa Rica':'🇨🇷','Honduras':'🇭🇳','Panama':'🇵🇦','Ecuador':'🇪🇨',
        'Venezuela':'🇻🇪','Bolivia':'🇧🇴','South Africa':'🇿🇦','Egypt':'🇪🇬','Mali':'🇲🇱',
        'Guinea':'🇬🇳','DR Congo':'🇨🇩','Congo':'🇨🇬','Gabon':'🇬🇦','Togo':'🇹🇬',
        'Burkina Faso':'🇧🇫','China':'🇨🇳','Iran':'🇮🇷','Iraq':'🇮🇶','Saudi Arabia':'🇸🇦',
        'Liberia':'🇱🇷','Jamaica':'🇯🇲','Trinidad and Tobago':'🇹🇹','Albania':'🇦🇱','Georgia':'🇬🇪',
        'Iceland':'🇮🇸','Luxembourg':'🇱🇺','Zambia':'🇿🇲','Zimbabwe':'🇿🇼',
    }
    nat = p.get('NATIONALITY', '')
    nat_flag = nat_flags.get(nat, '🏳️')
    foot = p.get('STRONG FOOT', 'R')
    age = g(p, 'AGE')

    proc.append({
        'name': p.get('NAME', ''),
        'team': p.get('CLUB TEAM', ''),
        'pos': pos,
        'pos2': pos2,
        'ovr': ovr,  # NEW: FIFA-style OVR
        'nat': nat_flag,
        'nat_name': nat,
        'foot': foot,
        'age': age,
        'score': legacy_score,  # Legacy for position rankings
        'speed': g(p, 'TOP SPEED'),
        'acceleration': g(p, 'ACCELERATION'),
        'dribble': g(p, 'DRIBBLE ACCURACY'),
        'dribble_speed': g(p, 'DRIBBLE SPEED'),
        'shot': g(p, 'SHOT ACCURACY'),
        'shot_power': g(p, 'SHOT POWER'),
        'shot_technique': g(p, 'SHOT TECHNIQUE'),
        'free_kick': g(p, 'FREE KICK ACCURACY'),
        'swerve': g(p, 'SWERVE'),
        'defense': g(p, 'DEFENSE'),
        'heading': g(p, 'HEADING'),
        'jump': g(p, 'JUMP'),
        'gk': g(p, 'GOAL KEEPING'),
        'technique': g(p, 'TECHNIQUE'),
        'attack': g(p, 'ATTACK'),
        's_pass': g(p, 'SHORT PASS ACCURACY'),
        's_pass_spd': g(p, 'SHORT PASS SPEED'),
        'l_pass': g(p, 'LONG PASS ACCURACY'),
        'l_pass_spd': g(p, 'LONG PASS SPEED'),
        'stamina': g(p, 'STAMINA'),
        'balance': g(p, 'BALANCE'),
        'response': g(p, 'RESPONSE'),
        'agility': g(p, 'AGILITY'),
        'aggression': g(p, 'AGGRESSION'),
        'mentality': g(p, 'MENTALITY'),
        'teamwork': g(p, 'TEAM WORK'),
        'consistency': g(p, 'CONSISTENCY'),
        'condition': g(p, 'CONDITION / FITNESS'),
    })

# By position (sorted by legacy score for differentiation)
bypos = defaultdict(list)
for p in proc:
    bypos[p['pos']].append(p.copy())
for pos in bypos:
    bypos[pos] = sorted(bypos[pos], key=lambda x: x['score'], reverse=True)

# Overall top 100 (sorted by NEW OVR)
top100 = sorted([p.copy() for p in proc], key=lambda x: x['ovr'], reverse=True)[:100]

# By team (average OVR) — only from SITE_TEAMS to avoid unworked teams flooding the list
byteam_d = defaultdict(list)
for p in proc:
    if p['team']:
        byteam_d[p['team']].append(p)

# All players from WORKED site teams only (for skill rankings)
SITE_TEAMS = {'Atalanta', 'Arsenal', 'Ajax', 'Feyenoord', 'PSV Eindhoven', 'Real Madrid', 'Inter', 'Milan', 'Juventus', 'Fiorentina', 'Genoa', 'Lazio', 'Cagliari', 'Roma', 'Brescia', 'Lecce', 'Liverpool', 'Manchester United', 'Bari'}
all_site_players = sorted([p.copy() for p in proc if p['team'] in SITE_TEAMS], key=lambda x: x['ovr'], reverse=True)
byteam = []
for t, ps in byteam_d.items():
    if len(ps) >= 5:
        avg = sum(x['ovr'] for x in ps) / len(ps)
        byteam.append({
            'team': t,
            'avg_score': int(avg),
            'players': sorted(ps, key=lambda x: x['ovr'], reverse=True)
        })
# Ensure all SITE_TEAMS are included, then fill up to 50 with others
site_byteam = [bt for bt in byteam if bt['team'] in SITE_TEAMS]
other_byteam = sorted([bt for bt in byteam if bt['team'] not in SITE_TEAMS], key=lambda x: x['avg_score'], reverse=True)
remaining = max(0, 50 - len(site_byteam))
byteam = sorted(site_byteam + other_byteam[:remaining], key=lambda x: x['avg_score'], reverse=True)

# Output
out = {
    'overall': top100,
    'all_players': all_site_players,
    'by_position': dict(bypos),
    'by_team': byteam,
    'pos_names': NAMES,
    'formulas': FORMULAS
}

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Saved to {OUT}")
print("\n" + "="*50)
print("HYBRID OVR SYSTEM - TOP 20 OVERALL")
print("="*50)
for i, p in enumerate(top100[:20], 1):
    print(f"{i:2}. {p['ovr']:2} OVR - {p['name']:20} ({p['pos']:3}) - {p['team']}")

print("\n" + "="*50)
print("BY POSITION - TOP 5 EACH")
print("="*50)
for pos in ['GK', 'CB', 'SB', 'DMF', 'CMF', 'SMF', 'AMF', 'SS', 'CF']:
    players = bypos.get(pos, [])
    if players:
        print(f"\n{pos} ({NAMES.get(pos, '')}):")
        for i, p in enumerate(players[:5], 1):
            print(f"  {i}. {p['ovr']:2} OVR - {p['name']} ({p['team']})")
