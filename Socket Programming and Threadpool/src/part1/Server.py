
#!/usr/bin/env python3
import socket
import queue
import threading
import re

Lookuptable ={"FishCo": [10.00,50],
              "GameStart" :[20.00,100]        
                  }

threadList=[]
QueueLock = threading.Lock()
Connection_lock=threading.Lock()
suspendFlag =False

#function for checking stockname in the lookup table and return values
def lookup(stock_name):
    if stock_name in Lookuptable.keys():
        #if stock is suspended then return 0 else return stcokprice
        if suspendFlag:
            return 0
        return Lookuptable[stock_name][0]
    else:
        return -1


#manage each requests using a thread from threadpool                
def process_connections(conn_q):
    while True:         
        try:
            request,conn =conn_q.get()
            print("request is",request )
            request=re.match('Lookup\((.*)\)',request).group(1)
            print("Thread : ",str(threading.current_thread().name))
            data=process_requests(request)
            print(data)
            conn.sendall(bytes(data,'utf-8'))            
        finally:               
            conn.close()
            conn_q.task_done()

#processing the request to get the resposne from lookup          
def process_requests(req):            
        print("value of request is ",req)       
        print("processing %s" % ( req))
        return_price = str(lookup(req))
        #print(return_price)
        return return_price


#Create an empty queue to hold all incoming connections 
connection_req_queue = queue.Queue()


#Initialize socket connection by binding port num to address
s = socket.socket()
host = socket.gethostname()     # Get local machine name
port = 65045                    # Reserve a port for your service
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection

#Create a threadpool with fixed N number of threads maintain it in a list
ThreadNumbers=3
for i in range(ThreadNumbers):
    thread=threading.Thread(target=process_connections,args=[connection_req_queue])
    thread.start()
    threadList.append(thread)


while True:

    #Accpet the incoming client and put it to the queue so that threadpool can handle the requests
    c, addr = s.accept()     # Establish connection with client
    print('Connected to: ' + addr[0] + ':' + str(addr[1]))
    request = c.recv(2048).decode('utf-8')
    #pushing the request and client to queue
    connection_req_queue.put((request,c))


