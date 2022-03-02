import json
from pathlib import Path
import nltk
import numpy as np

def filter_words(theme, w2v_model):
    for c in ["/", "'", ",", "(", ")"]:
        theme = theme.replace(c, " ")
    word_list = [w.lower() for w in theme.split(" ") if len(w) > 2]

    for word in word_list:
        if not word in w2v_model.index_to_key:
            word_list.remove(word)

    return word_list

def mean_similarity(filtered_theme, word_list, w2v_model):
    mean_sim = 0
    for theme_word in filtered_theme:
        mean_sim += np.sum([w2v_model.similarity(word, theme_word) for word in word_list])
    return 1/len(filtered_theme) * mean_sim
            
def embed_theme(theme, list_themes, list_subthemes, w2v_model, threshold=0.4):
    comparison_subtheme, comparison_theme = [], []

    filtered_theme = filter_words(theme, w2v_model)
    if len(filtered_theme) == 0:
        return None, False

    for real_subtheme in list_subthemes:
        word_list = filter_words(real_subtheme, w2v_model)
        comparison_subtheme += [mean_similarity(filtered_theme, word_list, w2v_model)]
    
    idx = np.argmax(comparison_subtheme)
    if comparison_subtheme[idx] >= threshold:
        return list_subthemes[idx], True
    else:
        for real_theme in list_themes:
            word_list = filter_words(real_theme, w2v_model)
            comparison_theme += [mean_similarity(filtered_theme, word_list, w2v_model)]

        idx = np.argmax(comparison_theme)
        return list_subthemes[idx], False