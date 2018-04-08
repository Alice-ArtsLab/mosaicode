import os
import tempfile


def get_absolute_path_from_file(filename):
    """Gets the absolute path from received file.

        :param filename: file to obtain the absolute path.
        :return: absolute path from file.
    """
    directory = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(directory, filename)
    filename = os.path.abspath(os.path.realpath(filename))

    return filename


def get_temp_file():
    """Gets the temporary file.

        :return: temporary file.
    """
    with tempfile.NamedTemporaryFile() as file:
        return file.name

