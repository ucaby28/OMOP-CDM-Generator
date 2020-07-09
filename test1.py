import pandas

data = pandas.read_csv("Athena search.csv", header=0)
col_1 = list(data.Id)
print(col_1)