import pandas as pd

df = pd.read_csv("data/data_candidates/propositions.csv", delimiter='|', encoding = "ISO-8859-1")
subthemes = df['Sub-theme'].unique()

with open('./subthemes.txt', 'w') as file:
    for subtheme in subthemes:
        print(subtheme)
        file.write(f"    - {subtheme[4:]}\n")