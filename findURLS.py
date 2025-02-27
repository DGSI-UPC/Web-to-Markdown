import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_links(base_url):
    # Send a GET request to the base URL
    response = requests.get(base_url)
    
    # If the request was successful, proceed
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <a> tags (which represent hyperlinks)
        links = soup.find_all('a', href=True)
        
        # Use urljoin to construct full URLs from relative URLs
        full_urls = [urljoin(base_url, link['href']) for link in links]
        
        # Return the list of full URLs
        return full_urls
    else:
        # If the request fails, print an error message and return an empty list
        print(f"Error: Unable to fetch {base_url}")
        return []

# Example usage
base_url = 'https://example.com'  # Replace with your target base URL
urls = get_all_links(base_url)
print(urls)