import os
import fitz
from extract_grants import extract_grants
from extract_applications import extract_applications
from extract_journals import extract_journal_details
from download_pdfs import download_Pdfs

def extractJournalAndDownloadPdfs (): 
    #Download specific year
    downloadType = "Range"     #"Year", "New", "Range"
    downloadYear = 0         #2921, 0, 0
    downRange = "31/2021-1/2021" #Give journals in range,else 0

    #Scan for journals
    filteredJournals = extract_journal_details(downloadType, downloadYear, downRange) #last run: 29/06/2024

    #download pdfs of each new journal
    for index, row in filteredJournals.iterrows():
            print(f"Starting download of {row['Journal No.']}")
            download_Pdfs(row['Journal No.'])

extractJournalAndDownloadPdfs()

#directory where PDFs downloaded
directroy = "pdf_download_v2"
pdf_files = os.listdir(directroy)

design_text_lookup1= "In view of the recent amendment made in the Designs (Amendment) Rules, 2008"
design_text_lookup2= "Design Number"
application_text_lookup = "(12) PATENT APPLICATION PUBLICATION"
grant_text_lookup = "Following Patents have been granted"

grant_pdf_files = []
application_pdf_files = []
design_pdf_files = []

print(f"Total files found {len(pdf_files)}")

#check if the pdf has applications and grants - we are skipping designs
for file in pdf_files:
    if file.endswith('.pdf'):
        print(f"Opening and checking PDF {file}")
        journal = fitz.open('/Users/kratik/Documents/GitHub/indian-patent-dataset/pdf_download_v2/' + file)
        for page in journal:
            match = page.search_for(design_text_lookup1)
            match2 = page.search_for(design_text_lookup2)
            if (match or match2):
                design_pdf_files.append(file)
                print (file + " is a design file, so it is skipped")
                break
            else:
                match4 = page.search_for(application_text_lookup)
                if (match4):
                    application_pdf_files.append(file)
                    break
        for page in journal:
            match3 = page.search_for(grant_text_lookup)
            if (match3):
                grant_pdf_files.append(file)
                break

# application_pdf_files = [i for i in pdf_files if i not in design_pdf_files]

print (grant_pdf_files)
# print (design_pdf_files)
print (application_pdf_files)

csv_file_path = os.path.join('/Users/kratik/Documents/GitHub/indian-patent-dataset/output/grants', '2021_grants.csv') #create a grants.csv
for i,file in enumerate(grant_pdf_files):
    print(file + " is running...")
    df = extract_grants(file)
    header_setting = False
    if (i == 0):
        header_setting = True        
    df.to_csv(csv_file_path, mode='a', header=header_setting, index=False) #save received df in the existing csv
    print(file + " is processed and extracted " + str(len(df)) + " grants")

csv_file_path = os.path.join('/Users/kratik/Documents/GitHub/indian-patent-dataset/output/applications', '2021_applications.csv') #create a application.csv
for i,file in enumerate(application_pdf_files):
    print(file + " is running...")
    df = extract_applications(file)
    header_setting = False
    if (i == 0):
        header_setting = True        
    df.to_csv(csv_file_path, mode='a', header=header_setting, index=False) #save received df in the existing csv
    print(file + " is processed and extracted " + str(len(df)) + " applications")