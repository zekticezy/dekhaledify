import json
import os

def convert_text_to_json(input_file, output_file, format_type, comment=None):
    data = []
    current_element = None
    current_text = []

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if ':' in line:
                    if current_element:
                        # Save the previous element
                        data.append({current_element: ' '.join(current_text)})

                    # Start a new element
                    element, text = line.split(':', 1)
                    current_element = element.strip()
                    current_text = [text.strip()]
                else:
                    # Append text to the current element
                    current_text.append(line.strip())

            # Save the last element
            if current_element:
                data.append({current_element: ' '.join(current_text)})

        if not output_file.lower().endswith(('.json', '.jsonc')):
            output_file += f'.{format_type.lower()}'
        
        output_path = os.path.join(os.path.dirname(__file__), output_file)

        with open(output_path, 'w', encoding='utf-8') as json_file:
            if format_type.lower() == 'jsonc' and comment:
                json_file.write(f'// {comment}\n')
            json.dump(data, json_file, indent=4)
        
        print(f"Conversion successful! {format_type} saved to {output_path}")
    
    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = input("Enter the path to the text file: ")
    output_file = input("Enter the desired output file name (e.g., output): ")
    format_type = input("Enter the format (JSON or JSONC): ").strip().upper()
    if format_type == 'JSONC':
        comment = input("Enter the comment to add at the top of the file: ")
    else:
        comment = None
    convert_text_to_json(input_file, output_file, format_type, comment)
