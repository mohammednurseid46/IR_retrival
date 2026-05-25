import json
from pathlib import Path
p = Path('src/translation/bilingual_dict.json')
if not p.exists():
    data = {'en_to_am':{}, 'am_to_en':{}}
else:
    data = json.loads(p.read_text(encoding='utf-8'))

# Add mappings
extras_en_to_am = {
    'bahir': ['ባህር'],
    'dar': ['ዳር'],
    'bahir dar': ['ባህር ዳር'],
    'bahir dar university': ['ባህር ዳር ዩኒቨርሲቲ'],
    'university': ['ዩኒቨርሲቲ'],
    'lake tana': ['ጣና ሐይቅ']
}
extras_am_to_en = {
    'ባህር': ['bahir'],
    'ዳር': ['dar'],
    'ባህር ዳር': ['bahir dar'],
    'ባህር ዳር ዩኒቨርሲቲ': ['bahir dar university'],
    'ዩኒቨርሲቲ': ['university'],
    'ጣና ሐይቅ': ['lake tana']
}

for k,v in extras_en_to_am.items():
    data.setdefault('en_to_am', {})
    if k not in data['en_to_am']:
        data['en_to_am'][k] = v

for k,v in extras_am_to_en.items():
    data.setdefault('am_to_en', {})
    if k not in data['am_to_en']:
        data['am_to_en'][k] = v

p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print('Updated bilingual dictionary with extra terms.')
