import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

page = requests.get("https://www.ifrap.org/comparateurs/presidentielle-2022")

columns = ['Theme', 'Sub-theme', 'Candidate', 'Proposition', 'Priority', 'Keywords', 'Data_origin', 'Data_source', 'Created_at', 'Updated_at']

#Priority : 1 - Chiffres Clés, 0 - Proposition classique, -1 - Pas de proposition pour l'instant, -2 - Proposition initiale modifiée 

def scrape_programs_list(page):
    
    propositions_list = []
    soup = BeautifulSoup(page.content, 'html.parser')
    sections = soup.find_all('div', {'class' : 'mx-auto p-4 max-w-screen-lg lg:px-6'})[0]

    for section in sections:
        theme = section.find('h2').get_text()
        details = section.find_all('details', {'class' : 'border-t border-gray-100 last-of-type:rounded-b pe'})

        for detail in details:
            sub_theme = detail.select('summary')[0].get_text().replace('\n','')
            ul = detail.find_all('ul', {'class' : 'divide-y'})[0]

            for li in ul:
                candidate_name = li.select('figure')[0].get_text()
                test_propositions = li.select('div')[0].find_all('ol')
                test_key_figures = li.select('div')[0].find_all('div', {'class' : 'mt-4 p-4 rounded-lg border shadow text-sm'})
                test_no_propositions = li.select('div')[0].find_all('p', {'class' : 'text-gray-400'})

                if test_key_figures: # A Reformater 
                    key_figure = test_key_figures[0].get_text().replace('\n','').replace ('  ','')
                    key_figures_detail = [theme, sub_theme, candidate_name, key_figure, 1, "", "Programme", "IFRAP", date.today(), date.today()] # Attention des fois l'origine des données ne provient pas des candidats mais de l'IFRAP, rajouter une fonction pour éviter ce phénomène 
                    propositions_list.append(key_figures_detail)

                if test_propositions:

                    test_details = test_propositions[0].find_all('details')
                    if test_details:
                        for past_proposition in test_details[0].find_all('p'):
                            past_proposition_name = past_proposition.get_text()
                            past_proposition_detail = [theme, sub_theme, candidate_name, past_proposition_name, -2, "", "Programme", "IFRAP", date.today(), date.today()]
                            propositions_list.append(past_proposition_detail)

                    # print(test_propositions[0].find_all('p'))
                    for proposition in test_propositions[0].find_all('p'):
                        proposition_name = proposition.get_text()
                        proposition_detail = [theme, sub_theme, candidate_name, proposition_name, 0, "", "Programme", "IFRAP", date.today(), date.today()]
                        propositions_list.append(proposition_detail)

                if test_no_propositions:
                    candidate_detail = [theme, sub_theme, candidate_name, "Proposition non encore connue", -1, "", "Programme", "IFRAP", date.today(), date.today()]
                    propositions_list.append(candidate_detail)
    
    return propositions_list

def scrape_programs_df(page, columns):
    return pd.DataFrame(scrape_programs_list(page), columns = columns)

propositions_df = scrape_programs_df(page, columns)
propositions_df.to_csv(r"chatbot-presidentielle2022\\utils\\propositions.csv", sep='|') 