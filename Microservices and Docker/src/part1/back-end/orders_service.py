from http.server import BaseHTTPRequestHandler
from http.client import HTTPConnection
import socketserver,json,pickle,os,csv
from Read_Write_Lock import ReadWriteLock 

# Set the port number for the order server
PORT = 8080
#Create an instance to readwritelock
rwlock=ReadWriteLock()

#Takes the http requests and sends back the transaction number is buy/sell ws success, else send error
def trade_stocks(post_data):
    #To fetch the last transaction number inorder to update the recent transaction, lock is acquired before accessing the file
    if os.path.exists("src/part1/back-end/orders_DB.csv"):
        rwlock.acquire_read()
        with open("src/part1/back-end/orders_DB.csv") as f:
            reader = csv.reader(f)
            rows=0
            for row in reader:
                rows+=1
            if rows==1:
                transaction_number=0
            else:
                transaction_number=int(row[0])
        rwlock.release_read()

    # Handle the post data here add or subtract the trade volume
    if post_data['name']:
        req_endpoint='/Lookup_csv/'+post_data['name']
        conn = HTTPConnection('localhost', 8001)  #Connect to catalog to get stock details
        conn.request('GET',req_endpoint)
        response = conn.getresponse()
        response_data = response.read()
        response_data=pickle.loads(response_data)
        if response_data=='stock not found':  #If the catalog does not have the requested stock send stock not found with 404 code
            response_code=404
            response_data='stock not found'
        else:
            stock_name=response_data['name'] #if the stock is available from lookup in catlog server check for the maximum trading limit condition
            present_quantity=response_data['quantity']
            max_trade_possible=response_data['max_trade']
            if post_data['name'] == stock_name :
                num_of_stocks=post_data['quantity']
                if (post_data['type']=='buy' or post_data['type']=='sell') and (num_of_stocks>max_trade_possible or  num_of_stocks>present_quantity): 
                    response_data= "max trading volume exceeded" # if num_of_stocks > max_trade_possible throw error
                    response_code=422
                                        
                elif post_data['type']=='buy' and num_of_stocks<=max_trade_possible and num_of_stocks<=present_quantity:                   
                    response_data['quantity']=response_data['quantity'] - post_data['quantity']  #reduce the quantity of the stock after buying
                    req_endpoint='/Update_csv/'+post_data['name']                        
                    headers={'Content-Type': ' application/json'}
                    post_data_to_catalog=json.dumps(response_data)
                    conn2 = HTTPConnection('localhost', 8001)  #connect to catalog server for updating the modified data
                    conn2.request('POST',req_endpoint,post_data_to_catalog,headers)
                    response=conn2.getresponse() #response for buying trade from catalog
                    response_data = response.read()
                    response_data=pickle.loads(response_data)
                    response_data['transaction_number']=transaction_number+1 #increase the transaction number after buying 
                    del response_data['success']
                    add_row=[transaction_number+1,post_data['name'],post_data['type'],post_data['quantity']]
                    rwlock.acquire_write()
                    with open("src/part1/back-end/orders_DB.csv", 'a', newline= '') as file: # Write the updated contents to the new file
                    # Write the updated contents to the new file
                        writer = csv.writer(file)
                        writer.writerow(add_row)
                    rwlock.release_write()
                    response_code=200
                                                
                elif post_data['type']=='sell' and num_of_stocks<=max_trade_possible and num_of_stocks<=present_quantity:
                    response_data['quantity']=response_data['quantity'] + post_data['quantity'] #increase the quantity of the stock after selling
                    req_endpoint='/Update_csv/'+post_data['name']
                    headers={'Content-Type': ' application/json'}
                    post_data_to_catalog=json.dumps(response_data)
                    conn2 = HTTPConnection('localhost', 8001)   #connect to catalog server for updating the modified data
                    conn2.request('POST',req_endpoint,post_data_to_catalog,headers)
                    response=conn2.getresponse()    #response for selling trade from catalog
                    response_data = response.read()
                    response_data=pickle.loads(response_data)
                    response_data['transaction_number']=transaction_number+1  #increase the transaction number after buying
                    del response_data['success']
                    add_row=[transaction_number+1,post_data['name'],post_data['type'],post_data['quantity']]
                    rwlock.acquire_write()
                    with open("src/part1/back-end/orders_DB.csv", 'a', newline= '') as file:  # Write the updated contents to the new file 
                    # Write the updated contents to the new file
                        writer = csv.writer(file)
                        writer.writerow(add_row)
                    rwlock.release_write()  #release lock
                    response_code=200
                    #self.send_response(200)
    return response_data,response_code

# Define the handler to process incoming requests
class MyHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        end_point=self.path
        if 'trade_stocks' in end_point:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            post_data=json.loads(post_data)
            response_data,response_code=trade_stocks(post_data)
            self.send_response(response_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(pickle.dumps(response_data))  


# Set up the server to listen on the specified port
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Order server running on port", PORT)
    # Start the server to handle incoming requests
    httpd.serve_forever()
    
