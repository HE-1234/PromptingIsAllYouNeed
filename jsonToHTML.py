import json
import argparse

def dfs(node):
    html = ""
    
    
    if "class" not in node:
        return
    # Start the HTML tag for this node
    html += "<" + node['class']
    
    # Add each required property as an attribute in the HTML tag if it exists
    properties = ['resource-id', 'class', 'text', 'content-desc']
    for prop in properties:
        if prop in node:
            html += " " + prop + "=\"" + str(node[prop]) + "\""
    
    # Close the opening HTML tag
    html += ">"
    
    # If this node has children, recurse on each child
    if 'children' in node:
        for child in node['children']:
            html += dfs(child)
            
    # Close the HTML tag for this node
    html += "</" + node['class'] + ">"
    
    return html

def convert_json_to_html(json_file):
    # Load the JSON data from file
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    json_data = json_data["activity"]["root"]
    print(len(json_data))
    
    # Start DFS on the root node
    return dfs(json_data)

# Initialize argument parser
parser = argparse.ArgumentParser()
parser.add_argument("json_file", help="Path to the JSON file to convert to HTML")

# Parse arguments
args = parser.parse_args()

# Convert JSON to HTML
html = convert_json_to_html(args.json_file)

with open("target.html", "w") as file:
    file.write(html)
