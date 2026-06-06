import os, json, csv
from pathlib import Path

DB_PATH = "БД"
OUTPUT = "db_index.json"
index = {"files": []}

for root, dirs, files in os.walk(DB_PATH):
    for f in files:
        ext = Path(f).suffix.lower()
        fp = os.path.join(root, f)
        rows = []
        try:
            if ext == '.csv':
                with open(fp, 'r', encoding='utf-8', errors='ignore') as cf:
                    for row in csv.reader(cf):
                        line = ' '.join(str(c) for c in row if c).strip()
                        if line: rows.append(line[:500])
            elif ext == '.json':
                with open(fp, 'r', encoding='utf-8', errors='ignore') as jf:
                    content = jf.read()
                for line in content.split('\n'):
                    line = line.strip()
                    if line and len(line) > 5: rows.append(line[:500])
            elif ext in ['.txt', '.log', '.sql', '.xml']:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as tf:
                    for line in tf:
                        line = line.strip()
                        if line: rows.append(line[:500])
                        if len(rows) >= 5000: break
            if rows:
                index["files"].append({"name": f, "rows": rows[:5000]})
                print(f"  {f}: {len(rows)} строк")
        except Exception as e:
            print(f"  ❌ {f}: {e}")

with open(OUTPUT, 'w', encoding='utf-8') as out:
    json.dump(index, out, ensure_ascii=False)
print(f"\n✅ {OUTPUT}: {len(index['files'])} файлов")