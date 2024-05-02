import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
import math

# Disable logging from selenium
logging.getLogger('selenium').setLevel(logging.CRITICAL)
# Turn off driver logging
logging.getLogger('webdriver_manager').setLevel(logging.CRITICAL)

# Load .env file
load_dotenv()

# Access environment variables
SERP_API_KEY = os.getenv("SERP_API_KEY")

def search_google_scholar(query, n_results=4):
    search_url = "https://serpapi.com/search"
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": n_results
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
        "num": n_results
    }    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json()
        image_results = results.get("images_results", [])
        image_urls = [{
            "title": result.get("title"),
            "url": result.get("original")
            } for result in image_results]
        return image_urls[:n_results]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
    
def download_image(image_url, save_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False
    

# Initialize Selenium webdriver with Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # To run Chrome in headless mode (without opening GUI)


def extract_webpage_contents(url, max_length=2500):
    driver = webdriver.Chrome(options=chrome_options)
    
    # Load the page with dynamic content
    driver.get(url)
    
    # Wait for JavaScript to render content (adjust the sleep time as needed)
    time.sleep(3)
    
    # Get page source after JavaScript rendering
    page_source = driver.page_source
    
    # Close the webdriver
    driver.quit()
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # return the top biggest sorted elements (contentText length)
    # excluding the script and style tags
    content = [element.get_text() for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'span'])]
    tem_sort_content = sorted(content, key=lambda x: len(x), reverse=True)[:10]
    # sort the results by their index in the original content
    content = sorted(tem_sort_content, key=lambda x: content.index(x))
    # replace all \n with space and trim the text
    content = '\n'.join([text.replace('\n', ' ').strip() for text in content])
    # slice the content to max_length
    content = content[:max_length]    
    return content