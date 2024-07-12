import console


# Read a list of IDs from a whitelist file and return said list.
def read_wl_file(path):
    list = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.split("#")[0].strip()

                if line:
                    try:
                        id = int(line)
                        list.append(id)
                    except ValueError:
                        console.log(f"Couldn't convert one of the IDs in '{path}' file into a number. All of the IDs must be numbers.", console.Level.ERROR)
    except FileNotFoundError:
        console.log(f"The '{path}' file doesn't exist. The whitelist will be empty.", console.Level.WARNING)
        return []
    return list
