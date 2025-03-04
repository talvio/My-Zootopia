import json

FOX_FILE = "animals_data.json"

def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as handle:
        return json.load(handle)


def print_foxes():
    """
    reads the content of animals_data.json, iterates through the animals, and for each one prints:
    Name, Diet, The first location from the locations list, Type
    :return: None
    """
    foxes_data = load_data(FOX_FILE)
    for fox in foxes_data:
        if fox.get('name'):
            print(f"Name: {fox.get('name')}")
        if fox.get('characteristics',{}).get('diet', None):
            print(f"Diet: {fox.get('characteristics',{}).get('diet', None)}")
        if fox.get('locations', None):
            print(f"Location: {fox.get('locations', [])[0]}")
        if fox.get('characteristics',{}).get('type', None):
            print(f"Type: {fox.get('characteristics',{}).get('type', None)}")
        print()

def main():
    print_foxes()


if __name__ == '__main__':
    main()
