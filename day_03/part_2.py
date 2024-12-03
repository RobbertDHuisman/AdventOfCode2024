import re
import csv

totals = []
enabled = 1

with open("input.csv", 'r') as file:
    csv_file = csv.reader(file, delimiter="\\")

    for row in csv_file: 
        muls = re.findall('(mul\([0-9]{1,3},[0-9]{1,3}\))|(do\(\))|(don\'t\(\))', row[0])

        subtotals = []
        for i in muls:
            numbers = re.findall('[0-9]{1,3}', i[0])
            do = re.findall('(do\(\))', i[1])
            dont = re.findall('(don\'t\(\))', i[2])
            if do != []:
                enabled = 1
            elif dont != []:
                enabled = 0
            else:
                if enabled == 1:
                    subtotals.append(int(numbers[0])*int(numbers[1]))
        
        totals.append(sum(subtotals))

total = sum(totals)
print(total)