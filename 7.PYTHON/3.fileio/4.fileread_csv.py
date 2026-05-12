import csv

filename = "data.csv"

with open(filename, "r") as file:
    csv_reader =  csv.reader(file)
    for row in csv_reader:
        print(row)

print(data)

data2=[]
with open(filename, "r") as file:
    csv_reader =  csv.DictReader(file)
    for row in csv_reader:
        data2.append(row)

print(data2)