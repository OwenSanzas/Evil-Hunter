import re
import os
import shutil
import csv

# 文件路径
ability_file_path = r"D:\[2021-05-25]Warcraft.III.v1.20e-v1.27a.CHS.Green.Edition\伏魔战记\2025-3-15\Evil-Hunter\humanabilityfunc.txt"
backup_file_path = ability_file_path + ".full_backup"
translation_csv = r"D:\[2021-05-25]Warcraft.III.v1.20e-v1.27a.CHS.Green.Edition\伏魔战记\2025-3-15\Evil-Hunter\translate.csv"

# 创建备份
print(f"正在创建原始文件的备份: {backup_file_path}")
try:
    shutil.copy2(ability_file_path, backup_file_path)
    print("备份创建成功！")
except Exception as e:
    print(f"创建备份时出错: {e}")
    exit(1)

# 读取翻译表
try:
    translations = {}
    category_map = {}
    
    with open(translation_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # 跳过表头
        
        for row in reader:
            if len(row) >= 5:  # 确保至少有5列
                chinese_category = row[1]
                english_category = row[2]
                chinese_description = row[3]
                english_description = row[4]
                
                # 添加到翻译字典
                translations[chinese_description] = english_description
                
                # 添加类别映射
                if chinese_category and english_category:
                    category_map[chinese_category] = english_category
    
    print(f"已加载翻译词典，共 {len(translations)} 个条目")
    print(f"已创建类别映射表: {category_map}")
    
except Exception as e:
    print(f"读取翻译文件时出错: {e}")
    # 如果CSV读取失败，添加一些基本翻译
    translations = {
        "力量+5": "Strength +5",
        "智力+5": "Intelligence +5",
        "敏捷+5": "Agility +5",
        "力量+20": "Strength +20",
        "智力+50": "Intelligence +50",
        "敏捷+10": "Agility +10",
        "力量+50": "Strength +50",
        "力量+20敏捷+20": "Strength +20 Agility +20",
        "力量+20智力+20": "Strength +20 Intelligence +20",
        "力量+50智力+50": "Strength +50 Intelligence +50",
        "力量+50敏捷+50": "Strength +50 Agility +50",
        "力量+50智力+100": "Strength +50 Intelligence +100",
        "力量+50敏捷+100": "Strength +50 Agility +100",
        "力量+50敏捷+50智力+50": "Strength +50 Agility +50 Intelligence +50",
        "属性 未使用": "Attribute Unused",
        "攻击力+200暗": "Attack Power +200 Dark",
        "防": "Defense",
        "攻": "Attack",
    }
    category_map = {"防": "Defense", "攻": "Attack"}
    print("使用默认翻译字典继续执行")

# 读取原始文件内容
try:
    encodings = ['utf-8', 'gbk', 'gb2312', 'cp936']
    file_content = None
    
    for encoding in encodings:
        try:
            with open(ability_file_path, 'r', encoding=encoding) as file:
                file_content = file.read()
                used_encoding = encoding
                print(f"成功使用 {encoding} 编码读取文件")
                break
        except UnicodeDecodeError:
            continue
    
    if file_content is None:
        print("无法使用任何编码读取文件")
        exit(1)
except Exception as e:
    print(f"读取原始文件时出错: {e}")
    exit(1)

# 替换所有出现的中文描述
print("开始替换中文描述...")
replaced_count = 0

# 首先替换Name标签中的内容
name_pattern = re.compile(r'(Name=\[)(.*?)(\])(.*?)($|,)')
def name_replacer(match):
    global replaced_count
    bracket_prefix = match.group(1)  # "Name=["
    category = match.group(2)        # 类别
    bracket_suffix = match.group(3)  # "]"
    description = match.group(4)     # 描述
    ending = match.group(5)          # 结尾 (换行或逗号)
    
    # 替换类别
    if category in category_map:
        category = category_map[category]
    
    # 替换描述
    if description.strip() in translations:
        new_description = translations[description.strip()]
        replaced_count += 1
        print(f"替换: {description.strip()} -> {new_description}")
    else:
        new_description = description
    
    return f"{bracket_prefix}{category}{bracket_suffix}{new_description}{ending}"

# 对Name标签应用替换
modified_content = re.sub(name_pattern, name_replacer, file_content)

# 然后替换其他位置出现的中文描述
for chinese, english in translations.items():
    if chinese and english and chinese != english:
        # 排除非常短的字符串，以避免误替换
        if len(chinese) < 200:
            # 确保只替换完整的词，而不是部分匹配
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(chinese) + r'(?![a-zA-Z0-9])'
            count = len(re.findall(pattern, modified_content))
            if count > 0:
                modified_content = re.sub(pattern, english, modified_content)
                replaced_count += count
                print(f"非Name标签替换: {chinese} -> {english}，共{count}处")

# 写入修改后的内容
try:
    with open(ability_file_path, 'w', encoding=used_encoding) as file:
        file.write(modified_content)
    print(f"替换完成！共替换了 {replaced_count} 处中文描述")
except Exception as e:
    print(f"写入修改后的文件时出错: {e}")
    print(f"原始文件已备份为: {backup_file_path}")
    exit(1)

print(f"已完成中文描述的英化处理")
print(f"原始文件已备份为: {backup_file_path}")
print(f"修改后的文件已保存为: {ability_file_path}")