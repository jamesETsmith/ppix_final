#!/bin/bash

printf "\nChecking Neutral:\n"
grep -A 3 "148  <i|F|i>" neutral/_logs/_sa_mcscf.out

printf "\nChecking Anion:\n"
grep -A 3 "148  <i|F|i>" anion/_logs/_sa_mcscf.out

printf "\nChecking Dinion:\n"
grep -A 3 "148  <i|F|i>" dianion/_logs/_sa_mcscf.out

printf "\nChecking Anion pt. charge 1:\n"
grep -A 3 "118  <i|F|i>" anion_pt_chg_1/_logs/_sa_mcscf.out

printf "\nChecking Anion pt. charge 2:\n"
grep -A 3 "118  <i|F|i>" anion_pt_chg_2/_logs/_sa_mcscf.out

printf "\nChecking Anion pt. charge 3:\n"
grep -A 3 "118  <i|F|i>" anion_pt_chg_3/_logs/_sa_mcscf.out

printf "\nChecking Dinion pt. charge:\n"
grep -A 3 "118  <i|F|i>" dianion_pt_chg/_logs/_sa_mcscf.out