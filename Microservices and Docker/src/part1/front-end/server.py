import json
import socket
from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPConnection
import pickle


class Http_req_Handler:
    def __init__(self,conn):
        self.conn = conn

    #Decode whether http req is to GET or POST and call respective methods
    def decode_request(self):
        while True:
            http_req=self.conn.recv(1024).decode() # receive the request from client
            if "GET" in http_req:                  # checking whether Its a GET or POST request
                stocks = http_req.split()[1]
                stock_name=stocks.split("/")[2]
                self.do_GET(stock_name)            #extract the stockname 

            elif "POST" in http_req:
                http_req=http_req.split("\r\n")
                content_type=http_req[2]
                body=json.loads(http_req[5]) 
                self.do_POST(content_type,body)    #call the do_POST function post the request to the orders service 

        self.conn.close() 
    
    #Perform GET of requested stock function to process the GET request

    def do_GET(self,stock_name):
        connect = HTTPConnection('localhost', 8001)  #Connect to the catalog server 
        req_endpoint='/Lookup_csv/'+stock_name         #Request endpoint /Lookup_csv
        connect.request('GET', req_endpoint)
        response = connect.getresponse()
        response_data = response.read()
        data_dict=pickle.loads(response_data)
        if type(data_dict) == dict:
            if 'max_trade' in data_dict.keys():    #remove the max_trade entity from the catalog's response 
                del data_dict['max_trade']
        self._build_http_response(response.status,response.reason,data_dict)
        self.conn.send(self.response)              # send the resposne back to client

    #Do POST of requested orders
    # function to process the POST request
    def do_POST(self,content_type,body):
        contenttype=content_type.split(':')
        content={}
        content[contenttype[0]]=contenttype[1]                      # convert it into a dictionary to post
        body=json.dumps(body)
        connect2 = HTTPConnection('localhost', 8080)                # connect to order service
        req_endpoint='/trade_stocks'
        connect2.request('POST',req_endpoint,body,content)          #Connect to the catalog server 
        response = connect2.getresponse()
        response_data = response.read()
        data=pickle.loads(response_data)
        self._build_http_response(response.status,response.reason,data)
        self.conn.send(self.response)                       #send the response back to client


    def _build_http_response(self,code,status,stock_data):
        # Create an HTTP response header
        self.response_header = "HTTP/1.1 %s %s\r\n" % (str(code),status)
        self.response_header += "Content-Type: application/json\r\n"
        self.response_header += "Connection: close\r\n"

        # Create the body of the response
        result=dict()
        res_msg=dict()
        if code==200:
            result['data']=stock_data
        else:
            res_msg['code']=code
            res_msg['message']=stock_data
            result['error']=res_msg
        print("before sending the result to client",result)
        json_data = json.dumps(result)
        self.response_body = json_data.encode('utf-8')      # response body to send to the client

        # Add the Content-Length header to the response header
        self.response_header += "Content-Length: " + str(len(self.response_body)) + "\r\n"

        # Add a blank line to indicate the end of the header
        self.response_header += "\r\n"

        # Send the response header and body
        self.response = self.response_header.encode('utf-8') + self.response_body


#Method to handle each client as per thread per session model
def handle_client(conn):
    req_obj=Http_req_Handler(conn)
    req_obj.decode_request()


PORT=12345
IP='localhost'
s=socket.socket()
s.bind((IP,PORT))
s.listen(5)
# create a threadpool of workers 7
executor = ThreadPoolExecutor(max_workers=7)
while True:
    c,addr=s.accept()
    print("Connection from {0} has been established.".format(addr))
    executor.submit(handle_client,c)              #calling the fcuntion handle_client to handle the request

