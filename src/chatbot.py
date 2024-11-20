import json
import random
import console


# Class responsible for generating text using Markov chains.
class ChatBot():
    def __init__(self, chatbot_data_filepath: str, token_limit_per_line: int = 150):
        self.data = {}
        self.token_limit_per_line = token_limit_per_line

        try:
            with open(chatbot_data_filepath, "r", encoding="utf-8") as json_data:
                self.data = json.load(json_data)
        except Exception as e:
            console.log("Couldn't load chatbot training data from a JSON file. Make sure the filepath is correct and that the file exists.", level=console.Level.ERROR)
    
    def generate_line(self) -> str | None:
        if not self.data:
            return None
        
        text_str: str = ""
        current_key: str = "/START-OF-SENTENCE/"
        token_limit = self.token_limit_per_line

        while current_key != "/END-OF-SENTENCE/" or token_limit < 1:
            (token, value) = random.choice(self.data[current_key])

            if token == "/END-OF-SENTENCE/":
                break

            current_key = token
            text_str += token + " "
            token_limit -= 1
        
        return text_str
