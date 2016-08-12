#!/bin/sh
cd ../..

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

echo "=============================="
echo "Starting Pirates Online UberDOG server..."
echo "=============================="

while [ true ]
do
ppython -m pirates.uberdog.ServiceStart
done
