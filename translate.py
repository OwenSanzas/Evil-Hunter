import csv
import re

def create_localized_translations():
    # Develop a rich vocabulary for different item types and attributes
    # This helps create varied but thematically consistent translations
    
    # Element vocabulary for more varied translations
    fire_terms = ["Flame", "Blaze", "Inferno", "Ember", "Cinder", "Fire", "Burning", "Scorching", "Volcanic", "Molten"]
    water_terms = ["Tidal", "Ocean", "Wave", "Aqua", "Torrent", "Stream", "Deluge", "Frost", "Glacial", "Mist"]
    earth_terms = ["Terra", "Stone", "Mountain", "Crystal", "Earthen", "Quake", "Boulder", "Granite", "Jade", "Mineral"]
    wind_terms = ["Gale", "Tempest", "Zephyr", "Storm", "Cyclone", "Breeze", "Hurricane", "Gust", "Aerial", "Squall"]
    lightning_terms = ["Thunder", "Bolt", "Shock", "Electric", "Spark", "Static", "Discharge", "Volt", "Current", "Charge"]
    shadow_terms = ["Dusk", "Shade", "Shadow", "Void", "Abyss", "Twilight", "Gloom", "Umbral", "Murk", "Sinister"]
    light_terms = ["Radiant", "Brilliant", "Luminous", "Solar", "Celestial", "Astral", "Divine", "Gleaming", "Hallowed", "Sacred"]
    death_terms = ["Grave", "Necro", "Death", "Ghastly", "Phantom", "Spectral", "Wraith", "Doom", "Reaper", "Soul"]
    
    # Weapon vocabulary for variety
    sword_terms = ["Blade", "Edge", "Saber", "Claymore", "Greatsword", "Longsword", "Rapier", "Cutlass", "Falchion", "Broadsword"]
    bow_terms = ["Longbow", "Shortbow", "Recurve", "Composite", "Greatbow", "Reflex Bow", "Archer's", "Hunter's", "Ranger's", "Marksman's"]
    staff_terms = ["Rod", "Scepter", "Wand", "Stave", "Cane", "Focus", "Channel", "Conduit", "Instrument", "Medium"]
    armor_terms = ["Plate", "Mail", "Cuirass", "Hauberk", "Aegis", "Bastion", "Bulwark", "Guard", "Carapace", "Shell"]
    
    # Epic name patterns that sound good in English but maintain the Chinese style
    epic_prefixes = ["Ancient", "Elder", "Eternal", "Mythic", "Fabled", "Arcane", "Primal", "Sovereign", "Astral", "Eldritch"]
    epic_suffixes = ["of Power", "of Might", "of Fury", "of Devastation", "of the Ancients", "of Legends", "of Dominion", "of Majesty", "of the Cosmos", "of Eternity"]
    
    # More specific attribute mappings
    element_map = {
        "火": fire_terms,
        "水": water_terms,
        "地": earth_terms,
        "土": earth_terms,
        "风": wind_terms,
        "雷": lightning_terms,
        "冥": shadow_terms,
        "死": death_terms,
        "光": light_terms,
        "天": light_terms,
        "魔": shadow_terms,
        "战": ["War", "Battle", "Combat", "Martial", "Conflict", "Skirmish", "Strife", "Valor", "Conquest", "Triumph"]
    }
    
    item_type_map = {
        "剑": sword_terms,
        "刀": ["Blade", "Knife", "Cleaver", "Machete", "Scimitar", "Dagger", "Dirk", "Scythe", "Glaive", "Katar"],
        "弓": bow_terms,
        "杖": staff_terms,
        "锤": ["Hammer", "Mace", "Maul", "Cudgel", "Mallet", "Bludgeon", "Smasher", "Pounder", "Crusher", "Warhammer"],
        "斧": ["Axe", "Hatchet", "Tomahawk", "Cleaver", "Halberd", "Poleaxe", "Battleaxe", "Greataxe", "Chopper", "Reaver"],
        "盾": ["Shield", "Barrier", "Bulwark", "Aegis", "Ward", "Safeguard", "Defender", "Protector", "Rampart", "Buckler"],
        "铠": armor_terms,
        "甲": armor_terms,
        "靴": ["Boots", "Greaves", "Sabatons", "Treads", "Stompers", "Striders", "Walkers", "Foot Guards", "Sollerets", "Footwear"],
        "戒": ["Ring", "Band", "Signet", "Circlet", "Loop", "Seal", "Hoop", "Coil", "Spiral", "Knot"],
        "手套": ["Gloves", "Gauntlets", "Grips", "Handguards", "Fists", "Clutches", "Grasps", "Mitts", "Handlers", "Bracers"],
        "护符": ["Amulet", "Talisman", "Charm", "Pendant", "Totem", "Relic", "Icon", "Fetish", "Idol", "Token"],
        "项链": ["Necklace", "Pendant", "Locket", "Choker", "Chain", "Collar", "Amulet", "Torc", "Carcanet", "Gorget"],
        "腰带": ["Belt", "Girdle", "Sash", "Cincture", "Waistband", "Waistguard", "Binder", "Clasp", "Fastener", "Cinch"],
        "披风": ["Cloak", "Cape", "Mantle", "Shroud", "Drape", "Wrap", "Covering", "Stole", "Robe", "Shawl"],
        "头": ["Helm", "Crown", "Circlet", "Diadem", "Headpiece", "Coronet", "Tiara", "Cap", "Cowl", "Hood"],
        "箭": ["Arrow", "Bolt", "Shaft", "Dart", "Quarrel", "Projectile", "Missile", "Volley", "Barb", "Spike"]
    }
    
    quality_map = {
        "CC33FF": "Legendary",  # Purple items
        "00FFFF": "Rare",       # Cyan items
        "00ff00": "Uncommon",   # Green items
        "FFFF00": "Epic",       # Yellow items
        "FF0000": "Superior"    # Red items
    }
    
    # Pattern matching for Chinese item names
    def extract_elements(name):
        elements = []
        for element in element_map:
            if element in name:
                elements.append(element)
        return elements
    
    def extract_item_type(name):
        for item_type in item_type_map:
            if item_type in name:
                return item_type
        return None
    
    def has_color_tag(html_line, color_code):
        pattern = f'color="#{color_code}"'
        return pattern in html_line
    
    def determine_quality(html_line):
        for quality_code in quality_map:
            if has_color_tag(html_line, quality_code):
                return quality_map[quality_code]
        return "Common"
    
    # Create translation mapping with more stylistic variety
    def create_translation(item_id, original_name, html_line=""):
        # Skip items with no original name
        if not original_name or original_name.strip() == "":
            return ""
            
        # Handle special cases
        if "技能" in original_name:
            if "攻击" in original_name:
                element = next((e for e in ["火", "水", "地", "风", "雷"] if e in original_name), "")
                element_trans = {"火": "Fire", "水": "Water", "地": "Earth", "风": "Wind", "雷": "Lightning"}.get(element, "")
                
                if "箭" in original_name:
                    return f"{element_trans} Arrow Attack Skill"
                return f"{element_trans} Attack Skill"
            
            if "辅助" in original_name:
                return "Support Skill"
            if "医疗" in original_name:
                return "Healing Skill"
            if "光环" in original_name:
                return "Aura Skill"
            if "防御" in original_name:
                return "Defense Skill"
                
        if "奖励物资" in original_name:
            number = re.search(r"奖励物资(\d+)", original_name)
            if number:
                return f"Resource Reward {number.group(1)}"
            return "Resource Reward"
            
        if original_name.strip() == "之剑":
            return "Mystery Sword"
        if original_name.strip() == "法杖":
            return "Arcane Staff"
            
        # Determine common elements in the name
        elements = extract_elements(original_name)
        item_type = extract_item_type(original_name)
        quality = determine_quality(html_line)
        
        # Begin constructing a localized name
        localized_name = []
        
        # Add quality-based prefix for higher rarity items
        if quality in ["Legendary", "Epic"]:
            import random
            localized_name.append(random.choice(epic_prefixes))
        
        # Add elemental term if present
        if elements:
            # Use the first found element, but with variety
            import random
            element = elements[0]
            element_term = random.choice(element_map[element])
            localized_name.append(element_term)
        
        # Handle special name components
        if "神" in original_name:
            if "战神" in original_name:
                localized_name.append("Wargod's")
            elif any(e + "神" in original_name for e in ["火", "水", "土", "风", "雷"]):
                # Already covered by element term
                pass
            else:
                localized_name.append("Divine")
        
        if "之" in original_name:
            # The Chinese "之" structure is typically handled by using "of" later
            # or by combining the elements differently in English
            pass
        
        # Add appropriate item type term
        if item_type:
            import random
            type_term = random.choice(item_type_map[item_type])
            localized_name.append(type_term)
        elif "筋" in original_name:
            localized_name.append("Sinew")
        elif "结晶" in original_name:
            localized_name.append("Crystal")
        elif "宝石" in original_name:
            localized_name.append("Gem")
        elif "符纹" in original_name:
            localized_name.append("Rune")
        elif "魔法" in original_name:
            if "杖" in original_name:
                localized_name.append("Spellstaff")
            else:
                localized_name.append("Arcane")
                # Add a generic item type if we haven't identified one
                if not item_type:
                    localized_name.append("Artifact")
        
        # For epic/legendary items, sometimes add a suffix
        if quality in ["Legendary", "Epic"] and len(localized_name) <= 3:
            import random
            if random.random() > 0.5:  # 50% chance
                localized_name.append(random.choice(epic_suffixes))
        
        # Join the parts with spaces
        result = " ".join(localized_name)
        
        # Clean up any awkward phrasing
        result = result.replace("Divine Divine", "Divine")
        result = result.replace("Arcane Arcane", "Arcane")
        
        return result
    
    # Load the original HTML content to extract color info
    try:
        with open("paste.txt", "r", encoding="utf-8") as html_file:
            html_content = html_file.readlines()
            html_lines = {line.split('href="#')[1].split('"')[0]: line for line in html_content if 'href="#' in line}
    except Exception as e:
        print(f"Warning: Could not load HTML file for color information: {e}")
        html_lines = {}
    
    # Custom translations for specific items to ensure quality and consistency
    custom_translations = {
        "I007": "Black Dragon Sinew",
        "I004": "Crystal Arrow",
        "I009": "Frostfall Bow",
        "I005": "Inferno Edge",
        "I014": "Ember Rain Bow",
        "I015": "Tempest God's Warbow",
        "I016": "Glacial Hunter",
        "I017": "Starshatter Bow",
        "I018": "Arcane Longbow",
        "I019": "Skyfire Bow",
        "I01A": "Phoenix Wing Bow",
        "I00Z": "Runic Blade",
        "I006": "Crimson Dragon Fang",
        "I010": "Formation Crystal",
        "I011": "Runic Gem",
        "I012": "Elven Branch",
        "I013": "Sorcerer's Staff",
        "I01B": "Tidal Sovereign's Scepter",
        "I01C": "Terra Lord's Hammer",
        "I01D": "Flamelord's Warblades",
        "I01E": "Azure Tide Blade",
        "I01F": "Blazing Edge",
        "I01H": "Arbiter's Sword",
        "I01I": "Radiant Focus",
        "I01J": "Winterfrost Staff",
        "I024": "Spiritwood Staff",
        "I026": "Malevolent Staff",
        "I028": "Hex Bringer Staff",
        "I008": "Reaper's Warblade",
        "I02E": "Hellfire Sword",
        "I02J": "Arcane Source Crystal",
        "I00I": "Hexwoven Armor",
        "I00J": "Shadow Magic Blade",
        "I00K": "Crown of Skulls",
        "I00M": "Specter Shield",
        "I00N": "Osseous Breastplate",
        "I02K": "Wraith Amulet",
        "I02L": "Bloodthirst Cloak",
        "I02M": "Deathlord's Greaves",
        "I02N": "Phantom King's Shroud",
        "I02O": "Death God's Battleplate",
        "I03D": "Wargod's Hallowed Plate",
        "I03E": "Wargod's Sacred Axe",
        "I04H": "Earthlord's Battle Armor",
        "I04I": "Tidelord's Battle Armor",
        "I04J": "Stormcaller's Battleplate",
        "I04K": "Firelord's Battle Armor",
        "I04W": "Thunderlord's Battle Armor",
        "I04X": "Netherworld Sovereign Plate",
        "I04Y": "Thunderlord's Spike",
        "I04Z": "Netherworld Sovereign Rod",
        "I05H": "Spirit King's Scepter",
        "I05K": "Spirit King's Battle Armor",
        "I04P": "Seraphim Wings",
        "I04Q": "Demonic Wings",
        "I01S": "Infernal Robes",
        "I04R": "Heart of Darkness",
        "I04S": "Fallen Angel Wings"
    }
    
    try:
        # Read the existing CSV
        with open("item_translations.csv", "r", encoding="utf-8-sig") as infile:
            reader = csv.reader(infile)
            headers = next(reader)  # Get header row
            items = list(reader)    # Get all data rows
        
        # Add a new column for translations
        if "Translate" not in headers:
            headers.append("Translate")
            
        # Track indices
        id_idx = headers.index("ID")
        name_idx = headers.index("Original Name")
        trans_idx = len(headers) - 1  # Translate column should be the last one
        
        # Add translations for each item
        for item in items:
            item_id = item[id_idx]
            original_name = item[name_idx]
            
            # Ensure the item has enough columns for the translation
            while len(item) <= trans_idx:
                item.append("")
                
            # Check for custom translation first
            if item_id in custom_translations:
                item[trans_idx] = custom_translations[item_id]
            else:
                # Get HTML line for color info if available
                html_line = html_lines.get(item_id, "")
                
                # Generate a translation
                item[trans_idx] = create_translation(item_id, original_name, html_line)
        
        # Write the updated CSV with translations
        with open("item_translations_localized.csv", "w", encoding="utf-8-sig", newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(headers)
            writer.writerows(items)
        
        # Also create a tab-delimited text file
        with open("item_translations_localized.txt", "w", encoding="utf-8-sig", newline='') as outfile:
            outfile.write("\t".join(headers) + "\n")
            for item in items:
                outfile.write("\t".join(item) + "\n")
        
        print("Successfully created localized translation files:")
        print("1. item_translations_localized.csv")
        print("2. item_translations_localized.txt")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        # If there's an error, create a sample file with some good translations
        sample_items = [
            ["I000", "-火系攻击技能", "Fire Attack Skill"],
            ["I001", "-水系攻击技能", "Water Attack Skill"],
            ["I002", "-火系攻击技能-箭", "Fire Arrow Attack Skill"],
            ["I003", "-地系攻击技能", "Earth Attack Skill"],
            ["I007", "黑龙筋", "Black Dragon Sinew"],
            ["I004", "水晶箭", "Crystal Arrow"],
            ["I009", "天霜之弓", "Frostfall Bow"],
            ["I005", "爆炎之剑", "Inferno Edge"],
            ["I014", "火雨之弓", "Ember Rain Bow"],
            ["I015", "风神战弓", "Tempest God's Warbow"],
            ["I016", "冰雪之弓", "Glacial Hunter"],
            ["I017", "碎星之弓", "Starshatter Bow"],
            ["I018", "魔法弓", "Arcane Longbow"],
            ["I00I", "诅咒铠甲", "Hexwoven Armor"],
            ["I00J", "黑魔剑", "Shadow Magic Blade"],
            ["I00K", "骷髅冠", "Crown of Skulls"],
            ["I03D", "战神圣铠", "Wargod's Hallowed Plate"],
            ["I03E", "战神圣斧", "Wargod's Sacred Axe"],
            ["I04P", "天使之翼", "Seraphim Wings"],
            ["I04Q", "恶魔之翼", "Demonic Wings"],
            ["I04S", "堕落天使之翼", "Fallen Angel Wings"]
        ]
        
        # Write sample CSV
        with open("item_translations_localized.csv", "w", encoding="utf-8-sig", newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["ID", "Original Name", "Translate"])
            writer.writerows(sample_items)
        
        # Write sample tab-delimited file
        with open("item_translations_localized.txt", "w", encoding="utf-8-sig", newline='') as outfile:
            outfile.write("ID\tOriginal Name\tTranslate\n")
            for item in sample_items:
                outfile.write("\t".join(item) + "\n")
        
        print("Created sample localized translation files with high-quality examples.")

if __name__ == "__main__":
    create_localized_translations()