import fitz
import pandas as pd
import re

file_name = 'ViewJournal18.5.pdf'
journal = fitz.open('/Users/kratik/Documents/Patent Alert/' + file_name)
#print(journal.metadata)

grant_text_lookup = "Publication Under Section 43(2) in Respect of the Grant"

page_numbers = []
for page in journal:
    match = page.search_for(grant_text_lookup)
    if (match):
        page_numbers.append(page.number)

page_num_start_input = page_numbers[0]

headers = ['Serial No.', 'Patent Number', 'Application Number', 'Date of Application', 
                                  'Date of Priority', 'Title of Invention', 'Patentee Name', 'Date of Application Publication', 'Office', 'journal']
df_grants = pd.DataFrame()

df_temp = pd.DataFrame()
for page in journal:
     page.search_for(grant_text_lookup)
     if page.number >= page_num_start_input:
        tabs = page.find_tables()
        if tabs.tables:
           table_data = tabs[0].extract()
           for row in table_data:
               cleaned_row = [string.replace('\n', ' ') for string in row]
               #check if the row's value are of previous page
               df_grants = pd.concat([df_grants, pd.DataFrame([cleaned_row])], ignore_index=True)

df_grants.columns = headers

#clean the dataframe
for index, row in df_grants.iterrows():
    if not row['Serial No.']:
        for head in headers:
            df_grants.loc[index - 1, head] = str(df_grants.loc[index - 1, head]) + ' ' + str(df_grants.loc[index, head])
#remove extra spaces
df_grants['Serial No.'] = df_grants['Serial No.'].apply(lambda x: ''.join(x.split()))
df_grants['Patent Number'] = df_grants['Patent Number'].apply(lambda x: ''.join(x.split()))
df_grants['Application Number'] = df_grants['Application Number'].apply(lambda x: ''.join(x.split()))
df_grants['Date of Application'] = df_grants['Date of Application'].apply(lambda x: ''.join(x.split())).str[:10] #remove time from date, if exists
df_grants['Date of Priority'] = df_grants['Date of Priority'].apply(lambda x: ''.join(x.split()))
df_grants['Date of Application Publication'] = df_grants['Patent Number'].apply(lambda x: ''.join(x.split()))
df_grants['Serial No.'].replace('', None, inplace=True)
df_grants['journal'] = file_name.replace('ViewJournal', '').replace('.pdf','')

df_grants_final = pd.DataFrame()
df_grants_final = df_grants.dropna(subset=['Serial No.'])
indices_to_drop = df_grants_final[df_grants_final['Serial No.'].isin(['SerialNumber'])].index
df_grants_final.drop(indices_to_drop, inplace=True)

df_grants_final.to_csv('grants.csv')