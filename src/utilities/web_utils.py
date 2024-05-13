from typing import List
import requests
import os

# Access environment variables
SERP_API_KEY = os.getenv("SERP_API_KEY")

def search_google(query, n_results=5) -> List[dict]:
    search_url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "google_domain": "google.com",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": n_results,
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json()
        # Extract the top search results
        top_results = results.get("organic_results", [])
        summary_results = [
            {
                "title": result.get("title"),
                "snippet": result.get("snippet"),
                "link": result.get("link"),
            }
            for result in top_results
        ]
        return summary_results[:n_results]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def search_google_images(query, n_results=3):
    search_url = "https://serpapi.com/search"
    params = {
        "engine": "google_images",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": n_results,
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json()
        image_results = results.get("images_results", [])
        image_urls = [
            {"title": result.get("title"), "url": result.get("original")}
            for result in image_results
        ]
        return image_urls[:n_results]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def download_image(image_url, save_path):
    try:
        print(f"Downloading image from: {image_url}")
        response = requests.get(image_url)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        return f"Image saved to: {save_path}"
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "An error occurred while downloading the image."


jina_base_url = "https://r.jina.ai/"
def extract_webpage_contents(url: str, max_length: int = 3500) -> str:
    try:
        target_url = f"{jina_base_url}{url}"
        # Make a request to the Jina Reader API
        response = requests.get(target_url)
        response.raise_for_status()
        # Extract the text content from the response content-type: text/plain
        content = response.text
        if max_length > 0:
            # Adding ellipsis if the content exceeds the maximum length
            ellipsis= ""
            if len(content) > max_length:
                ellipsis="..."
            content = content[:max_length] + ellipsis
        return content
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"
    
