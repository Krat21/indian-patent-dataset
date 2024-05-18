import fitz # pip install pymupdf
import pandas as pd
import re

file_name = 'ViewJournal18.5.pdf'
journal = fitz.open('/Users/kratik/Documents/Patent Alert/' + file_name)
#print(journal.metadata)

page_num_start_input = 9 #input the page number of PDF, not the document page number
page_list = []

# Iterate over all the pages in the document
for page in journal:
    if page.number >= page_num_start_input:
        # Extract the text from the page
        content = page.get_text()
        page_list.append(content)
print(page_list)

df_final = pd.DataFrame()
df_applications = pd.DataFrame()

header_count = 27
pattern = r'\((\d{2})\)\s*([^:]+):([\s\S]*?)(?=\(\d{2}\)|$)'

# page_list = [page_list[648]] #test single case
for content in page_list:
    #print(content)
    matches = re.findall(pattern, content)
    extracted_values = {}

    for group1, group2, group3 in matches:
        extracted_values[re.sub(r'\s{2,}', ' ', group2.strip().replace('\n', ''))] = group3.strip()

    #data cleaning:
    #extract application number:
    application_number_pattern = r'Application No\.(\d+ [A-Z])'
    application_number_match = re.search(application_number_pattern, list(extracted_values.keys())[0])
    if application_number_match:
        application_number = application_number_match.group(1)
        extracted_values['application_number'] = application_number
    else:
        application_number = None
        extracted_values['application_number'] = application_number

    #extract page count and claim count:
    page_count_pattern = r'No. of Pages : (\d+)'
    claim_count_pattern = r'No. of Claims : (\d+)'

    def find_count_claim_pages():
        page_count_match = re.search(page_count_pattern, extracted_values['Abstract'])
        claim_count_match = re.search(claim_count_pattern, extracted_values['Abstract'])

        if claim_count_match and page_count_match:
            extracted_values['page_count'] = page_count_match.group(1)
            extracted_values['claim_count'] = claim_count_match.group(1)
        else:
            #abstract gets divided because of double digit in paranthesis search
            if (header_count != len(extracted_values.keys())):
                #Locate all keys between "Abstract" and "application_number"
                abstract_ind = list(extracted_values.keys()).index('Abstract')
                appNum_ind = list(extracted_values.keys()).index('application_number')
                delta = appNum_ind - abstract_ind

                #Find in these keys' values 'No. of Claims', 
                #if found then: append key & value to "Abstract" and call function again, 
                #else append key & value to "Abstract"
                if (delta > 1):
                    for i in range(delta):
                        if ('No. of Claims' in list(extracted_values.values())[abstract_ind + i]):
                            extracted_values['Abstract'] = "".join([extracted_values['Abstract'], list(extracted_values.keys())[abstract_ind + i]])
                            extracted_values['Abstract'] = " : ".join([extracted_values['Abstract'], list(extracted_values.values())[abstract_ind + i]])
                            find_count_claim_pages()
                        else:
                            if i != 0:
                                extracted_values['Abstract'] = "".join([extracted_values['Abstract'], list(extracted_values.keys())[abstract_ind + i]])
                                extracted_values['Abstract'] = " : ".join([extracted_values['Abstract'], list(extracted_values.values())[abstract_ind + i]])
                else:
                    extracted_values['page_count'] = None
                    extracted_values['claim_count'] = None

    find_count_claim_pages()
                
    # date of filing of the application
    extracted_values['Date of filing of Application'] = list(extracted_values.values())[0]

    #extract each International Application, Patent of addition, and Divisinal with filing date
    extracted_values['International Application No'] = extracted_values['International Application No Filing Date'].split('\n')[0].strip()
    extracted_values['International Application Filing Date'] = extracted_values['International Application No Filing Date'].split('\n')[1].strip(':')

    #EXCEPTION - where "Patent of Addition to Application Number Filed on" instead of "Patent of Addition to Application Number Filing Date"    
    try:
        #EXCEPTION - (Patent of Addition) - Application Number is not present and only filing date exist
        if (len(extracted_values['Patent of Addition to Application Number Filing Date'].split('\n')) >= 2):
            extracted_values['Patent of Addition to Application'] = extracted_values['Patent of Addition to Application Number Filing Date'].split('\n')[0].strip()
            extracted_values['Patent of Addition Filing Date'] = extracted_values['Patent of Addition to Application Number Filing Date'].split('\n')[1].strip(':')
        else:
            extracted_values['Patent of Addition to Application'] = extracted_values['Patent of Addition to Application Number Filing Date'].split('\n')[0].strip(':')
            extracted_values['Patent of Addition Filing Date'] = extracted_values['Patent of Addition to Application Number Filing Date'].split('\n')[0].strip(':')
    except KeyError:
        extracted_values['Patent of Addition to Application'] = "NA"
        extracted_values['Patent of Addition Filing Date'] = "NA"

    #EXCEPTION - where "Divisional to Application Number Filed on" instead of "Divisional to Application Number Filing Date"    
    try:
        extracted_values['Divisional to Application'] = extracted_values['Divisional to Application Number Filing Date'].split('\n')[0].strip()
        extracted_values['Divisional Filing Date'] = extracted_values['Divisional to Application Number Filing Date'].split('\n')[1].strip(':')
    except KeyError:
        extracted_values['Divisional to Application'] = "NA"
        extracted_values['Divisional Filing Date'] = "NA"

    #extract applicants and separate the address
    applicants = re.split(r'\n\s*(?=\d+\))', extracted_values['Name of Applicant'])
    address_pattern = r'Address of Applicant\s*:(.*?)(?=\d+\)|$)'
    applicants_list = []
    addresses = []
    for entry in applicants:
        match = re.search(address_pattern, entry, re.DOTALL)
        if match:
            applicant_wo_address = entry.replace(match.group(1),'').replace('\n','').replace('Name of Applicant :','').replace('Address of Applicant :','').strip()
            addresses.append(match.group(1).strip())
        else:
            applicant_wo_address = entry.strip()
            
        applicants_list.append(re.sub(r'\d+\)', '',applicant_wo_address))

    extracted_values['applicants'] = applicants_list
    extracted_values['addresses'] = addresses
    extracted_values['Publication Type'] = 'Early' #NEED TO BE CALCULATED

    # print(extracted_values)

    #extract inventors
    inv_pattern = r'\d+\)([A-Za-z]+.*?)(?=\nAddress)'
    inv_names = re.findall(inv_pattern, extracted_values['Name of Inventor'])
    inv_list = [inv.strip() for inv in inv_names]
    extracted_values['inventor'] = inv_list

    #remove first entry
    for key in list(extracted_values.keys()):
        if 'PATENT APPLICATION PUBLICATION (21) Application' in key:
            del extracted_values[key]

    #add dict as a row to df
    df_temp = pd.DataFrame([extracted_values])
    df_final = pd.concat([df_final, df_temp], ignore_index=True)

# remove junk Abstract columns
# df_final = df_final[df_final.columns[:26]]

df_final['journal'] = file_name.replace('ViewJournal', '').replace('.pdf','')

#page number === no. of rows?

#only main columns are required
df_applications = df_final.get(['application_number', 'Title of the invention', 'Abstract', 'applicants', 'Publication Date',
                        'inventor', 'claim_count', 'Date of filing of Application', 'Publication Type',
                        'Divisional to Application', 'Divisional Filing Date', 'Patent of Addition to Application', 'Patent of Addition Filing Date',
                       'International classification', 'International Application No', 'International Application Filing Date', 'page_count', 'journal'])

df_applications.to_csv('applications.csv')