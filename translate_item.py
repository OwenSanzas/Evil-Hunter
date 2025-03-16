import csv
import re
import os
import shutil

def replace_item_names():
    # File paths - update these to match your actual locations
    csv_path = r"D:\[2021-05-25]Warcraft.III.v1.20e-v1.27a.CHS.Green.Edition\伏魔战记\2025-3-15\Evil-Hunter\item_translations_localized.csv"
    itemfunc_path = r"D:\[2021-05-25]Warcraft.III.v1.20e-v1.27a.CHS.Green.Edition\伏魔战记\2025-3-15\Evil-Hunter\fmzj3.9J\units\itemfunc.txt"
    
    # Create a backup of the original file
    backup_path = itemfunc_path + ".backup"
    shutil.copy2(itemfunc_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    # Load translations from CSV
    translations = {}
    try:
        # Try different encodings, as CSV might have BOM
        encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb18030']
        
        for encoding in encodings:
            try:
                with open(csv_path, 'r', encoding=encoding) as csv_file:
                    reader = csv.reader(csv_file)
                    headers = next(reader)  # Get header row
                    
                    # Find column indices
                    name_col = None
                    trans_col = None
                    
                    for i, header in enumerate(headers):
                        if "Original Name" in header:
                            name_col = i
                        elif "Translate" in header:
                            trans_col = i
                    
                    if name_col is None or trans_col is None:
                        print(f"Could not find required columns in CSV. Headers: {headers}")
                        continue
                    
                    # Load translations
                    for row in reader:
                        if len(row) > max(name_col, trans_col):
                            original = row[name_col].strip()
                            translation = row[trans_col].strip()
                            
                            if original and translation:
                                translations[original] = translation
                
                print(f"Successfully loaded {len(translations)} translations using encoding: {encoding}")
                break  # Successfully loaded
                
            except Exception as e:
                print(f"Failed to load with encoding {encoding}: {e}")
                continue
        
        if not translations:
            print("Failed to load translations from CSV with any encoding.")
            return
            
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return
    
    # Sort translations by length (longest first) to avoid partial replacements
    sorted_items = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    try:
        # Read the itemfunc.txt file
        encodings = ['utf-8', 'gbk', 'gb18030']
        content = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                with open(itemfunc_path, 'r', encoding=encoding) as file:
                    content = file.read()
                used_encoding = encoding
                print(f"Successfully read itemfunc.txt using encoding: {encoding}")
                break
            except Exception as e:
                print(f"Failed to read with encoding {encoding}: {e}")
        
        if content is None:
            print("Failed to read itemfunc.txt with any encoding.")
            return
        
        # Create a list of replacements to apply
        replacements = []
        for original, translation in sorted_items:
            # Skip empty originals or translations
            if not original or not translation:
                continue
                
            # Look for the original name in the content
            occurrences = content.count(original)
            if occurrences > 0:
                replacements.append((original, translation, occurrences))
                
                # Replace the original with the translation
                content = content.replace(original, translation)
        
        # Write the modified content back to the file
        with open(itemfunc_path, 'w', encoding=used_encoding) as file:
            file.write(content)
        
        # Report results
        print("\nReplacement Summary:")
        print(f"Total translations loaded: {len(translations)}")
        print(f"Total replacements made: {len(replacements)}")
        print("\nItems replaced:")
        for original, translation, count in replacements:
            print(f"  '{original}' → '{translation}' ({count} occurrences)")
        
        print("\nItems not found in the file:")
        not_found = set(translations.keys()) - set(item[0] for item in replacements)
        for original in sorted(not_found):
            print(f"  '{original}' → '{translations[original]}'")
            
        print("\nReplacement complete!")
            
    except Exception as e:
        print(f"Error processing itemfunc.txt: {e}")
        print("Restoring backup...")
        shutil.copy2(backup_path, itemfunc_path)
        print("Backup restored.")

if __name__ == "__main__":
    replace_item_names()