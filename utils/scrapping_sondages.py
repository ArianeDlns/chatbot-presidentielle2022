import requests
from bs4 import BeautifulSoup
import pandas as pd
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

def scrape_table(url):
    """
    Get tables from wikipedia url 
    """
    # get the response in the form of html
    wikiurl=url
    table_class="wikitable sortable jquery-tablesorter"
    response=requests.get(wikiurl)
    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    table=soup.find('table',{'class':"wikitable"})
    df=pd.read_html(str(table))
    return df

def clean_sondages(df):
    """
    Clean scrapped tables
    """
    sondages = pd.DataFrame(df[0])
    sondages.columns = [idx[1] for idx in sondages.columns]
    cleaned_sondages = sondages.copy()
    for idx in range(len(sondages)):
        if len(sondages.iloc[idx].unique()) == 1 :
            cleaned_sondages = cleaned_sondages.drop(idx)
    return cleaned_sondages.reset_index(drop=True)

def remove_percent(df):
    """replace %"""
    for col in df.columns:
        df[col] = df.apply(lambda x: x[col].replace('<','').split('%')[0], axis=1)
        df[col] = df.apply(lambda x: 0 if x[col] == '—' else x[col], axis=1)
    return df

def set_date(df):
    df['Date'] = df.apply(lambda x: x['Date'].split('-')[1], axis=1)
    df['Date'] = df.apply(lambda x: x['Date'].replace('1er','1') + ' 2021', axis=1)
    return df 

def apply_transformations(sondages):
    """
    Apply transformations to deal with scrapped data
    """
    #Useful for multi LR candidates
    #sondages['ChoixLR'] = sondages.apply(lambda x: x.CandidatLR.split('%')[-1], axis=1)
    #sondages['CandidatLR'] = sondages.apply(lambda x: x.CandidatLR.split('%')[0], axis=1)
    #sondages = remove_percent(sondages)
    sondages = set_date(sondages)
    return sondages

def get_sondages(url):
    df = scrape_table(url)
    sondages = clean_sondages(df)
    sondages = apply_transformations(sondages)
    return sondages

if __name__ =="__main__":
    df = get_sondages("https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")

