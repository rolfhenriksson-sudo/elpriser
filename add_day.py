#!/usr/bin/env python3
"""Lägg till en dags timpriser (SE3) i data.json, committa och pusha.
Användning: python3 /workspace/elpriser/add_day.py YYYY-MM-DD [--no-push] [--force]
Befintliga dagar tas aldrig bort. Finns dagen redan hoppas den över (om inte --force)."""
import json, sys, subprocess, os, datetime
from collections import OrderedDict

REPO = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(REPO, 'data.json')

def fetch(day):
    y, m, d = day.split('-')
    url = f'https://www.elprisetjustnu.se/api/v1/prices/{y}/{m}-{d}_SE3.json'
    out = subprocess.run(['curl', '-sf', '-A', 'Mozilla', url], capture_output=True, text=True)
    if out.returncode != 0 or not out.stdout.strip():
        sys.exit(f'Fel: kunde inte hämta {url} (curl {out.returncode})')
    rows = json.loads(out.stdout)
    hours = OrderedDict()  # nyckel = time_start utan minuter (inkl. tidszon, så sommartidsbytet ger 25/23 timmar)
    for r in rows:
        key = r['time_start'][:13] + r['time_start'][19:]
        hours.setdefault(key, []).append(r['SEK_per_kWh'])
    vals = [round(sum(v) / len(v) * 100) for v in hours.values()]
    if len(vals) not in (23, 24, 25):
        sys.exit(f'Fel: oväntat antal timmar ({len(vals)}) för {day}')
    return vals

def save(data):
    items = sorted(data.items())
    with open(DATA, 'w') as f:
        f.write('{\n' + ',\n'.join(f'"{k}":{json.dumps(v, separators=(",", ":"))}' for k, v in items) + '\n}\n')

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 1:
        sys.exit(__doc__)
    day = args[0]
    datetime.date.fromisoformat(day)
    data = json.load(open(DATA)) if os.path.exists(DATA) else {}
    if day in data and '--force' not in sys.argv:
        print(f'{day} finns redan, inget att göra.')
    else:
        data[day] = fetch(day)
        save(data)
        print(f'{day}: {data[day]}')
    if '--no-push' in sys.argv:
        return
    os.chdir(REPO)
    subprocess.run(['git', 'add', 'data.json'], check=True)
    if subprocess.run(['git', 'diff', '--cached', '--quiet']).returncode:
        subprocess.run(['git', 'commit', '-q', '-m', f'Uppdatera elpriser {day}'], check=True)
        subprocess.run(['git', 'push', '-q'], check=True)
        print('Pushat.')

if __name__ == '__main__':
    main()
