import json
import re

from httpx import Response


def pascal_to_snake(pascal_string: str) -> str:
    """
    Convert a PascalCase string to snake_case.

    :param pascal_string: The input string in PascalCase format.
                          Expected type is str.

    :return: A string converted to snake_case.
             The return type is str.
    """

    # Insert an underscore before each uppercase letter that follows a lowercase letter or digit
    snake_string = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", pascal_string)
    # Handle cases where a lowercase letter follows a sequence of uppercase letters
    snake_string = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", snake_string)

    return snake_string.lower()


def stringify_response(response: Response) -> str:
    """
    Convert the content of an HTTP response to a string with
    specific formatting.

    :param response: An instance of `httpx.Response`
                     representing the HTTP response.

    :return: A string representation of the response content
             with keys in title case and values joined
             by ':', separated by '.'.
    """

    try:
        json_content = response.json()

        formatted_pairs = [
            f"{key.title()}: {value}" for key, value in json_content.items() if isinstance(value, str) and value
        ]

        return ". ".join(formatted_pairs)

    except json.JSONDecodeError:
        return response.text
