import sys
import json
import os
from llm_cache import get_cached_llm, clear_cached_llm
from python_lib.unstructured_data_extractor import DataExtractor
import uuid

import csv


def convert_dict_to_csv(data_dict, file_id, csv_dir):
    nodes = data_dict['nodes']
    relationships = data_dict['relationships']

    node_dir = os.path.join(csv_dir, f"{file_id}_nodes.csv")
    rel_dir = os.path.join(csv_dir, f"{file_id}_rels.csv")
   # Write nodes to CSV
    with open(node_dir, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name:ID', 'label', ':LABEL', 'year',
                        'location', 'status', 'relation', 'role'])

        for node in nodes:
            props = node.get('properties', {})
            writer.writerow([
                node['name'],
                node['name'],
                node['label'],
                props.get('year', ''),
                props.get('location', ''),
                props.get('status', ''),
                props.get('relation', ''),
                props.get('role', '')
            ])

    # Write relationships to CSV
    with open(rel_dir, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([':START_ID', ':END_ID', ':TYPE',
                        'location', 'event', 'relation'])

        for rel in relationships:
            props = rel.get('properties', {})
            writer.writerow([
                rel['start'],
                rel['end'],
                rel['type'],
                props.get('location', ''),
                props.get('event', ''),
                props.get('relation', '')
            ])

    print("CSV files have been created: nodes.csv and relationships.csv")


def analyze_text(text):

    # try:
    llm = get_cached_llm()
    extractor = DataExtractor(llm)
    return extractor.run(text)
    # except Exception as e:
    #     print(f"Error: {e}", file=sys.stderr)
    #     sys.exit(1)


if __name__ == "__main__":
    try:
        res = analyze_text(sys.argv[1])
        clear_cached_llm()

        print("Analysis complete. Preparing JSON output...", file=sys.stderr)

        file_id = str(uuid.uuid4())

        # Construct the path to the public/json folder
        json_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'server', 'public', 'json')
        csv_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'server', 'public', 'csv')
        # Ensure the directory exists
        os.makedirs(json_dir, exist_ok=True)
        os.makedirs(csv_dir, exist_ok=True)

        # Save the JSON file
        file_path = os.path.join(json_dir, f'{file_id}.json')
        with open(file_path, 'w') as f:
            json.dump(res, f, indent=2)

        convert_dict_to_csv(res, file_id, csv_dir)
        print("JSON output saved.")

        # Print only the UUID to stdout
        print(file_id)

        sys.exit(0)
    except Exception as e:
        print(f"ERROR:{str(e)}", file=sys.stderr)
        sys.exit(1)
