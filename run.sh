#!/bin/bash

#$1 : denotes weight

#./main.py -w $1  -a http.raw 
./main.py -w $1 -d -t ./token.txt http16.dat 
