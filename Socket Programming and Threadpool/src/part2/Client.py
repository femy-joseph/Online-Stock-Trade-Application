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
"""The Python implementation of the GRPC stockbazaar.StockHandle client."""

from __future__ import print_function
import time
import logging
import random
import grpc
import stockbazaar_pb2
import stockbazaar_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('elnux3.cs.umass.edu:50051') as channel:
        stub = stockbazaar_pb2_grpc.StockHandleStub(channel)

        #Pre-configured lists to send requests to server randomly choosing from these lists
        stocks_list=['FishCo','GameStart','BoarCo','MenhirCo','Dogstart','CatCo']
        trading_type=['buy','sell']
        trade_vol=[2,3,5,7,10,12,15]

        
        #Loop to send and receive  multiple lookup and trading requests to the server by randomly selecting stock name, 
        #volume and trading type from above lists
        for i in range(1000):
            stock=random.choice(stocks_list)
            vol=random.choice(trade_vol)
            tr_type=random.choice(trading_type)
            print("Sending Lookup request for stock {0}".format(stock))
            response = stub.Lookup(stockbazaar_pb2.LookupRequest(name=stock))
            print("Lookup response from server: Price: {0}   Volume: {1}".format(str(response.price),str(response.volume)))
            print("\n")
            print("Sending {0} request for stock {1} of volume {2}".format(tr_type,stock,vol))
            response2 = stub.Trade(stockbazaar_pb2.TradeRequest(name=stock,add_remove=vol,type=tr_type))
            print("Trading reply from server: {0}".format(response2.message))
            print("\n")

if __name__ == '__main__':
    logging.basicConfig()
    run()