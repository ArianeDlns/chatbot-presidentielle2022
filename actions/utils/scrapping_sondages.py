import requests
from bs4 import BeautifulSoup
import pandas as pd
import locale

#locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


def scrape_table(url):
    """
    Get tables from wikipedia url 
    """
    # get the response in the form of html
    wikiurl = url
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl)
    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table', {'class': "wikitable"})
    df = pd.read_html(str(table))
    return df


def clean_sondages(df):
    """
    Clean scrapped tables
    """
    sondages = pd.DataFrame(df[0])
    sondages.columns = [idx[1] for idx in sondages.columns]
    cleaned_sondages = sondages.copy()
    for idx in range(len(sondages)):
        if len(sondages.iloc[idx].unique()) == 1:
            cleaned_sondages = cleaned_sondages.drop(idx)
    return cleaned_sondages.reset_index(drop=True)


def remove_percent(df):
    """replace %"""
    for col in df.columns:
        df[col] = df.apply(lambda x: x[col].replace(
            '<', '').split('%')[0], axis=1)
        df[col] = df.apply(lambda x: 0 if x[col] == '—' else x[col], axis=1)
    return df


def set_date(df):
    df['Dates'] = df.apply(lambda x: x['Dates'].split('-')[1], axis=1)
    df['Dates'] = df.apply(lambda x: x['Dates'].replace(
        '1er', '1') + ' 2021', axis=1)
    return df


def candidate_names_in_cols(df):
    """Set columns as candidate name"""
    columns = [col.split('(')[0] for col in df.columns]
    df.columns = columns
    return df


def remove_empty_col(df):
    """Remove column with Unnamed in names"""
    unnamed = [col for col in df.columns if 'Unnamed' in col]
    df = df.drop(columns=unnamed)
    return df


def apply_transformations(sondages):
    """
    Apply transformations to deal with scrapped data
    """
    #sondages['ChoixLR'] = sondages.apply(lambda x: x.CandidatLR.split('%')[-1], axis=1)
    #sondages['CandidatLR'] = sondages.apply(lambda x: x.CandidatLR.split('%')[0], axis=1)
    #sondages = remove_percent(sondages)
    for col in sondages.columns[3:]:
        sondages[col] = sondages.apply(lambda x: x[col].replace('%', '').replace(
            '<', '').replace(',', '.').replace('—', '0').split('\xa0')[0], axis=1)
        sondages[col] = sondages[col].astype('float')
    sondages = set_date(sondages)
    sondages = candidate_names_in_cols(sondages)
    return sondages


def get_sondages(url):
    df = scrape_table(url)
    sondages = clean_sondages(df)
    sondages = remove_empty_col(sondages)
    sondages = apply_transformations(sondages)
    return sondages


if __name__ == "__main__":
    df = get_sondages(
        "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")
    print(df)