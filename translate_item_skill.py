import re
import os
import shutil

def translate_skill_names(input_file):
    # Create a backup of the original file
    if os.path.exists(input_file):
        backup_path = input_file + ".backup"
        shutil.copy2(input_file, backup_path)
        print(f"Backup created at: {backup_path}")
    
    # Define the skill name translations
    skill_translations = {
        "爆炎地狱": "Infernal Eruption",
        "陨石火雨": "Meteor Shower",
        "神罚·罡风雷暴": "Smite: Tempest Fury",
        "风暴强袭": "Storm Assault",
        "神技·龙卷风暴": "Divine: Cyclone Rage",
        "千里冰封": "Endless Frost",
        "碎星之雨": "Starshard Rain",
        "烈焰焚天": "Heaven Scorcher",
        "凤炽天翔": "Phoenix Ascension",
        "神罚·冰霜封冻": "Smite: Glacial Prison",
        "神技·天降甘霖": "Divine: Heaven's Deluge",
        "神罚·诺姆之怒": "Smite: Gnome's Fury",
        "神技·裂地之牙": "Divine: Earth Fangs",
        "神罚·红莲业火": "Smite: Crimson Inferno",
        "神技·炎之炼狱": "Divine: Flame Purgatory",
        "碧波荡漾": "Azure Tidal Wave",
        "灼热闪电": "Searing Bolt",
        "裁决之光": "Judgment Beam",
        "圣光降临": "Radiance Descends",
        "暴风雪": "Blizzard",
        "闪电麻痹": "Lightning Strike",
        "召唤鬼龙": "Phantom Drake",
        "神之庇护·天降甘霖": "Aegis: Heaven's Deluge",
        "树根缠绕": "Root Snare",
        "天火燎原": "Skyfire Blaze",
        "邪恶气息": "Malice Aura",
        "诅咒敌人": "Doom Curse",
        "破军之阵": "Formation Breaker",
        "雷暴轰炸": "Thunder Barrage",
        "神罚·鬼哭神嚎": "Smite: Phantom Wail",
        "魔技·天魔噬魂": "Dark Art: Soul Reaper",
        "亡灵天灾": "Undead Cataclysm",
        "战神技·狂战八方": "Wargod: Omnislash",
        "战神技·冲锋陷阵": "Wargod: Vanguard Charge",
        "神罚·雷之领域": "Smite: Thunder Domain",
        "神技·雷蛇乱舞": "Divine: Lightning Serpents",
        "神罚·地狱死魂炮": "Smite: Soul Cannon",
        "神技·血腥之舞": "Divine: Blood Dance",
        "神罚·落叶飞花": "Smite: Petal Storm",
        "神技·梦幻之花": "Divine: Ethereal Bloom"
    }
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'gbk', 'gb18030']
        content = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                with open(input_file, 'r', encoding=encoding) as file:
                    content = file.read()
                used_encoding = encoding
                print(f"Successfully read file using encoding: {encoding}")
                break
            except Exception as e:
                print(f"Failed to read with encoding {encoding}: {e}")
        
        if content is None:
            print("Failed to read input file with any encoding.")
            return
        
        # Sort keys by length (longest first) to avoid partial replacements
        sorted_keys = sorted(skill_translations.keys(), key=len, reverse=True)
        
        # Apply all translations
        replacements = []
        for chinese_name in sorted_keys:
            english_name = skill_translations[chinese_name]
            
            # Count occurrences before replacement
            count = content.count(chinese_name)
            if count > 0:
                # Perform the replacement
                content = content.replace(chinese_name, english_name)
                replacements.append((chinese_name, english_name, count))
        
        # Write the translated content back to the file
        with open(input_file, 'w', encoding=used_encoding) as file:
            file.write(content)
        
        # Report results
        print("\nTranslation Summary:")
        print(f"Total skill names: {len(skill_translations)}")
        print(f"Skills that were found and replaced: {len(replacements)}")
        print("\nSkills replaced:")
        for chinese, english, count in replacements:
            print(f"  '{chinese}' → '{english}' ({count} occurrences)")
        
        print("\nSkills not found in the file:")
        not_found = set(skill_translations.keys()) - set(item[0] for item in replacements)
        for chinese in not_found:
            print(f"  '{chinese}' → '{skill_translations[chinese]}'")
            
        print("\nReplacement complete!")
            
    except Exception as e:
        print(f"Error processing file: {e}")
        print("Restoring backup...")
        try:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, input_file)
                print("Backup restored.")
        except Exception as restore_error:
            print(f"Error restoring backup: {restore_error}")

def main():
    # Ask for the input file
    input_file = input("Enter path to the file with skill names: ")
    
    if not input_file:
        print("No file path provided. Exiting.")
        return
    
    translate_skill_names(input_file)

if __name__ == "__main__":
    main()