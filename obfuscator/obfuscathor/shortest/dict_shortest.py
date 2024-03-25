import itertools

# Function to generate all possible combinations of characters up to length 4
def generate_combinations():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$"
    for length in range(1, 4):
        for combination in itertools.product(characters, repeat=length):
            yield "".join(combination)

# Function to filter out invalid identifiers
def filter_identifiers(identifiers, reserved_keywords):
    valid_identifiers = []
    for identifier in identifiers:
        if identifier not in reserved_keywords:
            if (identifier[0].isalpha() and identifier[0] != 'R') or identifier[0] in ['_', '$']:
                valid_identifiers.append(identifier)
    return valid_identifiers

# Load reserved keywords from file
def load_reserved_keywords(file_path):
    with open(file_path, 'r') as file:
        return set(file.read().splitlines())

# Generate all possible combinations
combinations = generate_combinations()

# Load reserved keywords
reserved_keywords = load_reserved_keywords("reserved_keywords.txt")

# Filter out invalid identifiers
valid_identifiers = filter_identifiers(combinations, reserved_keywords)

# Write valid identifiers to output file
with open("shortest_dict.txt", "w") as output_file:
    for identifier in valid_identifiers:
        output_file.write(identifier + "\n")

print("Obfuscated identifiers have been generated and saved to 'dictionary.txt'.")
