import pandas as pd
import json
import csv

csvFilePath = 'race_id.csv'
jsonFilePath = open('race_id.json', 'w')
data = {}

df = pd.read_csv (r'race_id.csv')
df.to_json(r'race_id.json')

# for rows in df:
#     print(rows)
    # name = df['Name']
    # data[name] = df['Id']




# with open(csvFilePath) as csvF:
#     csvR = csv.DictReader(csvF)
#     for rows in csvR:
#         name = rows['Name']
#         data[name] = rows['Id']

# data = pandas.read_csv("Athena search.csv", header=0)
# col_1 = list(data.Id)
# print(col_1)