import os
import json
import xml.etree.ElementTree as ET

folder_path = "src"
output_path = "ref"
sitemap_output_path = "."
base_url = "https://harutotsukusame.github.io/hirameki-no-kirameki"

def extract_filename(file_path):
    return os.path.splitext(os.path.basename(file_path))[0][1:]

filenames = [extract_filename(f) for f in os.listdir(folder_path) if os.path.isfile(
    os.path.join(folder_path, f)) and f.endswith('.md')]

file_data = {filename: {"referenced_by": [], "references": []} for filename in filenames}

for filename in filenames:
    file_path = os.path.join(folder_path, f"_{filename}.md")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        for ref_filename in file_data.keys():
            if filename != ref_filename and ref_filename in content:
                file_data[filename]["references"].append(ref_filename)
                file_data[ref_filename]["referenced_by"].append(filename)

for filename, data in file_data.items():
    data["references"].sort(key=len, reverse=True)  # 文字列が長い順に並び替え

output_file_path = os.path.join(output_path, 'file_data.json')
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(file_data, f, ensure_ascii=False, indent=4)

# Create sitemap.xml using ElementTree
urlset = ET.Element('urlset', {'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})

for filename in filenames:
    url = ET.SubElement(urlset, 'url')
    loc = ET.SubElement(url, 'loc')
    loc.text = f'{base_url}/?{filename}'

sitemap_output_file_path = os.path.join(sitemap_output_path, 'sitemap.xml')
tree = ET.ElementTree(urlset)
tree.write(sitemap_output_file_path, encoding='utf-8', xml_declaration=True)
