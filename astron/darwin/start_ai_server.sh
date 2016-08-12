#!/bin/sh
cd ../..

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

echo "=============================="
echo "Starting Pirates Online AI server..."
echo "=============================="

while [ true ]
do
ppython -m pirates.ai.ServiceStart
done
