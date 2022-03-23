# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker

from typing import Any, Text, Dict, List
from pathlib import Path
import json
import pandas as pd

from gensim.models import KeyedVectors

import sys
sys.path.append('/app/actions')
#sys.path.remove('/app/actions')

from utils.embed_themes import *
from utils.plot_formatting import *
from utils.candidate_names import *
from utils.scrapping_sondages import *

PATH = '/app/actions/'
#PATH = './'

# Loading the word2vec binary model
file_name = PATH + "data/word2vec/frWac_non_lem_no_postag_no_phrase_500_skip_cut100.bin"
w2v_model = KeyedVectors.load_word2vec_format(
    file_name, binary=True, unicode_errors="ignore")

# Loading the candidates JSON file
candidates_data = json.loads(
    Path(PATH + "data/data_candidates/candidates.json").read_text())
candidates_name = [candidate['name']
                   for candidate in candidates_data['candidates']]
candidates_party = [candidate['party']
                    for candidate in candidates_data['candidates']]
candidates_info = pd.DataFrame(json.loads(
    Path(PATH + "data/data_candidates/candidates_infos.json").read_text(encoding='utf-8'))['candidates'])

# Loading the propositions CSV file (scrapped from IFRAP)
df = pd.read_csv(PATH + "data/data_candidates/propositions.csv",
                 delimiter='|', encoding="utf-8")
names = df['Candidate'].unique()
themes = df['Theme'].unique()
subthemes = df['Sub-theme'].unique()


class ActionGetCandidates(Action):

    def name(self) -> Text:
        return "action_get_candidates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # .encode("latin_1").decode("utf_8")
        candidates_name_party = [
            f"{candidates_name[i]} ({candidates_party[i]})\n" for i in range(len(candidates_name))]
        dispatcher.utter_message(
            text=f"Voici la liste des candidats participants aux élections présidentielles de 2022 :\n- {'- '.join(candidates_name_party)}")

        return []

class ActionGetCandidatesInfo(Action):

    def name(self) -> Text:
        return "action_get_candidates_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        all_names = [real_name(blob1['value'],candidates_name) for blob1 in tracker.latest_message['entities']
                     if blob1['entity'] == 'candidate_name']
        img = candidates_info[candidates_info['firstname']==all_names[0].split(" ")[0]].imageProfile.values[0]
        path = 'https://raw.githubusercontent.com/ArianeDlns/chatbot-presidentielle2022/main/actions/data'
        img_path = path + img[3:-1]
        #print(img_path)

        if len(all_names) == 0:
            dispatcher.utter_message(
                text=f"Je n'ai pas compris le nom du candidat concerné. Pouvez-vous reformuler ?")
            return []

        else:
            text = f'Voici {all_names[0]}'
            dispatcher.utter_message(text=text, image=img_path)

            age = candidates_info[candidates_info['firstname']==all_names[0].split(" ")[0]].age.values[0]
            etudes = candidates_info[candidates_info['firstname']==all_names[0].split(" ")[0]].studies.values[0] 
            url = "https://fr.wikipedia.org/wiki/"+'_'.join(all_names[0].split(" "))
            print(url)
            response = f"*{all_names[0]}* a {age} ans et a étudié à {etudes} pour en savoir plus, je vous invite à consulter le [profil du candidat]({url})" 
            dispatcher.utter_message(
                    json_message={'text': response, 'parse_mode': 'markdown'})

            return []


class ActionGetPartyFromCandidate(Action):

    def name(self) -> Text:
        return "action_get_party_from_candidate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text=f"{tracker.latest_message}")

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'candidate_name':
                name = real_name(blob['value'], candidates_name)
                if name in candidates_name:
                    party = candidates_party[candidates_name.index(
                        name)]
                    dispatcher.utter_message(
                        text=f"Le parti politique de {name} est {party}")
                else:
                    dispatcher.utter_message(
                        text=f"Je ne reconnais pas le nom de ce candidat. L'avez-vous bien écrit ?")

        return []


class ActionGetPropositionsFromCandidateAndTheme(Action):

    def name(self) -> Text:
        return "action_get_propositions_from_candidate_and_theme"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # print(tracker.latest_message['entities'])
        all_names = [blob1['value'] for blob1 in tracker.latest_message['entities']
                     if blob1['entity'] == 'candidate_name']
        all_themes = [blob2['value']
                      for blob2 in tracker.latest_message['entities'] if blob2['entity'] == 'theme']

        if len(all_names) == 0:
            dispatcher.utter_message(
                text=f"Je n'ai pas compris le nom du candidat concerné. Pouvez-vous reformuler ?")
            return []

        if len(all_themes) == 0:
            dispatcher.utter_message(
                text=f"Je n'ai pas compris le sujet concerné. Pouvez-vous reformuler ?")
            return []
        
        temp = []
        for theme in all_themes:
            try: 
                theme = int(theme)
                if isinstance(theme, int): 
                    temp += [subthemes[theme]]
                all_themes = temp
            except: 
                pass
            
        all_themes_str = ' '.join(all_themes)
        name = real_name(all_names[0], names)
        theme, is_subtheme = embed_theme(
            all_themes_str, themes, subthemes, w2v_model)

        if is_subtheme:
            df_propositions = df[(df['Candidate'] == name)
                                 & (df['Sub-theme'] == theme)]
        else:
            df_propositions = df[(df['Candidate'] == name)
                                 & (df['Theme'] == theme)]

        print(f"Candidate name : {name}")
        print(f"Theme : {theme}")

        if name not in names:
            dispatcher.utter_message(
                text=f"Je ne reconnais pas le nom de ce candidat : {all_names[0]}. L'avez-vous bien écrit ?")
        elif theme is None:
            text = f"Je ne reconnais pas le sujet : *{all_themes_str}*. Pouvez-vous reformuler ?"
            dispatcher.utter_message(
                json_message={'text': text, 'parse_mode': 'markdown'})
        elif int(df_propositions['Priority'].tolist()[0]) == -1:
            text = f"Le candidat{name} n'a pas fait de proposition sur le sujet *{theme[4:-4]}* pour l'instant."
            dispatcher.utter_message(
                json_message={'text': text, 'parse_mode': 'markdown'})
        else:
            propositions = df_propositions[df_propositions['Priority'].astype(
                int) >= 0]['Proposition'].tolist()
            response = f"Les propositions de{name} sur le sujet *{theme[4:-4]}* sont les suivantes :\n \n"
            for proposition in propositions[:200]:
                response += "- " + proposition + "\n"
            response = response[:-2]
            response += "\n\n Source: Ifrap" #(https://www.ifrap.org/comparateurs/presidentielle-2022)"
            dispatcher.utter_message(
                json_message={'text': response, 'parse_mode': 'markdown'})
        return []

# --------------------------------------------------
# INTERACTIVE PROGRAM 
# --------------------------------------------------

class ActionProgrammInteractive(Action):
    """
    Answering questions like 'Quel est le programme de [Macron] ?'
    """

    def name(self) -> Text:
        return "action_get_interactive_program"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = []
        for idx,theme in enumerate(themes):
            # Limit of 64 bytes: https://github.com/yagop/node-telegram-bot-api/issues/706
            #payload = "/theme_cand{\"candidate_name\":\"" + tracker.latest_message['entities'][0]['value'].split(" ")[-1] + "\", \"theme\":\"" + str(idx) + "\"}"
            payload = "/demande_subthemes{\"candidate_name\":\"" + tracker.latest_message['entities'][0]['value'].split(" ")[-1] + "\", \"theme\":\"" + str(idx) + "\"}"
            #print(payload)
            buttons.append({"title": theme, "payload": payload})
        response = "Quel est le sujet qui vous interesse 🤔 ? "
        dispatcher.utter_message(
            text=response, buttons=buttons, button_type="vertical")
        return []

class ActionProgrammSubthemesInteractive(Action):
    """
    'Action to display subthems'
    """

    def name(self) -> Text:
        return "action_get_interactive_subthemes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        subthemes_thems = df[df['Theme'] == themes[int(tracker.latest_message['entities'][1]['value'])]]['Sub-theme'].unique()
        buttons = []
        for subtheme in subthemes_thems:
            # Limit of 64 bytes: https://github.com/yagop/node-telegram-bot-api/issues/706
            idx = list(subthemes).index(subtheme) #np.where(subthemes == subtheme) #subthemes.index(subtheme)
            payload = "/theme_cand{\"candidate_name\":\"" + tracker.latest_message['entities'][0]['value'].split(" ")[-1] + "\", \"theme\":\"" + str(idx) + "\"}"
            #print(payload)
            buttons.append({"title": subtheme, "payload": payload})
        response = "Quel est le sujet précis qui vous interesse 🤔 ? "
        dispatcher.utter_message(
            text=response, buttons=buttons, button_type="vertical")
        return []

# --------------------------------------------------
# POLL ACTIONS
# --------------------------------------------------


class ActionGetSondageFromCandidate(Action):
    """
    Answering questions like 'Ou est [candidat_name] dans les sondages ?'
    """

    def name(self) -> Text:
        return "action_get_sondage_candidat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # print(tracker.latest_message['entities'])
        #dispatcher.utter_message(text=f"Laissez-moi le temps de récupérer les derniers sondages ... ")

        candidates_data_sondage = get_sondages(
            "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")

        for blob in tracker.latest_message['entities']:

            if blob['entity'] == 'candidate_name':
                name = blob['value']
                name_value = ' '.join(real_name(name).split(' ')[1:])
                poll_value = candidates_data_sondage.iloc[0][name_value]
                dispatcher.utter_message(
                    text=f"{real_name(name, candidates_name)} est à {poll_value} % dans le dernier sondage ({candidates_data_sondage.iloc[0]['Sondeur']} - {candidates_data_sondage.iloc[0]['Dates']})")

            else:
                dispatcher.utter_message(text=f"Je ne reconnais pas le nom de ce candidat. L'avez-vous bien écrit ? \n Les candidats sont:" + (
                    f"({candidates_name[i]})\n" for i in range(len(candidates_name))))
        return []


class ActionGetSondageAllCandidates(Action):
    """
    Answering questions like 'Quel est le résultat du dernier sondage ?'
    """

    def name(self) -> Text:
        return "action_get_sondage_all_candidat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text=f"Laissez-moi le temps de récupérer les derniers sondages ... ")

        candidates_data_sondage = get_sondages(
            "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")

        candidates_poll_df = pd.DataFrame([[candidates_name[i], candidates_data_sondage.iloc[0][' '.join(
            candidates_name[i].split(' ')[1:])]] for i in range(len(candidates_name))], columns=['Candidats', '(%)']).sort_values(['(%)'], ascending=False)

        candidates_poll_value = [
            f"{candidates_poll_df['Candidats'].iloc[i]} ({candidates_poll_df['(%)'].iloc[i]} %)\n" for i in range(len(candidates_name))]

        dispatcher.utter_message(
            text=f"Voici les résultats du dernier sondage  ({candidates_data_sondage.iloc[0]['Sondeur']} - {candidates_data_sondage.iloc[0]['Dates']}):\n- {'- '.join(candidates_poll_value)}")
        
        response = "Pour plus d'informations sur les sondages, je vous invite à aller consulter ces très bon sites sur l'évolution des scores: [Electracker](https://electracker.fr/) et [Depuis1958](https://depuis1958.fr/2022/)"
        dispatcher.utter_message(
                json_message={'text': response, 'parse_mode': 'markdown'})
        # HTML Table displaying
        # dispatcher.utter_message(json_message={'text': HTML_table_from_df(
        #    candidates_poll_df), 'parse_mode': 'HTML'})

        return []


class ActionGetEvolutionGraphCandidates(Action):
    """
    Answering questions like 'Quel est le résultat du dernier sondage ?'
    """
    candidates_data_sondage = get_sondages(
        "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")

    def name(self) -> Text:
        return "action_get_evolution_graph_candidat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        candidates_poll_df = pd.DataFrame([[candidates_name[i], candidates_data_sondage.iloc[0][' '.join(
            candidates_name[i].split(' ')[1:])]] for i in range(len(candidates_name))], columns=['Candidats', '(%)']).sort_values(['(%)'], ascending=False)

        candidates_poll_value = [
            f"{candidates_poll_df['Candidats'].iloc[i]} ({candidates_poll_df['(%)'].iloc[i]} %)\n" for i in range(len(candidates_name))]

        dispatcher.utter_message(
            text=f"Voici les résultats du dernier sondage  ({candidates_data_sondage.iloc[0]['Sondeur']} - {candidates_data_sondage.iloc[0]['Dates']}):\n- {'- '.join(candidates_poll_value)}")

        response = "Pour plus d'informations sur les sondages, je vous invite à aller consulter ce très bon site sur l'évolution des scores: [Electracker](https://electracker.fr/) et [Depuis1958](https://depuis1958.fr/2022/)"
        dispatcher.utter_message(
                json_message={'text': response, 'parse_mode': 'markdown'})
        return []
