import os
import pandas as pd
import re
import shutil
from tqdm import tqdm

# 文件路径
original_file_path = r"D:\[2021-05-25]Warcraft.III.v1.20e-v1.27a.CHS.Green.Edition\伏魔战记\2025-3-15\Evil-Hunter\fmzj3.9J\units\humanunitfunc.txt"
backup_file_path = original_file_path + ".backup"
translated_csv = "translated_unit_names.csv"

# 创建备份
print(f"正在创建原始文件的备份: {backup_file_path}")
try:
    shutil.copy2(original_file_path, backup_file_path)
    print("备份创建成功！")
except Exception as e:
    print(f"创建备份时出错: {e}")
    exit(1)

# 读取翻译结果
try:
    df = pd.read_csv(translated_csv)
    translations = dict(zip(df["Chinese Name"], df["English Name"]))
    print(f"已加载 {len(translations)} 个翻译条目")
except Exception as e:
    print(f"读取翻译文件时出错: {e}")
    exit(1)

# 读取原始文件内容
try:
    encodings = ['utf-8', 'gbk', 'gb2312', 'cp936']
    file_content = None
    
    for encoding in encodings:
        try:
            with open(original_file_path, 'r', encoding=encoding) as file:
                file_content = file.readlines()
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

# 替换单位名称
print("开始替换单位名称...")
replaced_count = 0
modified_content = []

for line in tqdm(file_content):
    modified_line = line
    if "Name=" in line:
        for cn_name, en_name in translations.items():
            # 准备替换模式：Name=后面接着中文名称
            # 使用正则表达式确保只替换Name=后面的完整匹配
            pattern = f"(Name=)({re.escape(cn_name)})"
            if re.search(pattern, line):
                modified_line = re.sub(pattern, f"\\1{en_name}", line)
                replaced_count += 1
                break
    
    modified_content.append(modified_line)

# 写入修改后的内容
try:
    with open(original_file_path, 'w', encoding=used_encoding) as file:
        file.writelines(modified_content)
    print(f"替换完成！共替换了 {replaced_count} 处单位名称")
except Exception as e:
    print(f"写入修改后的文件时出错: {e}")
    print(f"原始文件已备份为: {backup_file_path}")
    exit(1)

print(f"已完成单位名称的英化处理")
print(f"原始文件已备份为: {backup_file_path}")
print(f"修改后的文件已保存为: {original_file_path}")