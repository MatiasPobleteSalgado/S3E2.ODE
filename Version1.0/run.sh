#!/bin/bash

make
python3 main.py "$1"
./exec  "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8"
python3 result.py
