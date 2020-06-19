#!/bin/bash

#
# Setup output directories and collect node information
#
sh ../script_utils/setup_output_dirs.sh
sh ../script_utils/get_node_info.sh

#
# Run Calculations
#

# Run RKS and SA-MCSCF Calculation
python sa_mcscf.py > _logs/_sa_mcscf.out

# Run PT2 Calculations on all Excited States
python pt2.py 0 > _logs/_pt2_0.out
python pt2.py 1 > _logs/_pt2_1.out
python pt2.py 2 > _logs/_pt2_2.out
#python pt2.py 3 > _logs/_pt2_3.out
#python pt2.py 4 > _logs/_pt2_4.out
#python pt2.py 5 > _logs/_pt2_5.out
#python pt2.py 6 > _logs/_pt2_6.out
#python pt2.py 7 > _logs/_pt2_7.out
#python pt2.py 8 > _logs/_pt2_8.out
#python pt2.py 9 > _logs/_pt2_9.out

