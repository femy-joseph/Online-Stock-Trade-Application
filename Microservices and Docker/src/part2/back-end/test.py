import os
import csv

#To fetch the last transaction number inorder to update the recent transaction
if os.path.exists("src/part1/back-end/orders_DB.csv"):
        with open("src/part1/back-end/orders_DB.csv") as f:
            reader = csv.reader(f)
            rows=0
            for row in reader:
                rows+=1
            transaction_number=int(row[0])
            if rows==1:
                transaction_number=0
            
            add_row=[transaction_number+1,'FishCo','buy',5]
            with open("src/part1/back-end/orders_DB.csv", 'a', newline= '') as file:
            # Write the updated contents to the new file
                writer = csv.writer(file)
                writer.writerow(add_row)
