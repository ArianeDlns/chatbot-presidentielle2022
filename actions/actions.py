# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from pathlib import Path
import json

from utils.scrapping_sondages import *
from utils.candidate_names import *

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCandidates(Action):
    candidates_data = json.loads(Path("data/candidates.json").read_text())

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
    candidates_data = json.loads(Path("data/candidates.json").read_text())
    candidates_name = [candidate['name']
                       for candidate in candidates_data['candidates']]
    candidates_party = [candidate['party']
                        for candidate in candidates_data['candidates']]

    def name(self) -> Text:
        return "action_get_party_from_candidate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        dispatcher.utter_message(text=f"{tracker.latest_message}")

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'candidate_name':
                name = blob['value']
                if name in self.candidates_name:
                    party = self.candidates_party[self.candidates_name.index(
                        name)]
                    dispatcher.utter_message(
                        text=f"Le parti politique de {name} est {party}")
                else:
                    dispatcher.utter_message(
                        text=f"Je ne reconnais pas le nom de ce candidat. L'avez-vous bien écrit ?")

        return []


class ActionGetPartyFromCandidate(Action):
    """
    Answering questions like 'Ou est [candidat_name] dans les sondages ?'
    """
    candidates_data_sondage = get_sondages(
        "https://fr.wikipedia.org/wiki/Liste_de_sondages_sur_l%27%C3%A9lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")
    candidates_data = json.loads(Path("data/candidates.json").read_text())
    candidates_name = [candidate['name']
                       for candidate in candidates_data['candidates']]

    def name(self) -> Text:
        return "action_get_sondage_candidat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        for blob in tracker.latest_message['entities']:

            if blob['entity'] == 'candidate_name':
                name = blob['value']
                name_value = ' '.join(real_name(name).split(' ')[1:])
                poll_value = self.candidates_data_sondage.iloc[0][name_value]
                dispatcher.utter_message(
                    text=f"{real_name(name)} est à {poll_value} dans le dernier sondage ({self.candidates_data_sondage.iloc[0]['Sondeur']} - {self.candidates_data_sondage.iloc[0]['Date']})")
            else:
                dispatcher.utter_message(text=f"Je ne reconnais pas le nom de ce candidat. L'avez-vous bien écrit ? \n Les candidats sont:" + (
                    f"({self.candidates_name[i]})\n" for i in range(len(self.candidates_name))))
        return []
