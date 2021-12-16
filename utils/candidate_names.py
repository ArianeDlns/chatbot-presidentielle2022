import json
from pathlib import Path
import nltk
import numpy as np

candidates_data = json.loads(Path("data/data_candidates/candidates.json").read_text())
candidates_name = [candidate['name']
                   for candidate in candidates_data['candidates']]

def real_name(name):
    comparaison_name = []
    for names in candidates_name:
        comparaison_name += [nltk.edit_distance(names, name)]
    idx = np.argmin(comparaison_name)
    return candidates_name[idx]