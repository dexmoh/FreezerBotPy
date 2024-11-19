# Script for converting old chatbot training data text file into a JSON format.
# Command usage: py chatbot_data_converter.py <old-data-filepath>

import sys
import json
import re


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1].lower() == "help":
        print("Usage: py chatbot_data_converter.py <old-data-filepath>")
        return -1
    
    parsed_data = {}

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        for index, line in enumerate(f):
            tokens = line.split(sep=" ")

            if len(tokens) < 1:
                print("Error: One of the tokens was empty! (Line: {index})")
                continue
            
            key = tokens[0].replace("`", " ")
            parsed_data[key] = []
            
            for token in tokens[1:]:
                match = re.match(r"^(.*)\+(\d+)$", token)
                if match:
                    text = match.group(1).replace("`", " ")
                    value = int(match.group(2))
                    parsed_data[key].append((text, value))
                else:
                    print(f"Error: One of the tokens didn't get matched! (Token: '{token}', Line: {index})")

    # Save parsed data as JSON.
    with open("chatbot_data.json", "w", encoding="utf-8") as f:
        json.dump(parsed_data, f)
    
    print(f"Successfully saved {len(parsed_data)} entries.")
    return 0


if __name__ == "__main__":
    main()
