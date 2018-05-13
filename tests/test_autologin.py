from pyeq import *


def test_reading_character_file():
    characters = load_character_list('./tests/test_characterfile')
    assert characters[0]['name'] != 'Shek'
