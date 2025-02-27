import os
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import trafilatura
import html2text

def get_md_filename(url, domain):
    """
    Maps a URL to its corresponding Markdown filename relative to the output directory.
    
    Args:
        url (str): The URL to map.
        domain (str): The domain of the website (e.g., 'example.com').
    
    Returns:
        str or None: The relative Markdown file path (e.g., 'about/team.md'), or None for external URLs.
    """
    parsed = urlparse(url)
    if parsed.netloc and parsed.netloc != domain:
        return None  # External link
    path = parsed.path.strip('/')
    if not path:
        return 'index.md'  # Homepage
    parts = path.split('/')
    if '.' in parts[-1]:
        parts[-1] = parts[-1].rsplit('.', 1)[0] + '.md'  # Replace extension with .md
    else:
        parts.append('index.md')  # Directory-like URL
    return os.path.join(*parts)

def process_page(url, html_content, output_dir, domain, current_md_filename):
    """
    Processes the HTML content of a page, updates links, and converts it to Markdown.
    
    Args:
        url (str): The URL of the current page.
        html_content (str): The raw HTML content fetched from the URL.
        output_dir (str): The output directory for Markdown files.
        domain (str): The domain of the website.
        current_md_filename (str): The Markdown filename for the current page.
    
    Returns:
        str or None: The processed Markdown content, or None if extraction fails.
    """
    # Extract main content as HTML
    html_main = trafilatura.extract(html_content, output_format="html", include_images=True, include_formatting=True, include_links=True)
    if not html_main:
        return None
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_main, 'html.parser')
    
    # Update all <a> tags with href attributes
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('#'):
            continue  # Skip fragment-only links
        
        # Resolve relative URLs to absolute
        absolute_url = urljoin(url, href)
        parsed = urlparse(absolute_url)
        current_parsed = urlparse(url)
        
        # Check if it's a link to the same page
        if (parsed.netloc == current_parsed.netloc and
            parsed.path == current_parsed.path and
            parsed.query == current_parsed.query):
            a['href'] = '#' + parsed.fragment if parsed.fragment else ''
        # Check if it's an internal link
        elif parsed.netloc == domain or not parsed.netloc:
            target_md = get_md_filename(absolute_url.split('#')[0], domain)
            if target_md:
                current_dir = os.path.dirname(current_md_filename)
                relative_path = os.path.relpath(target_md, current_dir)
                if parsed.fragment:
                    relative_path += '#' + parsed.fragment
                a['href'] = relative_path
        # External links are left unchanged
    
    # Convert modified HTML to Markdown
    h = html2text.HTML2Text()
    h.ignore_tables = True  # Optional: skips tables; adjust as needed
    markdown_content = h.handle(str(soup))
    return markdown_content

def crawl(start_url, output_dir="markdown_output"):
    """
    Crawls the website starting from start_url and saves pages as Markdown files.
    
    Args:
        start_url (str): The URL to start crawling from.
        output_dir (str, optional): Directory to save Markdown files. Defaults to 'markdown_output'.
    """
    queue = [start_url]
    visited = set()
    domain = urlparse(start_url).netloc
    os.makedirs(output_dir, exist_ok=True)
    
    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        print(f"Processing: {url}")
        
        # Fetch the page content
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            continue
        
        # Get the Markdown filename for the current URL
        current_md_filename = get_md_filename(url, domain)
        if current_md_filename is None:
            continue  # Should not happen for internal links
        
        # Process the page and get Markdown content
        markdown = process_page(url, downloaded, output_dir, domain, current_md_filename)
        if markdown:
            full_path = os.path.join(output_dir, current_md_filename)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
        
        # Extract links from the full HTML to continue crawling
        soup = BeautifulSoup(downloaded, 'html.parser')
        for a in soup.find_all('a', href=True):
            link = a['href']
            abs_link = urljoin(url, link)
            link_parsed = urlparse(abs_link)
            if link_parsed.netloc == domain and abs_link not in visited:
                queue.append(abs_link)
        
        time.sleep(1)  # Be polite to the server

def process_url(url, task_id):
    output_dir = f"output/{task_id}"
    crawl(url, output_dir=output_dir)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <start_url>")
        print("Example: python script.py https://example.com")
        sys.exit(1)
    start_url = sys.argv[1]
    crawl(start_url)