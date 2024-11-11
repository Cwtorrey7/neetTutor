#!/bin/bash

echo "\\*** Updating pip ***/"

sudo apt install python3-pip

echo ""
echo "\\*** Updating pytorch ***/"

pip install torch

echo ""
echo "\\*** Updating tiktoken ***/"

pip install tiktoken

echo ""
echo "\\*** Updating protobuf ***/"

pip install protobuf

echo ""
echo "\\*** Creating virtual enviroment ***/"

python3 -m venv .env

echo ""
echo "\\*** Activate the virtual enviroment ***/"

source .env/bin/activate

echo ""
echo "\\*** Updating necessary libraries ***/"

pip install transformers datasets evaluate accelerate
