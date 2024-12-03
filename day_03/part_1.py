import re
import csv

totals = []

with open("input.csv", 'r') as file:
    csv_file = csv.reader(file, delimiter="\\")

    for row in csv_file: 
        muls = re.findall('(mul\([0-9]{1,3},[0-9]{1,3}\))', row[0])

        subtotals = []
        for i in muls:
            numbers = re.findall('[0-9]{1,3}', i)
            subtotals.append(int(numbers[0])*int(numbers[1]))
        
        totals.append(sum(subtotals))

total = sum(totals)
print(total)