import json
import argparse

conversion_dict = {
    "text": "p",
    "Button": "button",
    "ImageView": "img",
    "EditText": "<input><label>",
    "CheckBox": "<input type='checkbox'><label>",
    "RadioButton": "<input type='radio'><label>"
}

# Unique index generator
def unique_index_generator():
    i = 1
    while True:
        yield i
        i += 1

index_gen = unique_index_generator()

def class_to_html_tag(class_name):
    return {
        "text": "p",
        "Button": "button",
        "ImageView": "img",
        "EditText": "<input><label>",
        "CheckBox": "<input type='checkbox'><label>",
        "RadioButton": "<input type='radio'><label>"
    }.get(class_name, "div")  # default to div

def dfs(node, is_div=False):
    html = ""
    class_name = ""

    #we should only check for text, images, and buttons
    if "class" in node:
        class_name = class_to_html_tag(node['class'])

        # Avoid nested div tags
        if is_div and class_name == "div":
            class_name = ""  # Reset to empty to avoid adding div
        else:
            html += "<" + class_name + ' id=\"' + str(next(index_gen)) + '\"'

            if 'resource-id' in node:
                html += ' class=\"' + node['resource-id'] + '\"'

            if node['class'] == "ImageView" and 'content-desc' in node:
                html += ' alt=\"' + node['content-desc'] + '\"'

            html += ">"
        
    for key, value in node.items():
        if key in conversion_dict:
            html += "<" + conversion_dict[key] + ">" + str(value) + "</" + conversion_dict[key].split('<')[0] + ">"
    
    if 'children' in node:
        for child in node['children']:
            html += dfs(child, class_name == "div")
    
    if "class" in node and class_name:
        html += "</" + class_name.split('<')[0] + ">"
    
    return html

def convert_json_to_html(json_file):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    json_data = json_data["activity"]["root"]
    return dfs(json_data)

parser = argparse.ArgumentParser()
parser.add_argument("json_file", help="Path to the JSON file to convert to HTML")
args = parser.parse_args()
html = convert_json_to_html(args.json_file)

with open("target.html", "w") as file:
    file.write(html)
