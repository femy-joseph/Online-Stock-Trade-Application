from http.server import BaseHTTPRequestHandler
import pickle,json,csv
import os
import socketserver
from Read_Write_Lock import ReadWriteLock 

# Set the port number for the catalog server
PORT = 8001

rwlock=ReadWriteLock()

# Open the CSV file and read the data into a dictionary to store in-memmory
if os.path.exists("src/part1/back-end/stocks_DB.csv"):
    with open("src/part1/back-end/stocks_DB.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data_dict = {row['name']: {'price': row['price'], 'quantity': row['quantity']} for row in reader}


def Lookup_csv(stock_name):
    if os.path.exists("src/part1/back-end/stocks_DB.csv"):
        rwlock.acquire_read()                    #acquire the readwrite lock
        with open("src/part1/back-end/stocks_DB.csv") as f:
            reader = csv.reader(f)
            for row in reader :                 # iterating row by row and checking for
                if stock_name in row:           # stock_name in the row and updating the row 
                    print(row)
                    keys = ['name', 'price', 'quantity', 'max_trade']
                    result = dict(zip(keys, row))
                    result['price'] = float(result['price'])
                    result['quantity'] = int(result['quantity'])
                    result['max_trade']=int(result['max_trade'])
                    print(result)
                    rwlock.release_read()
                    return result
            rwlock.release_read()           #release the readwrite lock


###### function to update the csv after getting modified data from Orders service ######                 

def Update_csv(stock_name,quantity):
    if os.path.exists("src/part1/back-end/stocks_DB.csv"):   # if stocks_DB.csv exists open
        rwlock.acquire_write()
        with open("src/part1/back-end/stocks_DB.csv") as f:
            reader = csv.reader(f)
            rows=[]
            for row in reader :                 # iterating row by row and checking for  
                if stock_name in row:               # stock_name in the row and updating the row 
                    print(row)
                    row[2]=quantity
                    print("after updating row ",row)
                rows.append(row)
                print(rows)
        with open("src/part1/back-end/stocks_DB.csv", 'w', newline='') as file:
            
            writer = csv.writer(file)       # Write the updated contents to the new file
            writer.writerows(rows)
        rwlock.release_write()
           
# Define the handler to process incoming requests
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        end_point=self.path
        if 'Lookup_csv' in end_point:                   # checking for the end point Look_csv in the GET request                                                           
            stock_name=end_point.split('/Lookup_csv/',1)[1]
        res=Lookup_csv(stock_name)                  #invoke teh lookup function to retrieve the stockdata
        if res=='stock not found':              #handle the exception if not found
            self.send_response(404)             #send response status 404
        else:
            self.send_response(200)             #send response status 200 if success
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(pickle.dumps(res))             # send the data back to 


####### function to handle the post requests from orders service #######
    def do_POST(self):
        end_point=self.path
        if 'Update_csv' in end_point:                        # checking for the end point Update_csv in the POST request  
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data=json.loads(post_data)
            if post_data is None or post_data == {}:        #handle the exception if the data is empty
                response=json.dumps({"Error": "Please provide correct type to buy or sell"}), 400, 'application/json'
                self.wfile.write(response)
            stock_name=post_data['name']
            quantity=post_data['quantity']
            Update_csv(stock_name,quantity)                 #call the updateCSV function to put the modified data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            # Send the headers to the client before sending the response body
            self.end_headers()
            data={'success':'data updated successfully'}

            self.wfile.write(pickle.dumps(data))


        
# Set up the server to listen on the specified port
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Catalog server running on port", PORT)
    # Start the server to handle incoming requests
    httpd.serve_forever()