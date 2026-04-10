import csv
from pathlib import Path

csv_path = Path('/Users/ziotore/Desktop/use_this_file.csv')
with csv_path.open(newline='', encoding='latin-1') as f:
    rows = list(csv.DictReader(f))
fieldnames = list(rows[0].keys())

updates = {
    '305': 'B',
    '307': 'R',
    '631': 'C',
    '700': 'C',
    '1036': 'C',
    '1039': 'R',
    '1043': 'C',
    '1393': 'C',
    '1395': 'C',
    '1397': 'C',
    '1418': 'C',
    '1424': 'C',
    '1426': 'C',
    '1470': 'L',
    '1769': 'C',
    '2312': 'C',
    '2541': 'L',
    '2542': 'L',
    '2543': 'C',
    '2545': 'L',
    '2546': 'C',
    '2549': 'C',
    '2616': 'L',
    '2728': 'C',
    '3012': 'C',
    '3019': 'L',
    '4372': 'L',
    '4475': 'R',
    '4478': 'C',
    '4486': 'L',
    '4523': 'C',
    '4571': 'R',
}

for row in rows:
    if row['ID'] in updates:
        row['FAVOURED SIDE'] = updates[row['ID']]

with csv_path.open('w', newline='', encoding='latin-1') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader(); w.writerows(rows)

print('updated', len(updates), 'Milan preferred sides')
