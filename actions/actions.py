# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from pathlib import Path
import json

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
        candidates_name = [candidate['name'] for candidate in self.candidates_data['candidates']]
        candidates_party = [candidate['party'] for candidate in self.candidates_data['candidates']]
        candidates_name_party = [f"{candidates_name[i]} ({candidates_party[i]})\n" for i in range(len(candidates_name))]
        dispatcher.utter_message(text=f"Voici la liste des candidats participants aux élections présidentielles de 2022 :\n- {'- '.join(candidates_name_party)}")

        return []

class ActionGetPartyFromCandidate(Action):
    candidates_data = json.loads(Path("data/candidates.json").read_text())
    candidates_name = [candidate['name'] for candidate in candidates_data['candidates']]
    candidates_party = [candidate['party'] for candidate in candidates_data['candidates']]

    def name(self) -> Text:
        return "action_get_party_from_candidate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        for blob in tracker.latest_message['entities']:
            if blob['entity'] == 'candidate_name':
                name = blob['value']
                if name in self.candidates_name:
                    party = self.candidates_party[self.candidates_name.index(name)]
                    dispatcher.utter_message(text=f"Le parti politique de {name} est {party}")
                else:
                    dispatcher.utter_message(text=f"Je ne reconnais pas le nom de ce candidat. L'avez-vous bien écrit ?")
                
        return []