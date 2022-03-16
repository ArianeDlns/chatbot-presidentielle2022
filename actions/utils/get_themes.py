import pandas as pd

PATH = '/app/actions/'
#PATH = './'

df = pd.read_csv(PATH + "data/data_candidates/propositions.csv", delimiter='|', encoding = "ISO-8859-1")
subthemes = df['Theme'].unique()

with open('./themes.txt', 'w') as file:
    for subtheme in subthemes:
        print(subtheme)
        file.write(f"    - {subtheme[1:]}\n")