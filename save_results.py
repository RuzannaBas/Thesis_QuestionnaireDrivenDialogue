import csv 
import json
from datetime import date
from datetime import datetime
def save_result(results, chatlog):
    total = 0
    for result in results:
        total += result
        print(total)
    results.append(total)
    
    results.insert(0,date.today())
    with open ('results.csv','a',newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter = ' ')
        writer.writerow(results)

    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.txt")

    with open(filename, 'w') as file:
        for item in chatlog:
            file.write(json.dumps(item) + '\n')
    