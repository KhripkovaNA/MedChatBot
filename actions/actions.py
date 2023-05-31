# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
import pandas as pd
import os
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(FILE_DIR, 'data', 'diseases.csv')

class ActionProvideDiseaseInfo(Action):

    def name(self) -> Text:
        return "action_provide_disease_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load the diseases.csv file into a pandas DataFrame
        df = pd.read_csv(DATA_PATH)

        # Extract the user's entity from the tracker
        inquired_disease = next(tracker.get_latest_entity_values("disease"), None)

        if not inquired_disease:
            dispatcher.utter_message(text="Which disease are you interested in?")
            return []

        # Search for the disease in the DataFrame based on the user's query
        disease_info = df[df["name"].str.contains(inquired_disease, case=False)]

        if not disease_info.empty:
            # Extract the relevant information from the DataFrame
            response = disease_info["description"].values[0]

            # Send the response to the user
            dispatcher.utter_message(text=f"Here is some information about {inquired_disease}:")
            dispatcher.utter_message(text=response)

        else:
            dispatcher.utter_message(text="I'm sorry, I couldn't find information about that disease.")

        return []
