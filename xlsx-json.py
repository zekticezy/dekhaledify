# Written by zekkie
# This is a basic CLI script to convert our database.ods file into a json/jsonc file when we update it, so that our code can read it and our extension can work.
# Last updated: 8/2/2024

import pandas as pd
import json
import os
from datetime import datetime

def convert_to_json(input_file, output_file, format_type, comment=None):
    print("Starting conversion...")
    file_extension = os.path.splitext(input_file)[1].lower()
    print(f"File extension detected: {file_extension}")
    
    if file_extension == '.xlsx':
        df = pd.read_excel(input_file)
    elif file_extension == '.ods':
        df = pd.read_excel(input_file, engine='odf')
    else:
        print("Unsupported file format.")
        return
    
    column_names = df.columns.tolist()
    formatted_column_names = [name.strip().lower().replace(' ', '-') for name in column_names]
    
    data = df.rename(columns=dict(zip(column_names, formatted_column_names))).to_dict(orient='records')
    
    def json_serialize(value):
        if isinstance(value, (datetime, pd.Timestamp)):
            return value.isoformat()
        elif isinstance(value, pd.Timedelta):
            return str(value)
        else:
            return str(value)
    
    serializable_data = [{k: json_serialize(v) for k, v in row.items()} for row in data]
    
    if not output_file.lower().endswith(('.json', '.jsonc')):
        output_file += f'.{format_type.lower()}'
    
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    
    with open(output_path, 'w') as f:
        if format_type.lower() == 'jsonc' and comment:
            f.write(f'// {comment}\n')
        json.dump(serializable_data, f, indent=4)
    
    print(f"Conversion successful! {format_type} saved to {output_path}")

if __name__ == "__main__":
    input_file = input("Enter the path to the .ods or .xlsx file: ")
    if not os.path.exists(input_file):
        print("The file does not exist.")
    else:
        output_file = input("Enter the desired output file name (e.g., output): ")
        format_type = input("Enter the format (JSON or JSONC): ").strip().upper()
        if format_type == 'JSONC':
            comment = input("Enter the comment to add at the top of the file: ")
        else:
            comment = None
        convert_to_json(input_file, output_file, format_type, comment)
