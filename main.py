import os, sys
from fuzzywuzzy import fuzz

with open ("CheckingExport.csv", "r") as f:
    lines = f.readlines()
    for i, x in enumerate(lines):
        splitLine = x.split(',')
        splitLine.pop(-1)
        print(splitLine)
        if i == 2:
            break