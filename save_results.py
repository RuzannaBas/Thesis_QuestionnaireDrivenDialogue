import csv 
from datetime import date

def save_result(results):
    total = 0
    for result in results:
        total += result
        print(total)
    results.append(total)
    
    results.insert(0,date.today())
    with open ('results.csv','a',newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter = ' ')
        writer.writerow(results)
