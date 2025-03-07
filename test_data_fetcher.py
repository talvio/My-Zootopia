import pytest
from animals_web_generator import load_animals

def test_load_animals():
    foxes = load_animals("fox")
    assert foxes[0].get('name') is not None
