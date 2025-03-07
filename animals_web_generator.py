import data_fetcher


TEMPLATE_FILE = "animals_template.html"
NOT_FOUND_TEMPLATE_FILE = "not_found_template.html"
DATA_PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"
ANIMALS_FILE = "animals.html"
ALL_SELECTION = "All of them"


def read_template_file(file_path):
    """
    Reads a file and returns the content in a string
    :param file_path: Path of the file to read
    :return: The content of the file
    """
    with open(file_path, "r") as file:
        return file.read()


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


def animals_to_html_list(animal_data, skin_filter=ALL_SELECTION):
    """
    Return animal data in one string, each animal as HTML list (<li></li>) item
    :skin_filter: If used, filters the animals in the output based on their skin type as stated in this variable.
    :return: Information about animals in one string, formatted as HTML list items
    """
    animal_string = ""
    for animal in animal_data:
        if skin_filter == ALL_SELECTION or animal.get('characteristics',{}).get('skin_type', None) == skin_filter:
            animal_string += serialize_animal(animal)
    return animal_string


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
    Discover what skin types the animals have
    :param animal_data: animal_data in dict. Skin type is in a dict inside another dict
    :return: list with all skin types
    """
    skin_types = set()
    for animal in animal_data:
       skin_types.add(animal.get('characteristics',{}).get('skin_type', "Not specified"))
    return list(skin_types)


def ask_string(message="Give your input: ", default_string=None):
    """
    :param default_string: If the user gives an empty string, function returns the default string
    :param message: Prompt message, what is asked from the user
    :return: a string the user types from the keyboard
    This method separates controller from using input directly.
    """
    user_input = ""
    while len(user_input) == 0:
        if default_string is None:
            user_input = input(f"{message}").strip()
        else:
            user_input = (input(f"{message}[{default_string}] ").strip()
                          or str(default_string))
    return user_input


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


def ask_which_skin_type(animal_data):
    """
    Ask the user which skin type we will use later
    :return: One of the skin types from the animal_file data
    """
    skin_types = discover_skin_types(animal_data)
    skin_types.sort()
    skin_types.append(ALL_SELECTION)
    for skin_num, skin_type in enumerate(skin_types):
        print(f"{skin_num + 1:2} {skin_type}")
    user_selection = int(ask_number(message="Which skin type you want to see in the web page? ",
                                    lower_limit=1, upper_limit=len(skin_types)))
    return skin_types[user_selection - 1]


def make_animals_not_found_page(animal_name):
    html_page_template = read_template_file(NOT_FOUND_TEMPLATE_FILE)
    not_found_page = html_page_template.replace(DATA_PLACEHOLDER, animal_name)
    save_to_file(ANIMALS_FILE, not_found_page)


def main():
    """
    Create a HTML file ANIMALS_FILE which lists information about animals whose name matches a string we
    ask from the user.
    :return: None
    """
    html_page_template = read_template_file(TEMPLATE_FILE)
    animal_name = ask_string(message="Enter a name of an animal: ")
    animals_data = data_fetcher.load_animals(animal_name)

    if len(animals_data) == 0:
        make_animals_not_found_page(animal_name)
    else:
        skin_type = ask_which_skin_type(animals_data)
        animal_html_data = html_page_template.replace(DATA_PLACEHOLDER, animals_to_html_list(animals_data, skin_filter=skin_type))
        save_to_file(ANIMALS_FILE, animal_html_data)


if __name__ == '__main__':
    main()
