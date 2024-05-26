import fitz
import pandas as pd

def extract_grants(filename):

    journal = fitz.open('/Users/kratik/Documents/GitHub/indian-patent-dataset/pdf_download_v2/' + filename) #enter pdfs downloaded directory
    #print(journal.metadata)

    grant_text_lookup = "Publication Under Section 43(2) in Respect of the Grant"

    page_numbers = []
    for page in journal:
        
        match = page.search_for(grant_text_lookup)
        if (match):
            page_numbers.append(page.number)

    page_num_start_input = page_numbers[0]

    #extract journal details from footer
    page = journal.load_page(page_num_start_input)
    text = page.get_text()
    journal_footer = ''
    for line in text.splitlines():
            if line.startswith('The Patent Office Journal'):
                journal_footer = line.split('   ')[0]
                break

    headers = ['Serial No.', 'Patent Number', 'Application Number', 'Date of Application', 
                                    'Date of Priority', 'Title of Invention', 'Patentee Name', 'Date of Application Publication', 'Office']
    df_grants = pd.DataFrame()

    for page in journal:
        # page.search_for(grant_text_lookup)
        if page.number >= page_num_start_input:
            tabs = page.find_tables()
            if tabs.tables:
                table_data = tabs[0].extract()
                for row in table_data:
                    try:
                        if(len(row)>=6):
                            cleaned_row = [string.replace('\n', ' ') for string in row]
                            # print(cleaned_row)
                            
                            #check if the row's value are of previous page
                            df_grants = pd.concat([df_grants, pd.DataFrame([cleaned_row])], ignore_index=True)
                    except:
                        print (f'Error in file {filename} at page no. {page.number}')

    #handling mismatch of headers - exception
    if len(df_grants.columns) < len(headers):
        new_columns_needed = len(headers) - len(df_grants.columns)
        new_columns = headers[-new_columns_needed:]
        for new_col in new_columns:
            df_grants[new_col] = None
    if len(df_grants.columns) > len(headers):
        df_grants = df_grants.iloc[:, :len(headers)]
    
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
    df_grants['Date of Application Publication'] = df_grants['Date of Application Publication'].astype(str).apply(lambda x: ''.join(x.split()))
    df_grants['Serial No.'].replace('', None, inplace=True)
    df_grants['journal'] = journal_footer.replace('The Patent Office Journal No. ','').replace('Dated  ','')

    df_grants_final = pd.DataFrame()
    df_grants_final = df_grants.dropna(subset=['Serial No.'])
    indices_to_drop = df_grants_final[df_grants_final['Serial No.'].isin(['SerialNumber'])].index
    df_grants_final.drop(indices_to_drop, inplace=True)

    return df_grants_final
    
 #This file can be run independently to extract grants   
if __name__ == "__main__":
    file = '21_2024_2.pdf' #enter file name
    df = pd.DataFrame()

    df = extract_grants(file)
    df.to_csv('grants.csv', mode='w', header=True, index=False)