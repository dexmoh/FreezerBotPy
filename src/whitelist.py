import console


# List of discord users that have access to the bot's privileged commands.
user_whitelist = []

# List of discord servers that have access to the experimental features.
server_whitelist = []


# Fetch user and server whitelists from files and initialize their respective lists.
def init():
    global user_whitelist
    global server_whitelist
    
    # File paths.
    user_wl_path = ".data/user_whitelist.txt"
    server_wl_path = ".data/server_whitelist.txt"

    # Function for reading the files while ignoring comments.
    def read_ids(path):
        list = []

        try:
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.split("#")[0].strip()

                    if line:
                        try:
                            list.append(int(line))
                        except ValueError:
                            console.log(f"Couldn't convert one of the IDs in '{path}' file into a number. All of the IDs must be numbers.", console.Level.ERROR)
        except FileNotFoundError:
            return []

        return list

    user_whitelist = read_ids(user_wl_path)
    server_whitelist = read_ids(server_wl_path)

    if not user_whitelist:
        console.log(f"The user whitelist is empty, there will be no privileged users. Make sure the '{user_wl_path}' file exists and contains proper user IDs.", console.Level.WARNING)
    if not server_whitelist:
        console.log(f"The server whitelist is empty, experimental features won't be available to any server. Make sure the '{server_whitelist}' file exists and contains proper server IDs.", console.Level.WARNING)
