from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import re

def extract_journal_details(downType, downYear, downJournals):
    url = 'https://search.ipindia.gov.in/IPOJournal/Journal/Patent'

    response = requests.get(url, verify=False)

    df_jornals_table = pd.DataFrame()

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
        
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all(['th', 'td']):
                row_data.append(cell.get_text())

            data.append(row_data)

        # Create a DataFrame from the extracted data
        df_jornals_table = pd.DataFrame(data[1:], columns=data[0])

        # Output the extracted data
        csv_filename = 'journals_' + str(len (df_jornals_table)) +'.csv'
        folder_path = 'journal_details'
        os.makedirs(folder_path, exist_ok=True)  # This will create the folder if it doesn't exist
        file_path = os.path.join(folder_path, csv_filename)
        df_jornals_table.to_csv(file_path)
        
        def checkyearjournal():
            all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

            # full paths for each file
            full_paths = [os.path.join(folder_path, f) for f in all_files]

            # sort files by modification time (newest first)
            full_paths.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
            # get the last added CSV files
            last_file = full_paths[:1]
            
            #get the latest journal details
            allJournals = pd.read_csv(last_file[0]) 
            filteredJournals = allJournals[allJournals['Journal No.'].str.contains(str(downYear))]
            # print(filteredJournals)

            return(filteredJournals)

        def checknewjournal():
            all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

            # full paths for each file
            full_paths = [os.path.join(folder_path, f) for f in all_files]

            # sort files by modification time (newest first)
            full_paths.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
            # get the last two added CSV files
            last_two_files = full_paths[:2]
            
            #filter the number from the file names 
            numbers = [int(re.search(r'\d+', filename).group()) for filename in last_two_files]

            newRowsinJournal = pd.DataFrame()

            countrowadded = numbers[0] - numbers[1]
            if (countrowadded > 0):
                print("Found " + str(countrowadded) + " new journal...")
                
                #get the latest journal details
                newJournal = pd.read_csv(last_two_files[0])
                newRowsinJournal = newJournal[:countrowadded]
                return(newRowsinJournal)
        
        if(downType == "Year"):
            print("Running year condition")        
            return checkyearjournal()
        elif(downType == "Range"):
            print("Running range condition")
            year1 = downJournals.split("-")[0].split("/")[1]
            year2 = downJournals.split("-")[1].split("/")[1]
            firstJournal = int(downJournals.split("-")[0].split("/")[0])
            lastJournal = int(downJournals.split("-")[1].split("/")[0])
            print (lastJournal)
            if (year1 == year2):
                downYear = year1
                rangeJournals = checkyearjournal()
                rangeJournals['split_col'] = rangeJournals['Journal No.'].str.split('/').str[0].astype(int)
                filteredJournals = rangeJournals[(rangeJournals['split_col'] >= lastJournal) & (rangeJournals['split_col'] <= firstJournal)]
                filteredJournals = filteredJournals.drop(columns=['split_col'])
                print(filteredJournals)
                return filteredJournals
        else:
            return checknewjournal()
        
        def addTestcsv():
            df_test = pd.DataFrame()
            # creates a csv file from the latest file for test
            df_test = pd.read_csv('journal_details/journals_910.csv')
            
            #remove first row - test 
            df_test = df_test.drop(0)
            df_test.reset_index(drop=True, inplace=True)

            # Adjust the "Sr. No." column to start from 1
            df_test['Sr. No.'] = df_test.index + 1

            df_test.to_csv('journal_details/journals_909.csv')

        # addTestcsv() #only for testing
    else:
        return("Failed to fetch the webpage. Status code:", response.status_code)

     #This file can be run independently to extract applications   
if __name__ == "__main__":
    downType = "Range"
    downYear = 0
    downJournals = "32/2021-1/2021"
    df = extract_journal_details(downType, downYear, downJournals)
    csv_filename = 'journals_' + str(len(df)) +'.csv'
    df.to_csv('csv_filename', mode='w', header=True, index=False)