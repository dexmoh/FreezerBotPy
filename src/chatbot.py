import re
import json
import random
import console


# Class responsible for generating text using Markov chains.
# The chatbot can learn words from new messages and use them in future generation.
class ChatBot():
    def __init__(self):
        self.data: dict[str, dict[str, int]] = {}
        self.data_filepath: str = ".data/chatbot/dataset.json"
        self.word_blacklist: list[str] = []
        self.max_char_len: int = 2000
        self.END_OF_SENTENCE: str = "/END-OF-SENTENCE/"

        # Load chatbot data from a file.
        try:
            with open(self.data_filepath, "r", encoding="utf-8") as json_file:
                self.data = json.load(json_file)
        except Exception as e:
            self.data = {}
            console.log("Couldn't load chatbot training dataset from a JSON file. Make sure the filepath is correct and that the file exists.", level=console.Level.ERROR)

        # Load a list of bad words we want our chatbot to avoid learning.
        try:
            with open(".data/chatbot/word_blacklist.json", "r") as json_file:
                self.word_blacklist = json.load(json_file)
        except Exception as e:
            self.word_blacklist = []
            console.log("Couldn't load a word blacklist, the chatbot might learn some naughty words.", console.Level.WARNING)

    def generate_line(self) -> str | None:
        if not self.data:
            return None
        
        message = ""
        message_token_len = 0

        # Pick a random token to start with.
        current_token = random.choice(list(self.data.keys()))

        while current_token != self.END_OF_SENTENCE:
            message += current_token + " "
            message_token_len += 1

            # Check if we hit the character limit.
            if len(message) > self.max_char_len:
                # Cut down the string to fit the limit.
                message = message[:self.max_char_len]
                break

            # Choose the next token.
            choice = random.randrange(0, self._get_weight(current_token) + 1)
            for next in self.data[current_token]:
                choice -= self.data[current_token][next]
                if choice < 1:
                    current_token = next
                    break
        
        return message

    def learn(self, sentence: str):
        tokens = []
        for token in sentence.split():
            if token.startswith("http") or re.search(r"<:.+:\d+>", token):
                tokens.append(token)
                continue

            # Set every token except URLs and emoji to lowercase.
            tokens.append(token.lower())

            # If the message contains a blacklisted word, we don't want to train on it.
            if token.lower() in self.word_blacklist:
                return
        
        if not tokens:
            return
                
        # Add the tokens to the dataset.
        for index, token in enumerate(tokens):
            # Get the next token.
            next = self.END_OF_SENTENCE
            if index + 1 != len(tokens):
                next = tokens[index + 1]
            
            # Create the token in the dataset if it doesnt exist yet.
            if token not in self.data:
                self.data[token] = {}
            
            # Create or increment a link.
            if next not in self.data[token]:
                self.data[token][next] = 1
            else:
                self.data[token][next] += 1
        
        # Save the dataset to a file.
        with open(self.data_filepath, "w", encoding="utf-8") as json_file:
            json.dump(self.data, json_file)
    
    # Get the total weight of all of the links for a token in a Markov chain.
    def _get_weight(self, token: str):
        link_weight = 0
        for next in self.data[token]:
            link_weight += self.data[token][next]
        
        return link_weight
