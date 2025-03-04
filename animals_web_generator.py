import json

FOX_FILE = "animals_data.json"
TEMPLATE_FILE = "animals_template.html"
DATA_PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"
ANIMALS_FILE = "animals.html"


def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def read_template_file(file_path):
    """
    Reads a file and returns the content in a string
    :param file_path: Path of the file to read
    :return: The content of the file
    """
    with open(file_path, "r") as file:
        return file.read()


def print_foxes(fox_file):
    """
    reads the content of animals_data.json, iterates through the animals, and for each one prints:
    Name, Diet, The first location from the locations list, Type
    :return: None
    """
    foxes_data = load_data(fox_file)
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

def foxes_to_html_list(fox_file):
    """
    Read fox information and return it all in one string, each fox as HTML list (<li></li>) item
    :return: Information about foxes in one string format as HTML list items
    """
    foxes_data = load_data(fox_file)
    foxes_string = ""
    for fox in foxes_data:
        foxes_string += '<li class="cards__item">\n'
        if fox.get('name'):
            foxes_string += f"Name: {fox.get('name')}<br/>\n"
        if fox.get('characteristics',{}).get('diet', None):
            foxes_string += f"Diet: {fox.get('characteristics',{}).get('diet', None)}<br/>\n"
        if fox.get('locations', None):
            foxes_string += f"Location: {fox.get('locations', [])[0]}<br/>\n"
        if fox.get('characteristics',{}).get('type', None):
            foxes_string += f"Type: {fox.get('characteristics',{}).get('type', None)}<br/>\n"
        foxes_string += "</li>\n\n"
    return foxes_string


def save_to_file(file_path, data):
    """
    Write data to file
    :param file_path: file to which we write
    :param data: Data to be written into the file. None binary.
    :return: None
    """
    with open(file_path, "w") as file:
        file.write(data)


def main():
    template = read_template_file(TEMPLATE_FILE)
    #print_foxes(FOX_FILE)

    fox_html_data = template.replace(DATA_PLACEHOLDER, foxes_to_html_list(FOX_FILE))
    save_to_file(ANIMALS_FILE, fox_html_data)


if __name__ == '__main__':
    main()
