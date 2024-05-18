from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://search.ipindia.gov.in/IPOJournal/Journal/Patent'

response = requests.get(url)

df_jornals = pd.DataFrame()

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    html_content = response.text

    # Find the table
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    # print (table)

    # Extract data from the table
    data = []
    links = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            row_data.append(cell.get_text())

        data.append(row_data)

    # Create a DataFrame from the extracted data
    df_jornals = pd.DataFrame(data[1:], columns=data[0])

    # Print the extracted data
    # print(df_jornals)
    df_jornals.to_csv('journals.csv')
else:
    print("Failed to fetch the webpage. Status code:", response.status_code)

##download PDFs

import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
    response = requests.get(pdf_url)
    # Save the PDF file to the download directory
    with open(os.path.join(download_dir, pdf_filename), 'wb') as f:
        f.write(response.content)

# Quit the driver when done
driver.quit()
