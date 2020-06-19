#!/bin/bash

#
# Get node info
#

INFO_FILE=_logs/node_info.txt
echo "Node Name" > $INFO_FILE
echo "=========" >> $INFO_FILE
hostname >> $INFO_FILE
echo "" >> $INFO_FILE

echo "Processor Info" >> $INFO_FILE
echo "==============" >> $INFO_FILE
lscpu >> $INFO_FILE
echo "" >> $INFO_FILE

echo "Memory Info" >> $INFO_FILE
echo "===========" >> $INFO_FILE
head -n 2 /proc/meminfo >> $INFO_FILE