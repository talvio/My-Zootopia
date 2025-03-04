import json

FOX_FILE = "animals_data.json"
TEMPLATE_FILE = "animals_template.html"
DATA_PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"
ANIMALS_FILE = "animals.html"
ALL_SELECTION = "All of them"


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
    animal_list_item += f'  <div class="card__title">{animal_obj.get("name", "No name")}'
    animal_list_item += f'  <span class="scientific__name">('
    animal_list_item += f'{animal_obj.get("taxonomy", {}).get('scientific_name', "no scientific name")})</span></div>\n'
    animal_list_item += '   <p class="card__text">\n'
    animal_list_item += '   <ul class="animal__facts">\n'
    if animal_obj.get('characteristics', {}).get('diet', None):
        animal_list_item += "      <li><strong>Diet:</strong> "
        animal_list_item += f"{animal_obj.get('characteristics', {}).get('diet', None)}</li>\n"
    if animal_obj.get('locations', None):
        animal_list_item += f"      <li><strong>Locations:</strong> "
        animal_list_item += f"{', '.join(animal_obj.get('locations', []))}</li>\n"

    if animal_obj.get('characteristics', {}).get('type', None):
        animal_list_item += "      <li><strong>Type:</strong> "
        animal_list_item += f"{animal_obj.get('characteristics', {}).get('type', None)}</li>\n"
    if animal_obj.get('characteristics', {}).get('weight', None):
        animal_list_item += "      <li><strong>Weight:</strong> "
        animal_list_item += f"{animal_obj.get('characteristics', {}).get('weight', None)}</li>\n"
    if animal_obj.get('characteristics', {}).get('type', None):
        animal_list_item += "      <li><strong>Lifespan:</strong> "
        animal_list_item += f"{animal_obj.get('characteristics', {}).get('lifespan', None)}</li>\n"
    animal_list_item += '   </ul>\n'
    animal_list_item += "   </p>\n"
    animal_list_item += "</li>\n\n"

    return animal_list_item


def foxes_to_html_list(fox_file, skin_filter=ALL_SELECTION):
    """
    Read fox information and return it all in one string, each fox as HTML list (<li></li>) item
    :return: Information about foxes in one string format as HTML list items
    """
    foxes_data = load_data(fox_file)
    foxes_string = ""
    for fox in foxes_data:
        if skin_filter == ALL_SELECTION or fox.get('characteristics',{}).get('skin_type', None) == skin_filter:
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


def discover_skin_types(animal_data):
    """
    Discover what skin types the animal have
    :param animal_data: animal_data in dict. Skin type is in a dict inside another dict
    :return: list with all skin types
    """
    skin_types = set()
    for animal in animal_data:
       skin_types.add(animal.get('characteristics',{}).get('skin_type', None))
    return list(skin_types)


def ask_number(message="Give a number: ", lower_limit=0, upper_limit=None, default_number=None, allow_empty=False):
    """
    Checks that the user enters a number and not something else
    :param allow_empty: If yes, allows the user to not enter anything. In this case, returns None
    :param default_number: Return this number if the user gives no other input except hits enter
                           If default_number is None, empty answer is not allowed.
                           The default_number needs to be a valid number as well.
    :param upper_limit: The number from the user needs to be below or equal to this
    :param lower_limit: The number from the user needs to be higher or equal to this
    :param message: What we display to xplain to the user what number we need
    :return: the number, duh! Or if allow_empty=True and user enters nothing, returns None
    """
    valid_number = False
    while not valid_number:
        if default_number is None:
            user_input_number = input(f"{message}").strip()
        else:
            user_input_number = (input(f"{message}  [{default_number}] ").strip() or
                                 default_number)
        if len(user_input_number) == 0 and allow_empty:
            return None
        try:
            user_input_number = float(user_input_number)
            valid_number = True
        except ValueError:
            user_input_number = lower_limit - 1

        if lower_limit is not None and user_input_number < lower_limit:
            valid_number = False
        if upper_limit is not None and user_input_number > upper_limit:
            valid_number = False

    return user_input_number


def ask_which_skin_type(animal_file):
    """
    Ask the user which skin type we will use later
    :return: One of the skin types from the animal_file data
    """
    skin_types = discover_skin_types(load_data(animal_file))
    skin_types.sort()
    skin_types.append(ALL_SELECTION)
    for skin_num, skin_type in enumerate(skin_types):
        print(f"{skin_num + 1:2} {skin_type}")
    user_selection = int(ask_number(message="Which skin type you want to see in the web page? ",
                                    lower_limit=1, upper_limit=len(skin_types)))
    return skin_types[user_selection - 1]


def main():
    """
    Create a HTML file ANIMALS_FILE which lists animals from the FOX_FILE.
    :return: None
    """
    html_page_template = read_template_file(TEMPLATE_FILE)
    skin_type = ask_which_skin_type(FOX_FILE)
    fox_html_data = html_page_template.replace(DATA_PLACEHOLDER, foxes_to_html_list(FOX_FILE, skin_filter=skin_type))
    save_to_file(ANIMALS_FILE, fox_html_data)


if __name__ == '__main__':
    main()
