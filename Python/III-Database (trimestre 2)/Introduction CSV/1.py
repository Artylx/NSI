import csv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

f = open((Path(__file__).parent.parent / "Data" / "villes_virgule.csv").resolve(), 'r', encoding='utf-8')

les_lignes = csv.reader(f)

table = []
for line in les_lignes:
    table.append(line)

f.close()

for row in table:
    if row[1] == 'Albi':
        print(f"La ville {row[1]} a une population de {row[8]} habitants.")