import json
import csv

with open('Data-Collection/Helper-Functions/Fund-Makeups/adage.json', 'r') as file:
    json_data = json.load(file)

data = []
for row in json_data['rows']:
    name = row['name']
    current_percent_of_portfolio = row['current_percent_of_portfolio'] / 100
    data.append({'name': name, 'current_percent_of_portfolio': current_percent_of_portfolio})

# Write the data to a CSV file
with open('Data-Collection/Helper-Functions/Fund-Makeups/adage.csv', 'w', newline='') as file:
    fieldnames = ['name', 'current_percent_of_portfolio']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)

print("Data written to 'output.csv' successfully.")