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
- journal : For example: 18/2024.5 means Journal 18 in year 2024 and PDF file 5.

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
extract-journal.py : Extract Journal from [here](https://search.ipindia.gov.in/IPOJournal/Journal/Patent) in a table format

extract-application.py : Extract applications from a give journal and pdf file

extract-grants.py : Extract grants from a give journal and pdf file

## Coming Soon...
extract abstract images in applications
