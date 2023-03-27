# voorbeeld aangeleverde data
data34 = ['meting34', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z']
data35 = ['meting35', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z']
data36 = ['meting36', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z']

newdata = ['meting34', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z']
newdata.insert(len(newdata), data35)

# importeren van app ding

import csv

# alle data die opgeslagen wordt/is

rows = [['meting1', 'stoel', 'tijd', 'nagalm tijd', 'x', 'y', 'z'],
        ['meting2', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z'],
        ['meting3', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z'],
        ['meting4', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z'],
        ['meting5', 'stoel', 'tijd', 'nagalm tijd', 'x', 'y', 'z']]

# het scrhijven van nieuw lines, oftwel nieuwe data overnemen in de csv file.

rows.insert(len(rows), data34)
rows.insert(len(rows), data35)
rows.insert(len(rows), data36)

# kolom naam

titel = ['meting', 'stoel', 'tijd', 'nagalmtijd', 'x', 'y', 'z']

# naam van document

filename = "meting1_pathe_experiment.csv"

# het opschrijven van de daadwerkelijke file

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(titel)
    csvwriter.writerow(rows)

# nu moet de data hierboven vervangen worden door echte data opnames.
