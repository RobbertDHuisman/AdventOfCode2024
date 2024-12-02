import pandas as pd
import re

def try_reports(numbers):
    safe = 1
    for j in range(1, len(numbers)):
        if safe == 1:
            previous = int(numbers[j-1])
            current = int(numbers[j])
            dif = current - previous
            print(f"nummers zijn {numbers[j]} en {numbers[j-1]} safe = {safe} and dif = {dif} ")
            if abs(dif) > 3:
                safe = 0
                print("te groot verschil")

            if dif == 0:
                safe = 0
                print("blijft gelijk")    

            if j > 1:
                one_more_back = int(numbers[j-2])
                if not (current > previous & previous > one_more_back) | (current < previous & previous < one_more_back):
                    safe = 0
                    print("verkeerde kant")
      
    return safe

def main():
    df = pd.read_csv("input.csv", names=["a"], engine="python")
    safe_reports = 0

    for i in df["a"]:
        numbers = re.findall(pattern="([0-9]{1,10})", string=i)
        print(numbers)
        safe = try_reports(numbers)

        safe_reports = safe_reports + safe

    print(safe_reports)

main()