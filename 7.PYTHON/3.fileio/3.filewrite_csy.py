filename = "data.csv"

#with open(filename, "w", newline="") as file:
#    csv_writer = csv.writer(file)
#    csv_writer.writerows(data)

data2 = [
    {"Name":"John", "Age":25, "City":"Seoul"},
    {"Name":"James", "Age":23, "City":"Busan"},
    {"Name":"Bob", "Age":24, "City":"Seoul"}
]

with open(filename, "w", newline="") as file:
    #headers = ["Name", "Age", "City"]
    headers = data2[0].keys()
    csv_writer = csv.DicWriter(file, fieldnames = headers)
    csv_writer.writeheaders()
    csv_writer.writerows(data2)