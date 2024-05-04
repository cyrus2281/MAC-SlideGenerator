from typing import Annotated


def save_draft(
    content: Annotated[str, "Text content to be written into the document."],
    path: Annotated[str, "Path to save the document."],
):
    """Create and save a text document."""
    with open(path, "w") as file:
        file.write(content)
