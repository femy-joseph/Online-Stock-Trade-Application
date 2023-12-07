#!/bin/bash

# Build Catalog Service image
docker build -f catalog.Dockerfile -t catalog .

#Build frontend Service image
docker build -f frontend.Dockerfile -t frontend .

#Build Orders Service image
docker build -f orders.Dockerfile -t orders .

