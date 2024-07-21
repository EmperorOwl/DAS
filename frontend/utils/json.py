""" Code for some utility methods. """
import json


def read_data_from_json_file(path: str) -> dict:
    """ Returns the data stored in the Json file as a Python dict.
    If the file is not found, then an empty dictionary is returned.
    """
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def write_data_to_json_file(path: str, new_data: dict) -> None:
    """ Overwrites the current data in the Json file with the new data.
    :raises FileNotFoundError: if the file cannot be found
    """
    with open(path, 'w') as file:
        json.dump(new_data, file, indent=2)
