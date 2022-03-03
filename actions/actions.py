# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from pathlib import Path
import json
import pandas as pd

from gensim.models import KeyedVectors

from utils.scrapping_sondages import *
from utils.candidate_names import *
from utils.plot_formatting import *
from utils.embed_themes import *

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Loading the word2vec binary model
file_name= "data/word2vec/frWac_non_lem_no_postag_no_phrase_500_skip_cut100.bin"
w2v_model = KeyedVectors.load_word2vec_format(file_name, binary=True, unicode_errors="ignore")

df = pd.read_csv("data/data_candidates/propositions.csv", delimiter='|', encoding = "utf-8")
candidates_name = df['Candidate'].unique()
themes = df['Theme'].unique()
subthemes = df['Sub-theme'].unique()

class ActionGetCandidates(Action):
    candidates_data = json.loads(
        Path("data/data_candidates/candidates.json").read_text())

    def name(self) -> Text:
        return "action_get_candidates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # .encode("latin_1").decode("utf_8")
        candidates_name = [candidate['name']
                           for candidate in self.candidates_data['candidates']]
        candidates_party = [candidate['party']
                            for candidate in self.candidates_data['candidates']]
        candidates_name_party = [
            f"{candidates_name[i]} ({candidates_party[i]})\n" for i in range(len(candidates_name))]
        dispatcher.utter_message(
            text=f"Voici la liste des candidats participants aux élections présidentielles de 2022 :\n- {'- '.join(candidates_name_party)}")

        return []


class ActionGetPartyFromCandidate(Action):
    candidates_data = json.loads(
        Path("data/data_candidates/candidates.json").read_text())
    candidates_name = [candidate['name']
                       for candidate in candidates_data['candidates']]
    candidates_party = [candidate['party']
                        for candidate in candidates_data['candidates']]

    def name(self) -> Text:
        return "action_get_party_from_candidate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text=f"{tracker.latest_message}")

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'candidate_name':
                name = real_name(blob['value'])
                if name in self.candidates_name:
                    party = self.candidates_party[self.candidates_name.index(
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

        dispatcher.utter_message(text=f"{tracker.latest_message}")

        #print(tracker.latest_message['entities'])
        all_names = [blob1['value'] for blob1 in tracker.latest_message['entities'] if blob1['entity'] == 'candidate_name']
        all_themes = [blob2['value'] for blob2 in tracker.latest_message['entities'] if blob2['entity'] == 'theme']
        
        if len(all_names) == 0:
            dispatcher.utter_message(
                text=f"Je n'ai pas compris le nom du candidat concerné. Pouvez-vous reformuler ?")
            return []

        if len(all_themes) == 0:
            dispatcher.utter_message(
                text=f"Je n'ai pas compris le sujet concerné. Pouvez-vous reformuler ?")
            return []

        all_themes_str = ' '.join(all_themes)
        name = real_name(all_names[0], candidates_name)
        theme, is_subtheme = embed_theme(all_themes_str, themes, subthemes, w2v_model)
        if is_subtheme:
            df_propositions = df[(df['Candidate'] == name) & (df['Sub-theme'] == theme)]
        else:
            df_propositions = df[(df['Candidate'] == name) & (df['Theme'] == theme)]

        print(f"Candidate name : {name}")
        print(f"Theme : {theme}")

        if name not in candidates_name:
            dispatcher.utter_message(
                text=f"Je ne reconnais pas le nom de ce candidat : {all_names[0]}. L'avez-vous bien écrit ?")
        elif theme is None:
            dispatcher.utter_message(
                text=f"Je ne reconnais pas le sujet : {all_themes_str}. Pouvez-vous reformuler ?")
        elif int(df_propositions['Priority'].tolist()[0]) == -1:
            dispatcher.utter_message(
                text=f"Le candidat {name} n'a pas fait de proposition sur le sujet {theme[4:-4]} pour l'instant.")
        else:
            propositions = df_propositions[df_propositions['Priority'].astype(int) >= 0]['Proposition'].tolist()
            response = f"Les propositions de {name} sur le sujet {theme[4:-4]} sont les suivantes :\n"
            for proposition in propositions[:200]:
                response += proposition + "\n"
            response = response[:-2]
            dispatcher.utter_message(text=response)

        return []

# --------------------------------------------------
# POLL ACTIONS
# --------------------------------------------------


class ActionGetSondageFromCandidate(Action):
    """
    Answering questions like 'Ou est [candidat_name] dans les sondages ?'
    """
    candidates_data_sondage = get_sondages(
        "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")
    candidates_data = json.loads(
        Path("data/data_candidates/candidates.json").read_text())
    candidates_name = [candidate['name']
                       for candidate in candidates_data['candidates']]

    def name(self) -> Text:
        return "action_get_sondage_candidat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print(tracker.latest_message['entities'])

        for blob in tracker.latest_message['entities']:

            if blob['entity'] == 'candidate_name':
                name = blob['value']
                name_value = ' '.join(real_name(name).split(' ')[1:])
                poll_value = self.candidates_data_sondage.iloc[0][name_value]
                dispatcher.utter_message(
                    text=f"{real_name(name)} est à {poll_value} % dans le dernier sondage ({self.candidates_data_sondage.iloc[0]['Sondeur']} - {self.candidates_data_sondage.iloc[0]['Date']})")
            else:
                dispatcher.utter_message(text=f"Je ne reconnais pas le nom de ce candidat. L'avez-vous bien écrit ? \n Les candidats sont:" + (
                    f"({self.candidates_name[i]})\n" for i in range(len(self.candidates_name))))
        return []


class ActionGetSondageAllCandidates(Action):
    """
    Answering questions like 'Quel est le résultat du dernier sondage ?'
    """
    candidates_data_sondage = get_sondages(
        "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")
    candidates_data = json.loads(
        Path("data/data_candidates/candidates.json").read_text())
    candidates_name = [candidate['name']
                       for candidate in candidates_data['candidates']]

    def name(self) -> Text:
        return "action_get_sondage_all_candidat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        candidates_poll_df = pd.DataFrame([[candidates_name[i], self.candidates_data_sondage.iloc[0][' '.join(
            candidates_name[i].split(' ')[1:])]] for i in range(len(candidates_name))], columns=['Candidats', '(%)']).sort_values(['(%)'], ascending=False)
        
        candidates_poll_value = [
            f"{candidates_poll_df['Candidats'].iloc[i]} ({candidates_poll_df['(%)'].iloc[i]} %)\n" for i in range(len(candidates_name))]

        dispatcher.utter_message(
            text=f"Voici les résultats du dernier sondage  ({self.candidates_data_sondage.iloc[0]['Sondeur']} - {self.candidates_data_sondage.iloc[0]['Date']}):\n- {'- '.join(candidates_poll_value)}")

        #HTML Table displaying 
        #dispatcher.utter_message(json_message={'text': HTML_table_from_df(
        #    candidates_poll_df), 'parse_mode': 'HTML'})

        return []

class ActionGetEvolutionGraphCandidates(Action):
    """
    Answering questions like 'Quel est le résultat du dernier sondage ?'
    """
    candidates_data_sondage = get_sondages(
        "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")
    candidates_data = json.loads(
        Path("data/data_candidates/candidates.json").read_text())
    candidates_name = [candidate['name']
                       for candidate in candidates_data['candidates']]

    def name(self) -> Text:
        return "action_get_evolution_graph_candidat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        candidates_poll_df = pd.DataFrame([[candidates_name[i], self.candidates_data_sondage.iloc[0][' '.join(
            candidates_name[i].split(' ')[1:])]] for i in range(len(candidates_name))], columns=['Candidats', '(%)']).sort_values(['(%)'], ascending=False)
        
        candidates_poll_value = [
            f"{candidates_poll_df['Candidats'].iloc[i]} ({candidates_poll_df['(%)'].iloc[i]} %)\n" for i in range(len(candidates_name))]

        dispatcher.utter_message(
            text=f"Voici les résultats du dernier sondage  ({self.candidates_data_sondage.iloc[0]['Sondeur']} - {self.candidates_data_sondage.iloc[0]['Date']}):\n- {'- '.join(candidates_poll_value)}")

        return []

