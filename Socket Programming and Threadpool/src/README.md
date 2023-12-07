Lab 1:

Part _ 1: Asterix and the Stock Bazaar

1. Run the Server.py on your edlab machine 
2. Run the Client.py on your machine and modify the port as same as the Server.py
    
     In Client.py 
        1. Replace the "socket.gethostname()" to 'elnux3.cs.umass.edu' or the hostname of the machine you are planning to execute the Server.py.
  

Part2 : Implementation with gRPC and Built in Thread Pool

1. Run the Server.py on your edlab machine 
2. In Client.py file change the localhost in the "grpc.insecure_channel('localhost:50051')" with your machine hostname and 
   port using which you are execuitng the Server.py file.
3. Run the Client.py for invoking Lookup or Trade requests sequentially to the lookup table.
4. Run the Client_Update.py for invoking update requests to the lookup table.



for installing grpc tools and create teh protobuff please follow the steps in :  https://grpc.io/docs/languages/python/quickstart/

Install gRPC:
    1.python -m pip install grpcio

To install gRPC tools, run:

$ python -m pip install grpcio-tools

To create gRPC code :

$ python -m grpc_tools.protoc -I proto --python_out=. --pyi_out=. --grpc_python_out=. proto/stockbazaar.proto


