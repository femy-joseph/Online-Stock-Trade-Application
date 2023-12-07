# Part 1 #

## catalog service 
Service to lookup the stocks_DB.csv for stock name and return the response. Also handle the lookup and update requests from the Order service to modify the stock_DB.csv

Run the catalog service   :python3 back-end/catalog_service.py
 
## Frontend Service

The clients can communicate with the front-end service using the below 2 HTTP-based REST APIs. It will forward the requests based on lookup or trade to catalog or order server.
1.GET /stocks/<stock_name>
2.POST /orders

Run the server  :python3 front-end/server.py
## order service

Run the orders service : python3 back-end/orders_service.py

## Client
Once all servers are up and running ,execute the client :
client_prob.py : client code for randomly sending GET and POST requests to the frontend after randomly looking up from the catalog and based on the quantity, if quantity>0 , assigning a probability and it will send another trade POST request to the frontend.

1. Run the client application on your machine : python3 prob_client.py

# Part 2 #

# runninng the shell script to create the images of dockerfiles #

1. make the 'build.sh' file executable with chmod +x build.sh
2. run the script using ./build.sh in the same folder as the dockerfiles located.(in part2)

# docker-compose.yml file to bring up and down the services #

1. We can bring up (or tear down) all three microservices using 'docker-compose up'
2. stop the services using 'docker compose down'
# client 

Once all servers are up and running ,execute the client.
1. Run the client application on your machine : python3 prob_client.py


Work Division:

Priyanka V devoor :
1. Part 1 : Frontend service,Catalog service, Client applciation
2. Part 3 : Design Document part 1
3. Part 3 : Test cases and Test case outputs.

Femimol Joseph:
1. Part 2 - Docker images and Docker compose files
2. Part 1 - Order Service
3. Part 3 - Evaluation Document and Design Document part 2






