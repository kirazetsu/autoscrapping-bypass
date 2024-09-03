#LU RECODE MINIMAL JANGAN HAPUS NAMA AUTHOR YA ANJING,,LAMMER
import os
import requests
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def download_file(url, folder):
    try:
        local_filename = url.split('/')[-1]
        local_path = os.path.join(folder, local_filename)
        
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f'Downloaded: {local_filename} to {folder}')
    except Exception as e:
        print(f'Failed to download {url}: {e}')

def save_base64_data(data, folder, filename):
    try:
        # Decode base64 data
        header, base64_data = data.split(',', 1)
        file_data = base64.b64decode(base64_data)
        
        local_path = os.path.join(folder, filename)
        
        # Save file data
        with open(local_path, 'wb') as f:
            f.write(file_data)
        
        print(f'Saved base64 data as: {filename}')
    except Exception as e:
        print(f'Failed to save base64 data: {e}')

def scrape_with_selenium(url):
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(5)  # Tunggu beberapa detik untuk memuat JavaScript
        
        page_source = driver.page_source
    finally:
        driver.quit()

    return page_source

def save_assets(url, folder, asset_urls, base64_data):
    for asset_url in asset_urls:
        full_url = urljoin(url, asset_url)
        download_file(full_url, folder)
    
    for base64_item in base64_data:
        filename = base64_item['filename']
        data = base64_item['data']
        save_base64_data(data, folder, filename)

def scrape_website(url, base_folder):
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    
    page_source = scrape_with_selenium(url)
    soup = BeautifulSoup(page_source, 'html.parser')

    asset_urls = set()
    base64_data = []

    # Collect asset URLs
    asset_urls.update(link['href'] for link in soup.find_all('link', href=True) if link['href'].endswith(('.css', '.woff', '.ttf')))
    asset_urls.update(script['src'] for script in soup.find_all('script', src=True) if script['src'].endswith('.js'))
    asset_urls.update(img['src'] for img in soup.find_all('img', src=True))

    # Collect base64 images
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src.startswith('data:image'):
            base64_data.append({
                'filename': f'image_{img.get('alt', 'default')}.png',  # Name file with a unique identifier
                'data': src
            })
    
    save_assets(url, base_folder, asset_urls, base64_data)

def main():
    print ("Author : IronHeart_X12 | Kirazetsu1337")
    target_url = input("Enter the URL of the website to scrape: ")
    output_folder = 'hasil'
    
    print(f"Starting the scraping process for {target_url}...")
    scrape_website(target_url, output_folder)

if __name__ == '__main__':
    main()
