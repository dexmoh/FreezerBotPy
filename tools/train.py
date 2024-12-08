# Script for training the chatbot.

import json
import re


INPUT_DATA_PATH: str = ".data/message_history.json"
WORD_BLACKLIST_PATH: str = ".data/chatbot/word_blacklist.json"
OUTPUT_PATH: str = ".data/chatbot/dataset.json"

END_OF_SENTENCE: str = "/END-OF-SENTENCE/"

data = {}
with open(INPUT_DATA_PATH, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

word_blacklist = []
with open(WORD_BLACKLIST_PATH, "r") as json_file:
    word_blacklist = json.load(json_file)

dataset = {}

for channel in data:
    print(f"Processing {channel}...")
    for message in data[channel]:
        (author, content) = message

        if not content or content == "":
            continue

        tokens = []
        for token in content.split():
            if token.startswith("http") or re.search(r"<:.+:\d+>", token):
                tokens.append(token)
                continue

            # Set every token except URLs and emoji to lowercase.
            tokens.append(token.lower())

            # If the message contains a blacklisted word, we don't want to train on it.
            if token.lower() in word_blacklist:
                tokens = []
                break

        if not tokens:
            continue
                
        # Add the tokens to the dataset.
        for index, token in enumerate(tokens):
            # Get the next token.
            next = END_OF_SENTENCE
            if index + 1 != len(tokens):
                next = tokens[index + 1]
            
            # Create the token in the dataset if it doesnt exist yet.
            if token not in dataset:
                dataset[token] = {}
            
            # Create or increment a link.
            if next not in dataset[token]:
                dataset[token][next] = 1
            else:
                dataset[token][next] += 1

# Save the dataset to a file.
with open(OUTPUT_PATH, "w", encoding="utf-8") as json_file:
    json.dump(dataset, json_file)
