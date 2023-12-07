import socket
import random,time





#list of stocknames 
stocks = ['FishCo','GameStart','BirdCo','BuffCo','DogStart']

start=time.perf_counter()
print("starting time",start )

for i in range(100):

    s = socket.socket()
    host = socket.gethostname()     # Get local machine name
    #host = 'elnux3.cs.umass.edu'
    port = 65045                    # Specify the port to connect to
    s.connect((host, port))
    stock_name=random.choice(stocks)
    stock="Lookup({})".format(stock_name) #sending requests in the format of 'Lookup(stock_name)'
    print(stock)
    msg=bytes(stock,'utf-8')
    s.send(msg)
    print("Request has been sent: ",i+1)    
    print("RESPONSE FROM server: for ",stock,"-" + str(s.recv(5000)))   
    s.close()                       # Close the socket when done
   
end=time.perf_counter() -start
print("time taken for client : ",end)