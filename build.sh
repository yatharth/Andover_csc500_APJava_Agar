#!/usr/bin/env bash

echo "Moving existing build out of the way"
if [ -d "dist.platforms.old" ]; then
 	rm -r dist.platforms dist.platforms.old
fi 
if [ -d "dist.platforms" ]; then
 	mv dist.platforms dist.platforms.old
fi 

echo "Creating temporary files"
touch src/tmp.pyde
echo "import launcher" >> src/tmp.pyde
echo "launcher.create()" >> src/tmp.pyde
cat src/agar.pyde >> src/tmp.pyde 

echo "Exporting"
sh libraries/processing.py-0202-macosx/processing-py.sh src/tmp.pyde

echo "Moving and copying over files"
mv src/dist.platforms .
cp src/*.py dist.platforms/mac/Launcher.app/Contents/Runtime/
cp src/*.py dist.platforms/win/runtime/

echo "Cleaning up"
rm src/tmp.pyde

echo "Done"
