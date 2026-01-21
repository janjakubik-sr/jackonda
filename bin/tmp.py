#!/usr/bin/env python3
import re
i = 80
with open('P_RMSF.dat') as ID:
    for line in ID:
        pattern = '_'+str(i)
        if re.search(pattern, line):
            res_id = (line.strip().split())[2]
            print(res_id)
