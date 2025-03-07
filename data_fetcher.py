import requests
import os
from dotenv import load_dotenv


load_dotenv()
ANIMALS_API_KEY = os.getenv('ANIMALS_API_KEY')
ANIMALS_API = "https://api.api-ninjas.com/v1/animals"
ALL_SELECTION = "All of them"


def load_animals(animal):
    """
    Fetch data about an anomal family from Animals API
    :param animal: a string to be used as the animals search string
    :return: List of dictionaries. Each dict contains info about one animal that matches the query string.
    """
    api_url = ANIMALS_API + f'?name={animal}'
    response = requests.get(api_url, headers={'X-Api-Key': ANIMALS_API_KEY})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return None


if __name__ == '__main__':
    pass

