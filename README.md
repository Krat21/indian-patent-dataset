# indian-patent-dataset
Dataset of indian patents sourced from indian patent [jounals](https://search.ipindia.gov.in/IPOJournal/Journal/Patent)

The journals are published weekly/bi-weekly.
## About Dataset
Two sets of data: Patent Applications and Patent Grants

applications.csv outputs **Patent Applications**, with following columns:
- Application Number
- Title of invention
- Abstract
- applicants
- Publication Date
- inventor
- claim_count
- Date of filing of Applications
- Publication Type
- Divisional to Application
- Divisional Filing Date
- Patent of Addition to Application
- Patent of Addition Filing Date
- International classification
- International Application No
- International Application Filing Date
- page_count
- journal : For example: 12/2024 22/03/2024 means Journal 12 in year 2024 and dates 22/03/2024.

grants.csv outputs **Patent Grants**, with following columns:
- Patent Number
- Application Number
- Date of Application
- Date of Priority
- Title of Invention
- Patentee Name
- Date of Application Publication
- Office
- journal

## Scripts
extract_application.py : extract applications from a pdf file & outputs csv '2024_applications.csv'

extract_grants.py : extract grants from a pdf file & outputs csv '2024_grants.csv'

extract_journal.py : extract Journal details from [here](https://search.ipindia.gov.in/IPOJournal/Journal/Patent) & outputs csv 'journal_910.csv' (910 journals)
    three modes: 
    "Range" or "Year" or "New"

    range mode - Filter based on a journal range
    Set downloadType = "Range" and downloadYear = 0 and downRange = "31/2021-1/2021"
    outputs dataframe, where journals are of the given ranges, currently supports only same year journal range
    
    year mode - Filter based on a year
    Set downloadType = "Year" and downloadYear = 2021
    outputs dataframe, where journals are of the set year (i.e., 2021)
    
    new mode - find new journal added to IPO - Finds the latest journal(s)
    Set downloadType = "New" and downloadYear = 0
    outputs dataframe, having rows of new journals added, by comparing with previous csv (i.e., 'journal_910.csv')

download_pdfs.py : download PDFs for a given journal ('16/2024')

main.py :  calls each of above scripts

## Coming Soon...
- Years 2017 & before
- extract abstract images in applications
- output in friendly format - json
- Design Patents
- terminal log indicating error page no.
- multi-year range support

## New Update...
- Year 2024 - Latest Journal updated - Journal 39/2024 (27/09/2024)
- Year 2018 Added
- Range Support