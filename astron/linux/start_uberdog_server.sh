#!/bin/sh
cd ../..

echo "=============================="
echo "Starting Pirates Online UberDOG server..."
echo "=============================="

while [ true ]
do
/usr/bin/python2 -m pirates.uberdog.ServiceStart
done