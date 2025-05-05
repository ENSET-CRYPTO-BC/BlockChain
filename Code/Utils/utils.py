import json
from typing import Any


def dump_data(data: Any) -> str:
    """Serialize the given data into a JSON-formatted string.

    Args:
        data (Any): The data to be serialized. It can be any object that is JSON serializable.

    Returns:
        str: A JSON-formatted string representation of the input data.
    """

    return json.dumps(data, indent=4, sort_keys=True)
