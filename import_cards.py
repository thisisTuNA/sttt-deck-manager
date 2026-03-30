import os
import re

# Read TSV file
with open('cardlist.tsv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

cards = []
card_id = 1

# Skip header (line 0)
for line in lines[1:]:
    parts = line.strip().split('\t')
    if len(parts) < 9:
        continue
    
    dex_num = parts[0].strip()
    stt = parts[1].strip()
    card_type = parts[2].strip()
    color = parts[3].strip()
    cost = parts[4].strip()
    rarity = parts[5].strip()
    name = parts[6].strip()
    race = parts[7].strip() if len(parts) > 7 else ""
    mua = parts[8].strip() if len(parts) > 8 else "STTT"
    
    # Map rarity: S, SS, 2S, 3S, 4S, 5S -> EX
    if rarity in ['S', 'SS', '2S', '3S', '4S', '5S']:
        rarity = 'EX'
    
    # Determine image path based on STT and set
    # STT is the sequential number, use it for image file
    image_path = ""
    if mua == "STTT":
        image_path = f"Images/STTT/{stt}.png"
    elif mua == "DTGL":
        image_path = f"Images/DTGL/{stt}.jpg"
    
    card = {
        'id': card_id,
        'code': stt,
        'name': name,
        'type': card_type,
        'color': color,
        'rarity': rarity,
        'cost': cost,
        'race': race,
        'set': mua,
        'image': image_path
    }
    
    cards.append(card)
    card_id += 1

# Generate JavaScript file
js_content = "const CARDS_DATA = [\n"

for i, card in enumerate(cards):
    name_escaped = card['name'].replace('"', '\\"')
    race_escaped = card['race'].replace('"', '\\"')
    
    js_content += "  {\n"
    js_content += f"    \"id\": {card['id']},\n"
    js_content += f"    \"code\": \"{card['code']}\",\n"
    js_content += f"    \"name\": \"{name_escaped}\",\n"
    js_content += f"    \"type\": \"{card['type']}\",\n"
    js_content += f"    \"color\": \"{card['color']}\",\n"
    js_content += f"    \"rarity\": \"{card['rarity']}\",\n"
    js_content += f"    \"cost\": \"{card['cost']}\",\n"
    js_content += f"    \"race\": \"{race_escaped}\",\n"
    js_content += f"    \"set\": \"{card['set']}\",\n"
    js_content += f"    \"image\": \"{card['image']}\"\n"
    js_content += "  }"
    
    if i < len(cards) - 1:
        js_content += ","
    js_content += "\n"

js_content += "];\n"

# Write to file
with open('cards-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ Generated {len(cards)} cards to cards-data.js")

# Check for missing images
print("\n📊 Checking images...")
sttt_images = set()
dtgl_images = set()

if os.path.exists('Images/STTT'):
    for f in os.listdir('Images/STTT'):
        if f.endswith('.png'):
            num = f.replace('.png', '')
            sttt_images.add(num)

if os.path.exists('Images/DTGL'):
    for f in os.listdir('Images/DTGL'):
        if f.endswith('.jpg'):
            num = f.replace('.jpg', '')
            dtgl_images.add(num)

print(f"Found {len(sttt_images)} STTT images")
print(f"Found {len(dtgl_images)} DTGL images")

# Find cards without images
missing = []
for card in cards:
    if card['set'] == 'STTT':
        if card['code'] not in sttt_images:
            missing.append(card)
    elif card['set'] == 'DTGL':
        if card['code'] not in dtgl_images:
            missing.append(card)

if missing:
    print(f"\n⚠️  {len(missing)} cards without images:\n")
    for card in missing:
        print(f"  • {card['code']}: {card['name']} ({card['type']}) - {card['set']}")
else:
    print("\n✅ All cards have images!")
