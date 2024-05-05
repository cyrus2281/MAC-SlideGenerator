from typing import Annotated, List, Optional
from langchain_core.tools import tool
from utilities.utils import generate_unique_filename
from utilities.web_utils import (
    search_google_images,
    download_image as download_image_util,
)


@tool
def google_image_search(
    query: Annotated[str, "The search query to be used"],
) -> Annotated[
    List[dict],
    "A list of dictionaries containing the top search results with keys 'title' and 'url'",
]:
    """Searches Google Images for the specified query and returns the top search results"""
    return search_google_images(query)


@tool
def download_image(
    image_url: Annotated[str, "The URL of the image to download"]
) -> Annotated[str, "The path where the image was saved"]:
    """Downloads the specified image from the URL to the specified path"""
    image_path = generate_unique_filename("image", "png", "img")
    return download_image_util(image_url, image_path)
