#!/bin/sh
cd ../..

echo "=============================="
echo "Starting Pirates Online AI server..."
echo "=============================="

while [ true ]
do
/usr/bin/python2 -m pirates.ai.ServiceStart
done