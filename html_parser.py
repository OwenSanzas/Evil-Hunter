import re
import csv
import html

def extract_text_from_html(html_content):
    """Extract text content from HTML, removing all tags"""
    # Remove all HTML tags, preserving only text content
    return re.sub(r'<[^>]*>', '', html_content)

def parse_html_content(html_content):
    """Parse the HTML content and extract item IDs and names"""
    items = []
    
    # Split the content by <br> tags to process line by line
    lines = html_content.split('<br>')
    
    for line in lines:
        if not line.strip():
            continue
        
        # Extract the item ID
        id_match = re.search(r'<a href="#([^"]+)">', line)
        if not id_match:
            continue
        
        item_id = id_match.group(1)
        
        # Remove the anchor tag part from the line
        content = re.sub(r'<a href="#[^"]+">.*?</a>', '', line).strip()
        
        # Extract text from the remaining content
        item_name_with_prefix = extract_text_from_html(content).strip()
        
        # Clean up any extra whitespace
        item_name_with_prefix = re.sub(r'\s+', ' ', item_name_with_prefix).strip()
        
        # Decode HTML entities (like &nbsp;)
        item_name_with_prefix = html.unescape(item_name_with_prefix)
        
        # Skip items with empty names
        if not item_name_with_prefix:
            continue
        
        item_name = re.sub(r'^\([^)]+\)', '', item_name_with_prefix)  # Remove (prefix)
        item_name = re.sub(r'^\[[^\]]+\]', '', item_name)  # Remove [prefix]
        item_name = item_name.strip()
        
        items.append((item_id, item_name))
    return items

def main():
    try:
        # Read the input HTML file
        with open("item.txt", "r", encoding="utf-8") as file:
            html_content = file.read()

        print(len(html_content))
        
        # Parse the HTML content
        items = parse_html_content(html_content)
        
        # Write to CSV
        with open("item_translations.csv", "w", encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Original Name"])
            for item_id, item_name in items:
                writer.writerow([item_id, item_name])
        
        print(f"Successfully extracted {len(items)} items to item_translations.csv")
        
        # Print a few examples for verification
        print("\nExample entries:")
        for i, (item_id, item_name) in enumerate(items[:5]):
            print(f"{item_id}: {item_name}")
            
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()