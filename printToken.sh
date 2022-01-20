#!/bin/bash

cd ..
cat token.txt
cd IoTdevices
git add .
git commit -m 'auto commit'
git push
