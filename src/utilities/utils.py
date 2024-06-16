import os
from typing import Annotated

project_space = "temp"

def set_project_space(directory: str = "temp"):
    """Set the project space."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    global project_space
    project_space = directory


# Initial number is base on the current time
last_base10_number = 4096


def generate_unique_id():
    """Generate a unique id."""
    global last_base10_number
    last_base10_number += 1
    return hex(last_base10_number)[2:]


def generate_unique_filename(
    prefix: str = "file", extension: str = "txt", subdirectory: str = None
):
    """Generate a unique filename."""
    filename = prefix + "-" + generate_unique_id() + "." + extension
    global project_space
    directory = project_space
    if subdirectory:
        directory = os.path.join(project_space, subdirectory)
        # create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
    return os.path.join(directory, filename)


def write_project_config(
    content: Annotated[
        str, "Text content to be written into the project config document."
    ],
    should_print: Annotated[bool, "Whether to print the content to console."] = True,
):
    """Adds content to the project config file."""
    global project_space
    path = os.path.join(project_space, "project_config.txt")
    if should_print:
        print(content)
    with open(path, "a") as file:
        file.write(content)


def save_draft(
    content: Annotated[str, "Text content to be written into the document."],
    affix: Annotated[str, "The affix to be added to the filename."],
):
    path = generate_unique_filename("draft-" + affix, "txt", subdirectory="drafts")
    """Create and save a text document."""
    with open(path, "w") as file:
        file.write(content)
