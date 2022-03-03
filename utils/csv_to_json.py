'''
Script to convert the csv Dataframe to a JSON file.
Use command : python utils/csv_to_json.py data/csv_DataFrame.csv data/json_DataFrame.json
'''

import csv
import sys
import json

args = sys.argv
csv_filepath = args[1]
json_filepath = args[2]

if csv_filepath[-3:] != 'csv' or json_filepath[-4:] != 'json':
    raise Exception("Please use a csv filepath for the first agument and a json filepath for the second argument")

with open(csv_filepath, 'r') as csvfile:
    data = [row for row in csv.reader(csvfile, delimiter=';')]
    dict = {}

    for row in data[1:]:
        theme, sub_theme, candidate, proposition = row[1], row[2], row[3], row[4]
        if theme in dict:
            if sub_theme in dict[theme]:
                if candidate in dict[theme][sub_theme]:
                    dict[theme][sub_theme][candidate].append(proposition)
                else:
                    dict[theme][sub_theme][candidate] = [proposition]
            else:
                dict[theme][sub_theme] = {candidate: [proposition]}
        else:
            dict[theme] = {sub_theme: {candidate: [proposition]}}

    with open(json_filepath, 'w') as f:
        json.dump(dict, f)
    