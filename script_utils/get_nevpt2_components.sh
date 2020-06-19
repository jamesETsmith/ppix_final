#!/bin/bash

#
# Usage get_nevpt2_components.sh _logs/_pt_0.out
#

FILE=$1

printf "Parsing ${FILE} ...\n"

grep "Sr    (-1)"    $FILE
grep "Si    (+1)"    $FILE
grep "Sijrs (0)  ,"  $FILE
grep "Sijr  (+1)"    $FILE
grep "Srsi  (-1)"    $FILE
grep "Srs   (-2)"    $FILE
grep "Sij   (+2)"    $FILE
grep "Sir   (0)"     $FILE
