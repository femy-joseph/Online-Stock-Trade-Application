# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC stockbazaar.StockHandle server."""

from concurrent import futures
import logging
import threading
import grpc
import stockbazaar_pb2
import stockbazaar_pb2_grpc
LookupLock = threading.Lock()

#Dictionary having all stocks details where key being the stockname and value is a list having 
#price as 1st element, volume as 2nd element and max trade allowed as 3rd element
Lookuptable ={"FishCo": [10.00,50,5],
              "GameStart" :[20.00,100,7],
              "BoarCo" : [30.00,25,10],
              "MenhirCo": [90.00,20,5]      
                  }

class StockHandle(stockbazaar_pb2_grpc.StockHandleServicer):

    #Function to process the lookup request from clients which send back price and volume of the requested stock if available
    def Lookup(self, request, context):
         with LookupLock:
            stock_name=request.name
            if stock_name in Lookuptable.keys():
                return stockbazaar_pb2.lookupReply(price=Lookuptable[stock_name][0],volume=Lookuptable[stock_name][1])
            else:
                return stockbazaar_pb2.lookupReply(price=-1,volume=-1)

    #Method to buy or sell any stock which updates the dictionary as well based on requests
    def Trade(self, request, context):
        with LookupLock:
            stock_name=request.name
            num_of_stocks=request.add_remove
            while(stock_name in Lookuptable.keys()):
                max_trade_possible=Lookuptable[stock_name][2]
                if num_of_stocks<=max_trade_possible:
                    if request.type=='buy':
                        Lookuptable[stock_name][1]-=num_of_stocks
                        print(Lookuptable)
                        return stockbazaar_pb2.TradeReply(message=1)
                    elif request.type=='sell':
                        Lookuptable[stock_name][1]+=num_of_stocks
                        print(Lookuptable)
                        return stockbazaar_pb2.TradeReply(message=1)
                else:
                    return stockbazaar_pb2.TradeReply(message=0)
            return stockbazaar_pb2.TradeReply(message=-1)
    
    #Method to update the stock prices periodically
    def Update(self, request, context):
        with LookupLock:
            stock_name=request.name
            newprice=float(request.price)
            while(stock_name in Lookuptable.keys()):
                if newprice<=0:
                    return stockbazaar_pb2.UpdateReply(message=-2)
                else:
                    Lookuptable[stock_name][0]=newprice
                    print("Stock details after updating new stock price: ",Lookuptable)
                    return stockbazaar_pb2.UpdateReply(message=1)
            return stockbazaar_pb2.UpdateReply(message=-1)  
    
def serve():
    #Creating a threadpool with maximum of 10 workers to handle all incoming requests from multiple clients 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stockbazaar_pb2_grpc.add_StockHandleServicer_to_server(StockHandle(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()