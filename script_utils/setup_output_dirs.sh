#!/bin/bash

#
# Make output Directories
#

for D in _logs _chk _molden _energies
do
if [ -d $D ] 
then
    echo "Directory $D exists." 
else
    echo "Directory $D does not exist, making directory..."
    mkdir $D
fi
done