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


def serialize_animal(animal_obj):
    """
    Takes input as dict and returns it serialized html list item string
    :param animal_obj:
    :return: html list item string
    """
    animal_list_item = ""
    animal_list_item += '<li class="cards__item">\n'
    animal_list_item += f'  <div class="card__title">{animal_obj.get("name", "No name")}</div>\n'
    animal_list_item += '   <p class="card__text">\n'
    if animal_obj.get('characteristics', {}).get('diet', None):
        animal_list_item += f"      <strong>Diet:</strong> {animal_obj.get('characteristics', {}).get('diet', None)}<br/>\n"
    if animal_obj.get('locations', None):
        animal_list_item += f"      <strong>Location:</strong> {animal_obj.get('locations', [])[0]}<br/>\n"
    if animal_obj.get('characteristics', {}).get('type', None):
        animal_list_item += f"      <strong>Type:</strong> {animal_obj.get('characteristics', {}).get('type', None)}<br/>\n"
    animal_list_item += "   </p>\n"
    animal_list_item += "</li>\n\n"
    return animal_list_item


def foxes_to_html_list(fox_file):
    """
    Read fox information and return it all in one string, each fox as HTML list (<li></li>) item
    :return: Information about foxes in one string format as HTML list items
    """
    foxes_data = load_data(fox_file)
    foxes_string = ""
    for fox in foxes_data:
        foxes_string += serialize_animal(fox)
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
