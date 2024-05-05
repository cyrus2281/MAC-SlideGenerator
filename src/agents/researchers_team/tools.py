from typing import Annotated, List, Optional
from langchain_core.tools import tool
from utilities.web_utils import extract_webpage_contents, search_google as search_google_util


@tool
def search_google(
    query: Annotated[str, "The search query to be used"],
) -> Annotated[
    List[dict],
    "A list of dictionaries containing the top search results with keys 'title', 'snippet', and 'link'",
]:
    """Searches Google for the specified query and returns the top search results"""
    return search_google_util(query)


@tool
def scrape_webpage(
    url: Annotated[str, "The URL of the webpage to scrape"],
    max_length: Annotated[Optional[int], "The maximum number of characters to return"],
) -> Annotated[str, "The important contents of the webpage"]:
    """Scrapes the specified webpage and returns its important contents"""
    return extract_webpage_contents(url, max_length) or "An error occurred. Try to use your own knowledge."
