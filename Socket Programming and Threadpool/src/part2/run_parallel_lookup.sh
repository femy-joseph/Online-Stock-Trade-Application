#!/bin/bash

# Run Python client script three times in parallel
python /workspaces/lab-1-asterix-and-the-stock-bazaar-femimol-and-priyanka/src/Part_2/Client_Lookup.py &
#python /workspaces/lab-1-asterix-and-the-stock-bazaar-femimol-and-priyanka/src/Part_2/Client_Lookup.py &
#python /workspaces/lab-1-asterix-and-the-stock-bazaar-femimol-and-priyanka/src/Part_2/Client_Lookup.py &
#python /workspaces/lab-1-asterix-and-the-stock-bazaar-femimol-and-priyanka/src/Part_2/Client_Lookup.py &
#python /workspaces/lab-1-asterix-and-the-stock-bazaar-femimol-and-priyanka/src/Part_2/Client_Lookup.py &

# Wait for all processes to finish
wait