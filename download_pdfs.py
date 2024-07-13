from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil

def download_Pdfs(journal_no):
    journal_no = journal_no.replace('/', '_')

    # Set up Chrome options to handle downloads
    download_dir = "pdf_download_v2"  # Update this to your preferred directory
    temp_dir = "temp"
    temp_download_dir = os.path.join(os.getcwd(), download_dir, temp_dir)  # Temporary directory for downloads

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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Ensure the temporary download directory exists
    os.makedirs(temp_download_dir, exist_ok=True)

    try:
        # Open the webpage
        driver.get("https://search.ipindia.gov.in/IPOJournal/Journal/Patent")

        # Locate dropdown element by its name attribute
        dropdown = Select(driver.find_element(By.NAME, 'Journal_length'))

        # Select option with values "5" "50", "100", "-1" (-1 for all)
        dropdown.select_by_value('-1')
        
        filterforms = []
        jounralPdfsName = []
        rows = driver.find_elements(By.XPATH, "//table[@id='Journal']/tbody/tr")

        for row in rows:
            # extracting data from each row
            journalNo = row.find_element(By.XPATH, "./td[2]").text.strip()
            if (journal_no == journalNo.replace('/', '_')):
                hidden_inputs = row.find_elements(By.XPATH, ".//input[@type='hidden' and @name='FileName']")
                for hInput in hidden_inputs:
                    file_name = hInput.get_attribute("value")
                    # file_id = file_name.split("/")[-2]
                    jounralPdfsName.append(file_name)
                
                filterforms = row.find_elements(By.XPATH, ".//form")
                    
                # all_hidden_input_eachRow = row.find_elements(By.XPATH, "./td[5]/form/input[@name='FileName']")
        
        # Locate all the forms that contain the file information and the buttons
        # forms = driver.find_elements(By.XPATH, "//form[@action='/IPOJournal/Journal/ViewJournal']")
        # # Iterate over each form    
        # for i, form in enumerate(forms):
        #     # Extract the file name from the hidden input field
        #     hidden_input = form.find_element(By.XPATH, ".//input[@type='hidden' and @name='FileName']")
        #     file_name = hidden_input.get_attribute("value")
            
        #     if (journal_no in file_name):
        #         filterforms.append(form)
        #         jounralPdfsName.append(file_name)

        pdfCount = len(jounralPdfsName)
        print (f"Located {pdfCount} PDFs")

        for index, form in enumerate(filterforms):
            # Click the submit button within the form to start the download
            button = form.find_element(By.XPATH, ".//button[@type='submit']")
            button.click()
            print(f"Clicked button {index+1} of {pdfCount} to download journal {journal_no}")

            # Wait for the download to complete
            time.sleep(20)  # Adjust this as necessary to ensure the download completes

            # Move and rename the downloaded file
            # Assuming there's only one file being downloaded at a time in the temp directory
            temp_files = os.listdir(temp_download_dir)
            file_name = str(journal_no) + '_' + str(index+1) + '.pdf'   #pdf file name like 21_2024_1
            # new_file_path = os.path.join(temp_download_dir, new_name)
            if temp_files:
                temp_file_path = os.path.join(temp_download_dir, temp_files[0])
                final_file_path = os.path.join(download_dir, file_name)
                shutil.move(temp_file_path, final_file_path)
                print(f"Downloaded and moved file to {final_file_path}")

    finally:
        # Clean up: Close the browser and remove the temporary download directory
        driver.quit()
        shutil.rmtree(temp_download_dir)
 
 #This file can be run independently to extract applications   
if __name__ == "__main__":
    download_Pdfs('32/2021')
    # print(df)
    # df.to_csv('applications.csv', mode='w', header=True, index=False)