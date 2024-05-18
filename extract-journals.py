##download PDFs

import os
import requests
import urllib3
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up Selenium webdriver (you need to have the appropriate driver installed, like chromedriver)
driver = webdriver.Chrome()

# URL of the webpage containing the links
url = 'https://search.ipindia.gov.in/IPOJournal/Journal/Patent'

# Load the webpage
driver.get(url)

# Get the page source after the JavaScript has executed
page_source = driver.page_source

# Parse the page source using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all the <input> elements with name="FileName" inside <form> elements
file_inputs = soup.find_all('input', {'name': 'FileName'})

# Construct the full URLs for each part using the base URL
base_url = 'https://search.ipindia.gov.in/IPOJournal/Journal/ViewJournal'
pdf_urls = [urljoin(base_url, file_input['value']) for file_input in file_inputs]

# Create a directory to store the downloaded PDF files
download_dir = 'pdf_downloads'
os.makedirs(download_dir, exist_ok=True)

# Download each PDF file
for pdf_url in pdf_urls:
    # Get the PDF filename
    pdf_filename = pdf_url.split('/')[-1]
    # Download the PDF file using requests
    response = requests.get(pdf_url, verify=False)
    # Save the PDF file to the download directory
    with open(os.path.join(download_dir, pdf_filename), 'wb') as f:
        f.write(response.content)

# Quit the driver when done
driver.quit()
