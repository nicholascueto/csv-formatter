import os, sys, csv
import lookupTables as lut
from fuzzywuzzy import fuzz

def searchAndReplace(line, table, oneLine=True, lineIndex=3, matchTolerance=85):
    '''
    Input list from csv and search through it using all search terms from 'lookupTables.py'.

    line : list or str
        Line from csv converted to list.

    table : dic
        Chosen Lookup Table. Dictionary formatted as Search Term : Replacement List.
            Example: {"sprouts" : ["Sprouts Farmer's Market", "Groceries",,]}

    oneLine : bool
        If True, will process only one item list input. Default for this usecase is 3.

    lineIndex : int
        Index of item in list to prcess.
    '''

    keyValues = table.items()

    for item in line:
        if oneLine:
            item = line[lineIndex]

        for k, v in keyValues:
            # input(k)
            # input(v)
            searchTerm, replacement = k, v
            matchStrength = fuzz.token_set_ratio(searchTerm, item)

            if matchStrength > matchTolerance:
                print(f'Matched {searchTerm} and {item} with a match confidence of {matchStrength}.    Replacing with {replacement}')
                # End search and return replacement
                return replacement

        # break after one search
        if oneLine:
            break
    # If nothing is found, return "None"
    return None


# open file
with open ("Export.csv", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    splitLine = line.split(',')
    # remove last line
    splitLine.pop(-1)
    # print(splitLine)

    # Search through third item in list.
    result = searchAndReplace(splitLine, lut.payees)
    if result:
        splitLine.extend(result)
        # Add updated line to new file
        with open("./FormattedExport.csv", "a") as f:
            write = csv.writer(f)
            write.writerow(splitLine)
        continue

    # If nothing is found, add the current line and format it
    else:
        extraLines = ['','','',]
        splitLine.extend(extraLines)


    # if i == 30:
    #     break


