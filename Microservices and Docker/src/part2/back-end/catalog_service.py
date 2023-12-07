from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection
import pickle,json,csv
import os
import socketserver
from urllib import response
from Read_Write_Lock import ReadWriteLock 

# Set the port number for the catalog server
PORT = 8001

rwlock=ReadWriteLock()

##### Method to lookup data for requested stock name, if not found returns stock not found 
def Lookup_csv(stock_name):
    if os.path.exists("stocks_DB.csv"):
        rwlock.acquire_read()                   #acquire the readwrite lock
        with open("stocks_DB.csv") as f:
            reader = csv.reader(f)
            for row in reader :                 # iterating row by row and checking for                                                
                if stock_name in row:            # stock_name in the row and updating the row 
                    print(row)
                    keys = ['name', 'price', 'quantity', 'max_trade']
                    result = dict(zip(keys, row))
                    result['price'] = float(result['price'])
                    result['quantity'] = int(result['quantity'])
                    result['max_trade']=int(result['max_trade'])
                    rwlock.release_read()
                    return result
            rwlock.release_read()               #release the readwrite lock
            return 'stock not found'            #if stockname not in csv return error

####### function to update the csv after getting modified data from Orders service ######

def Update_csv(stock_name,quantity):    
    if os.path.exists("stocks_DB.csv"): # if stocks_DB.csv exists open
        with open("stocks_DB.csv") as f:
            rwlock.acquire_write()
            reader = csv.reader(f)
            rows=[]
            for row in reader :         # iterating row by row and checking for                                       
                if stock_name in row:   # stock_name in the row and updating the row 
                    print(row)
                    row[2]=quantity
                    print("after updating row ",row)
                rows.append(row)
                print(rows)
        with open("stocks_DB.csv", 'w', newline='') as file:            
            writer = csv.writer(file)               # Write the updated contents to the new file
            writer.writerows(rows)
        rwlock.release_write()
           
##### Define the handler to process incoming GET requests######

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
        content_length = int(self.headers['Content-Length'])        
        post_data = self.rfile.read(content_length)             #read the contents from the post request
        post_data=json.loads(post_data)
        print("post_data is ",post_data)
        if post_data is None or post_data == {}:            #handle the exception if the data is empty
            response=json.dumps({"Error": "Please provide correct type to buy or sell"}), 400, 'application/json'
            self.wfile.write(response)                      
        stock_name=post_data['name']
        quantity=post_data['quantity']
        Update_csv(stock_name,quantity)                     #call the updateCSV function to put the modified data
        self.send_response(200)
        self.send_header('Content-type', 'application/json')        
        self.end_headers()                                  # Send the headers to the client before sending the response body
        data={'success':'data updated successfully'}

        self.wfile.write(pickle.dumps(data))



# Set up the server to listen on the specified port
with socketserver.TCPServer(("catalog_service", PORT), MyHandler) as httpd:
    print("Catalog server running on port", PORT)
    httpd.serve_forever()                                   # Start the server to handle incoming requests