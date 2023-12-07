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

import logging
import grpc
import stockbazaar_pb2
import stockbazaar_pb2_grpc
import time
import random

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('elnux3.cs.umass.edu:50051') as channel:
        stub = stockbazaar_pb2_grpc.StockHandleStub(channel)

        #Loop to send to update new stock prices to the server, including negative usecases
        for i in range(100):
            stock=random.choice(['FishCo','GameStart','BoarCo','MenhirCo'])
            amt=random.choice([10,-1,0,20,30,50])
            print("Sending update price request for stock {0} to {1}".format(stock,amt))
            response1 = stub.Update(stockbazaar_pb2.UpdateRequest(name=stock,price=amt))
            print("Update of price was: {0}".format(response1.message))
            time.sleep(3)
        
if __name__ == '__main__':
    logging.basicConfig()
    run()