#!/usr/bin/env bash

echo "Moving existing build out of the way"
if [ -d "dist.platforms.old" ]; then
 	rm -r dist.platforms dist.platforms.old
fi 
if [ -d "dist.platforms" ]; then
 	mv dist.platforms dist.platforms.old
fi 

echo "Creating temporary files"
touch agar/tmp.pyde
echo "import launcher" >> agar/tmp.pyde
echo "launcher.create()" >> agar/tmp.pyde
cat agar/agar.pyde >> agar/tmp.pyde 

echo "Exporting"
sh libraries/processing.py-0202-macosx/processing-py.sh agar/tmp.pyde

echo "Moving and copying over files"
mv agar/dist.platforms .
cp agar/*.py dist.platforms/mac/Launcher.app/Contents/Runtime/
cp agar/*.py dist.platforms/win/runtime/

echo "Cleaning up"
rm agar/tmp.pyde

echo "Done"
