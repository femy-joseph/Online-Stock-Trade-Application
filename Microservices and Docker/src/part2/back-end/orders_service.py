from http.server import BaseHTTPRequestHandler
from http.client import HTTPConnection
import socketserver,json,pickle,os,csv
from Read_Write_Lock import ReadWriteLock 


PORT = 8080                                             # Set the port number for the server
rwlock=ReadWriteLock()                                  #call the readwritelock imported from Read_Write_Lock.py

#####fucntion to fetch the last transaction number inorder to update the recent transaction             
def trade_stocks(post_data):
    if os.path.exists("orders_DB.csv"):     
        rwlock.acquire_read()
        with open("orders_DB.csv") as f:
            reader = csv.reader(f)
            rows=0
            for row in reader:
                rows+=1                     #get the last row in the csv to get the transaction_number
            if rows==1:
                transaction_number=0        #set transaction_number=0 if no rows in log
            else:
                transaction_number=int(row[0])      #set the transaction_number as the 
        rwlock.release_read()


    ####### Handle the post data here add or subtract the trade volume ########
    if post_data['name']:
        req_endpoint='/Lookup_csv/'+post_data['name']
        conn = HTTPConnection('catalog_service', 8001)      #connect to the catalog service for lookup
        conn.request('GET',req_endpoint)
        response = conn.getresponse()
        response_data = response.read()
        response_data=pickle.loads(response_data)
        if response_data=='stock not found':                #handle the error 
            response_code=404
            response_data='stock not found'
        else:               #if the stock is available from lookup in catlog server
            stock_name=response_data['name']                
            present_quantity=response_data['quantity']
            max_trade_possible=response_data['max_trade']
            if post_data['name'] == stock_name :           # if the quantity is matching with 
                num_of_stocks=post_data['quantity']        #the response received from catalog proceed with buy /sell
                if (post_data['type']=='buy' or post_data['type']=='sell') and (num_of_stocks>max_trade_possible or  num_of_stocks>present_quantity): 
                    response_data= "max trading volume exceeded"   # if num_of_stocks > max_trade_possible throw error
                    response_code=422
                                        
                elif post_data['type']=='buy' and num_of_stocks<=max_trade_possible and num_of_stocks<=present_quantity:  # if num_of_stocks > available quantity for the stock, throw error        
                    response_data['quantity']=response_data['quantity'] - post_data['quantity']      #reduce the quantity of the stock after buying                      
                    req_endpoint='/buy/'+post_data['name']                        
                    headers={'Content-Type': ' application/json'}
                    post_data_to_catalog=json.dumps(response_data) #
                    conn2 = HTTPConnection('catalog_service', 8001)     #
                    conn2.request('POST',req_endpoint,post_data_to_catalog,headers) #connect to catalog server for updating the modified data
                    response=conn2.getresponse()
                    response_data = response.read()                     #response for buying trade from catalog
                    response_data=pickle.loads(response_data)
                    response_data['transaction_number']=transaction_number+1   #increase the transaction number after buying 
                    del response_data['success']
                    add_row=[transaction_number+1,post_data['name'],post_data['type'],post_data['quantity']]
                    rwlock.acquire_write()
                    with open("orders_DB.csv", 'a', newline= '') as file:  # Write the updated contents to the new file
                        writer = csv.writer(file)
                        writer.writerow(add_row)
                    rwlock.release_write()
                    response_code=200
                                                                                        
                elif post_data['type']=='sell' and num_of_stocks<=max_trade_possible and num_of_stocks<=present_quantity:
                    response_data['quantity']=response_data['quantity'] + post_data['quantity']  #increase the quantity of the stock after selling  
                    print("updated data to catalog :",response_data)
                    req_endpoint='/sell/'+post_data['name']
                    headers={'Content-Type': ' application/json'}
                    post_data_to_catalog=json.dumps(response_data)
                    conn2 = HTTPConnection('catalog_service', 8001)                     #connect to catalog server for updating the modified data
                    conn2.request('POST',req_endpoint,post_data_to_catalog,headers)
                    response=conn2.getresponse()
                    response_data = response.read()
                    response_data=pickle.loads(response_data)                 #response for selling trade from catalog
                    print("response for selling trade from catalog ",response_data)
                    response_data['transaction_number']=transaction_number+1   #increase the transaction number after buying
                    del response_data['success']
                    add_row=[transaction_number+1,post_data['name'],post_data['type'],post_data['quantity']]
                    rwlock.acquire_write()
                    with open("orders_DB.csv", 'a', newline= '') as file:           # Write the updated contents to the new file                    
                        writer = csv.writer(file)
                        writer.writerow(add_row)

                    rwlock.release_write()                                          #release the readwrite lock
                    response_code=200
    return response_data,response_code

# Define the handler to process incoming POST requests
class MyHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):                                                      #fucntion to handle the post requests
        end_point=self.path
        if 'trade_stocks' in end_point:                                      #checking for the end point to accept the request
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            post_data=json.loads(post_data)
            response_data,response_code=trade_stocks(post_data)               #invoking the trade_stocks fucntion to modify 
            self.send_response(response_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(pickle.dumps(response_data))  


###### Set up the server to listen on the specified port ########
with socketserver.TCPServer(("orders_service", PORT), MyHandler) as httpd:
    print("Order server running on port", PORT)
    # Start the server to handle incoming requests
    httpd.serve_forever()
    
