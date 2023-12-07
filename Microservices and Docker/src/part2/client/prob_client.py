import socket
import json
import time
import random

# send some data 
s = socket.socket()
 
host='10.0.0.35'                            # Get local machine name
port = 12345                                # Specify the port to connect to
s.connect((host, port))
                                            #Send http req and get back json data
prob=0.5                                      #assigning a probability to compare  
start=time.perf_counter()



#sending a random GET request and only do the post if the returned quantity is greater than zero, with probability 
# it will send another order request using the same connection.

for i in range(10):
    stock_name=random.choice(['GameStart','FishCo','MenhirCo','BoarCo']) #take a random stock name to send lookup request to frontend    
    http_request = "GET /stocks/%s / HTTP/1.1\r\nHost:%s\r\n\r\n" %(stock_name,host)
    print(http_request)
    s.send(http_request.encode())           #Sending lookup request
    response = s.recv(1024)
    
    header_end = response.find(b'\r\n\r\n') # Find the end of the HTTP response header

    # Extract the HTTP response header and body
    header = response[:header_end].decode()
    body = response[header_end+4:]

    # Print the HTTP response header and body

    response_data = json.loads(body.decode('utf-8'))
    if response_data['data']['quantity']>0:             #check if the quantity is >0 
        assign_prob=random.uniform(0,1)                 #assigning a random proabability between 0 and 1
        print("assign prob",assign_prob)
        if assign_prob>prob:                            #only enter the loop if the assign prob>prob defined in client else continue
            quantity=random.choice([5,13,4,3,1000,2000])
            trade_type=random.choice(['buy','sell'])    #choose random buy or sell to post 
            request_body=json.dumps({ 
                "name": stock_name,
                "quantity": quantity,
                "type": trade_type
            })
            print(request_body)
            http_request = f"POST /orders HTTP/1.1\r\nHost: {host}:{port}\r\nContent-Type: application/json\r\nContent-Length: {len(request_body)}\r\n\r\n{request_body}"
            print(http_request)
            s.send(http_request.encode())               #send the request to  server
            response = s.recv(1024)
            # Find the end of the HTTP response header
            header_end = response.find(b'\r\n\r\n')

            # Extract the HTTP response header and body
            header = response[:header_end].decode()
            body = response[header_end+4:]

            # Print the HTTP response header and body
            #print(header)
            print("response from frontend server is",body)
            print("##################### transaction completed ##################")
        else:
            print("exiting since the assign prob is less than prob ")
            continue
end=time.perf_counter()
print("Time taken for 1000 requests: ",end-start)   # to analyse the time taken for 1000 requests
