import re
import os
import shutil

def translate_item_descriptions(input_file, output_file):
    # Create a backup of the original file
    if os.path.exists(input_file):
        backup_path = input_file + ".backup"
        shutil.copy2(input_file, backup_path)
        print(f"Backup created at: {backup_path}")
    
    # Define translation templates with regex patterns
    # Each pattern will capture the numeric values to preserve them
    # Using gaming abbreviations: dmg (damage), regen (regeneration), hp (health points)
    translation_templates = [
        # New templates
        # 1. 防御提升50点
        (r'防御提升(\d+)点', r'+\1 Armor'),
        
        # 2. 攻击使敌人神经错乱，减缓攻速移速
        (r'攻击使敌人神经错乱，减缓攻速移速', r'Attacks slow enemy attack and movement speed'),
        
        # 3. 20%机率造成3倍对敌伤害
        (r'(\d+)%机率造成3倍对敌伤害', r'\1% chance for 3x dmg'),
        
        # 4. 护甲提升10点
        (r'护甲提升(\d+)点', r'+\1 Armor'),
        
        # 5. 魔法值提升200点
        (r'魔法值提升(\d+)点', r'+\1 Mana'),
        
        # 6. 生命恢复速度提升50%
        (r'生命恢复速度提升(\d+)%', r'+\1% HP regen'),
        
        # 7. 加快少许生命回复速度
        (r'加快少许生命回复速度', r'Slightly increased HP regen'),
        
        # 8. 攻击吸血10%
        (r'攻击吸血(\d+)%', r'\1% Lifesteal'),
        
        # 9. 每次发工资多发1金
        (r'每次发工资多发(\d+)金', r'+\1 Gold per income'),
        
        # 10. 服用可增加1000生命值
        (r'服用可增加(\d+)生命值', r'Use: +\1 HP'),
        
        # 11. 魔法回复速度提升5倍
        (r'魔法回复速度提升(\d+)倍', r'+\1x Mana regen'),
        
        # 12. 增加2倍魔法回复速度
        (r'增加(\d+)倍魔法回复速度', r'+\1x Mana regen'),
        
        # Additional new templates
        # 1. 每秒回复生命100
        (r'每秒回复生命(\d+)', r'+\1 HP regen/sec'),
        
        # 2. 10%机率闪避敌人攻击
        (r'(\d+)%机率闪避敌人攻击', r'\1% Evasion'),
        
        # 3. 减少临近敌人单位护甲50点
        (r'减少临近敌人单位护甲(\d+)点', r'Aura: -\1 Armor to enemies'),
        
        # 4. 防御提升50
        (r'防御提升(\d+)(?!点)', r'+\1 Armor'),
        
        # 5. 增加少许魔法回复速度
        (r'增加少许魔法回复速度', r'Slightly increased Mana regen'),
        
        # 6. 10%格挡敌人攻击
        (r'(\d+)%格挡敌人攻击', r'\1% Block chance'),
        
        # 7. 生命提升200点
        (r'生命提升(\d+)点', r'+\1 HP'),
        
        # 8. 提升移动速度
        (r'提升移动速度', r'+Movement Speed'),
        
        # 9. 增加少许生命回复速度
        (r'增加少许生命回复速度', r'Slightly increased HP regen'),
        
        # 10. 防御值提升10点
        (r'防御值提升(\d+)点', r'+\1 Armor'),
        
        # 11. 魔法力提升200点
        (r'魔法力提升(\d+)点', r'+\1 Mana'),
        
        # 12. 20%机率打出3倍伤害
        (r'(\d+)%机率打出3倍伤害', r'\1% chance for 3x dmg'),
        
        # 13. 防御力提升10
        (r'防御力提升(\d+)(?!点)', r'+\1 Armor'),
        
        # 14. 近身攻击分裂15%
        (r'近身攻击分裂(\d+)%', r'\1% Cleave'),
        
        # 15. 增加生命回复速度
        (r'增加生命回复速度', r'Increased HP regen'),
        
        # More additional templates
        # 1. 每秒对身边单位造成200点火焰伤害
        (r'每秒对身边单位造成(\d+)点火焰伤害', r'Aura: \1 fire dmg/sec to nearby units'),
        
        # 2. 20%机率造成三倍伤害
        (r'(\d+)%机率造成三倍伤害', r'\1% chance for 3x dmg'),
        
        # 3. 看穿敌人弱点虚实，15%机率打出5倍伤害
        (r'看穿敌人弱点虚实，(\d+)%机率打出(\d+)倍伤害', r'\1% chance for \2x critical dmg'),
        
        # 4. 20%机率造成8倍对敌伤害
        (r'(\d+)%机率造成(\d+)倍对敌伤害', r'\1% chance for \2x dmg'),
        
        # 5. 将35%对敌人的伤害值转成自己的生命值
        (r'将(\d+)%对敌人的伤害值转成自己的生命值', r'\1% Lifesteal'),
        
        # 6. 每秒回复50点生命
        (r'每秒回复(\d+)点生命', r'+\1 HP regen/sec'),
        
        # 7. 提升少许魔法回复速度
        (r'提升少许魔法回复速度', r'Slightly increased Mana regen'),
        
        # 8. n增加少许的魔法回复速度
        (r'增加少许的魔法回复速度', r'Slightly increased Mana regen'),
        
        # 9. 魔法提升100点
        (r'魔法提升(\d+)点', r'+\1 Mana'),
        
        # 10. 移动速度下降
        (r'移动速度下降', r'Reduced Movement Speed'),
        
        # Original templates
        # 1. 每次射击能同时攻击7个目标
        (r'每次射击能同时攻击(\d+)个目标', r'Attacks \1 targets per shot'),
        
        # 2. 每秒生命回复100点
        (r'每秒生命回复(\d+)点', r'+\1 HP regen/sec'),
        
        # 3. 力量提升50
        (r'力量提升(\d+)', r'+\1 STR'),
        
        # 4. 敏捷提升50
        (r'敏捷提升(\d+)', r'+\1 AGI'),
        
        # 5. 魔力提升50
        (r'魔力提升(\d+)', r'+\1 Mana'),
        
        # 6. 攻击速度提升40%
        (r'攻击速度提升(\d+)%', r'+\1% Attack Speed'),
        
        # 7. 一定概率发动武器神技--
        (r'一定概率发动武器神技--', r'Chance to proc: '),
        
        # 8. 分裂攻击30%
        (r'分裂攻击(\d+)%', r'\1% Cleave'),
        
        # 9. 每次攻击吸血25%
        (r'每次攻击吸血(\d+)%', r'\1% Lifesteal'),
        
        # 10. 攻击速度提升40% - already covered by #6
        
        # 11. 攻击力提升200
        (r'攻击力提升(\d+)', r'+\1 Dmg'),
        
        # 12. 视野提升500范围
        (r'视野提升(\d+)范围', r'+\1 Vision'),
        
        # 13. 合成公式：
        (r'合成公式：', r'Recipe:'),
        
        # 14. 20%机率造成三倍对敌伤害
        (r'(\d+)%机率造成三倍对敌伤害', r'\1% chance for 3x dmg'),
        
        # 15. 15%机率闪避敌人的攻击
        (r'(\d+)%机率闪避敌人的攻击', r'\1% Evasion'),
        
        # 16. 魔法回复提升1倍
        (r'魔法回复提升(\d+)倍', r'+\1x Mana regen'),
        
        # 17. 智力提升100
        (r'智力提升(\d+)', r'+\1 INT'),
        
        # 18. 被攻击时有15%机率闪避
        (r'被攻击时有(\d+)%机率闪避', r'\1% Evasion'),
        
        # 19. 加快25%的魔法回复速度
        (r'加快(\d+)%的魔法回复速度', r'+\1% Mana regen'),
        
        # 20. 加速魔法值回复
        (r'加速魔法值回复', r'Increased Mana regen'),
        
        # 21. 防御力提升10点
        (r'防御力提升(\d+)点', r'+\1 Armor'),
        
        # 22. 英雄移动速度加快
        (r'英雄移动速度加快', r'+Movement Speed'),
        
        # 23. 每秒对临近敌人单位造成200点伤害
        (r'每秒对临近敌人单位造成(\d+)点伤害', r'Aura: \1 dmg/sec to nearby enemies'),
        
        # 24. 每秒回复生命200点
        (r'每秒回复生命(\d+)点', r'+\1 HP regen/sec'),
        
        # 25. 生命值提升2000点
        (r'生命值提升(\d+)点', r'+\1 HP'),
        
        # 26. 每10秒能隔挡一次指向性魔法攻击
        (r'每(\d+)秒能隔挡一次指向性魔法攻击', r'Spell Block (every \1 sec)'),
        
        # 27. 范围内减防150点，不分敌我
        (r'范围内减防(\d+)点，不分敌我', r'Aura: -\1 Armor to all units'),
        
        # 28. 持有者每秒损血100点
        (r'持有者每秒损血(\d+)点', r'Drains \1 HP/sec from bearer'),
        
        # 29. 移动速度最大化提升
        (r'移动速度最大化提升', r'Max Movement Speed'),
        
        # 30. 减少附近敌人50点防御
        (r'减少附近敌人(\d+)点防御', r'Aura: -\1 Armor to enemies'),
        
        # 31. 魔法伤害减少30%
        (r'魔法伤害减少(\d+)%', r'\1% Magic Resistance')
    ]
    
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
        
        # Apply all translation templates
        replacements = []
        for pattern, replacement in translation_templates:
            # Find all matches before replacement
            matches = re.findall(pattern, content)
            if matches:
                # Perform the replacement
                new_content = re.sub(pattern, replacement, content)
                
                # Count the actual replacements
                count = len(matches)
                replacements.append((pattern, replacement, count))
                
                # Update content for next pattern
                content = new_content
        
        # Write the translated content to the output file
        with open(output_file, 'w', encoding=used_encoding) as file:
            file.write(content)
        
        # Report results
        print("\nTranslation Summary:")
        print(f"Total patterns applied: {len(replacements)}")
        print("\nPatterns that made replacements:")
        total_replacements = 0
        for pattern, replacement, count in replacements:
            if count > 0:
                print(f"  Pattern: '{pattern}' → '{replacement}' ({count} replacements)")
                total_replacements += count
        
        print(f"\nTotal replacements made: {total_replacements}")
        print(f"Translated file saved to: {output_file}")
        
    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    # Default file paths - update these as needed
    input_file = input("Enter path to the input file (itemfunc.txt): ") or "itemfunc.txt"
    output_file = input("Enter path for the output file (leave blank to overwrite): ") or input_file
    
    translate_item_descriptions(input_file, output_file)

if __name__ == "__main__":
    main()