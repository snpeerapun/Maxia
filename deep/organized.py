import json
import os

# Function to process and organize the data
def organize_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    organized_data = {}

    for item in data:
        intent = item['intent']
        if intent not in organized_data:
            organized_data[intent] = []
        organized_data[intent].append(item['sentence'])

    return organized_data

# Function to save data to JSON file
def save_to_json(data, output_dir):
    for intent, items in data.items():
        intent_filename = intent.replace(" ", "_") + ".json"    
        output_file = os.path.join(output_dir, intent_filename)
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(items, json_file, ensure_ascii=False, indent=4)

# List of input JSON files
input_files = ['deep\\test1.json', 'deep\\test2.json']

# Output directory to save organized data
output_directory = 'deep\\organized'

# Create output directory if not exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Process and organize data from input files
combined_data = []
for input_file in input_files:
    organized_data = organize_data(input_file)
    combined_data.append(organized_data)

# Combine data from all input files
final_data = {}
for data in combined_data:
    for intent, items in data.items():
        if intent not in final_data:
            final_data[intent] = []
        final_data[intent].extend(items)

# Save organized data to JSON files
save_to_json(final_data, output_directory)

print("Data organized and saved successfully.")
