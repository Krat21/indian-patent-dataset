from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import shutil

# Set up Chrome options to handle downloads
download_dir = "pdf_download_v3"  # Update this to your preferred directory
temp_download_dir = os.path.join(download_dir, "temp")  # Temporary directory for downloads

chrome_options = Options()
prefs = {
    "download.default_directory": temp_download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the Chrome driver
# service = Service('/path/to/chromedriver')  # Update this to the path of your chromedriver
driver = webdriver.Chrome(options=chrome_options)

# Ensure the temporary download directory exists
os.makedirs(temp_download_dir, exist_ok=True)

try:
    # Open the webpage
    driver.get("https://search.ipindia.gov.in/IPOJournal/Journal/Patent")  # Replace with the actual URL

    # Locate all the forms that contain the file information and the buttons
    forms = driver.find_elements(By.XPATH, "//form[@action='/IPOJournal/Journal/ViewJournal']")

    # Iterate over each form
    for i, form in enumerate(forms):
        # Extract the file name from the hidden input field
        hidden_input = form.find_element(By.XPATH, ".//input[@type='hidden' and @name='FileName']")
        file_name = hidden_input.get_attribute("value")
        file_name = os.path.basename(file_name)  # Get just the file name part

        # Click the submit button within the form to start the download
        button = form.find_element(By.XPATH, ".//button[@type='submit']")
        button.click()
        print(f"Clicked button {i+1} of {len(forms)} to download {file_name}")

        # Wait for the download to complete
        time.sleep(10)  # Adjust this as necessary to ensure the download completes

        # Move and rename the downloaded file
        # Assuming there's only one file being downloaded at a time in the temp directory
        temp_files = os.listdir(temp_download_dir)
        if temp_files:
            temp_file_path = os.path.join(temp_download_dir, temp_files[0])
            final_file_path = os.path.join(download_dir, file_name)
            shutil.move(temp_file_path, final_file_path)
            print(f"Downloaded and moved file to {final_file_path}")

finally:
    # Clean up: Close the browser and remove the temporary download directory
    driver.quit()
    shutil.rmtree(temp_download_dir)
