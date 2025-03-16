import re
import csv
import os

# # 文件路径
# file_path = r"D:\[2021-05-25]Warcraft.III.v1.20e-v1.27a.CHS.Green.Edition\伏魔战记\2025-3-15\Evil-Hunter\fmzj3.9J\units\humanunitfunc.txt"

# # 输出CSV文件路径
# output_csv = "proper_names.csv"

# # 存储提取出的名称
# proper_names = []

# # 检查文件是否存在
# if not os.path.exists(file_path):
#     print(f"错误: 文件 {file_path} 不存在")
# else:
#     # 尝试不同编码读取文件
#     encodings = ['utf-8', 'gbk', 'gb2312', 'cp936']
#     success = False
    
#     for encoding in encodings:
#         try:
#             with open(file_path, 'r', encoding=encoding) as file:
#                 # 读取文件并提取含有"propernames="的行中=后面的内容
#                 for line in file:
#                     if "propernames=" in line.lower():  # 不区分大小写
#                         # 提取propernames=后面的所有内容
#                         parts = line.split("=", 1)
#                         if len(parts) > 1:
#                             name = parts[1].strip()
#                             proper_names.append([name])
                
#                 success = True
#                 print(f"成功使用 {encoding} 编码读取文件")
#                 break
#         except UnicodeDecodeError:
#             continue
    
#     if not success:
#         print("无法使用任何编码读取文件")
#         exit(1)

#     # 将提取的名称写入CSV文件
#     with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["Proper Name"])  # 写入表头
#         writer.writerows(proper_names)

#     print(f"提取完成！共找到 {len(proper_names)} 个专有名称")
#     print(f"结果已保存到 {output_csv}")


import os
import pandas as pd
import re
import shutil
from tqdm import tqdm

# 文件路径
original_file_path = r"D:\[2021-05-25]Warcraft.III.v1.20e-v1.27a.CHS.Green.Edition\伏魔战记\2025-3-15\Evil-Hunter\fmzj3.9J\units\humanunitfunc.txt"
backup_file_path = original_file_path + ".propername.backup"
translated_csv = "proper_names.csv"

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

# 替换专有名称
print("开始替换专有名称...")
replaced_count = 0
modified_content = []

for line in tqdm(file_content):
    modified_line = line
    if "propernames=" in line.lower():  # 不区分大小写
        for cn_name, en_name in translations.items():
            # 准备替换模式：propernames=后面接着中文名称
            pattern = f"(propernames=)(.*{re.escape(cn_name)}.*)"
            if re.search(pattern, line, re.IGNORECASE):
                # 对于包含中文名称的行，执行替换
                # 这里假设中文名称是整行的一部分，可能需要根据实际格式调整
                replaced = line.replace(cn_name, en_name)
                modified_line = replaced
                replaced_count += 1
                break
    
    modified_content.append(modified_line)

# 写入修改后的内容
try:
    with open(original_file_path, 'w', encoding=used_encoding) as file:
        file.writelines(modified_content)
    print(f"替换完成！共替换了 {replaced_count} 处专有名称")
except Exception as e:
    print(f"写入修改后的文件时出错: {e}")
    print(f"原始文件已备份为: {backup_file_path}")
    exit(1)

print(f"已完成专有名称的英化处理")
print(f"原始文件已备份为: {backup_file_path}")
print(f"修改后的文件已保存为: {original_file_path}")