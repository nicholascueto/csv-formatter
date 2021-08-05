import os, sys, csv, re
import lookupTables as lut
from fuzzywuzzy import fuzz

def searchAndReplace(line, table, oneLine=True, lineIndex=3, matchTolerance=85, useSearchtermAsOutput=True):
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
            # if searchterm has pipe, use alternate method
            if "|" in searchTerm:
                # seperate each term
                spliterms = searchTerm.split('|')
                for term in spliterms:
                    # and search through them
                    matchStrength = fuzz.token_set_ratio(term, item)
                    print(f'Possible match: {term} and {item} with a match confidence of {matchStrength}.    Replacement Candidate = {replacement}') if 80 < matchStrength < matchTolerance else None

                    if matchStrength > matchTolerance:
                        # Use the matched searchterm as the new name
                        replacement[0] = term if useSearchtermAsOutput and "!*norename*!" not in searchTerm else replacement[0]
                        # print(f'Matched {term} and {item} with a match confidence of {matchStrength}.    Replacing with {replacement}') if matchStrength < 99 else None
                        # End search and return replacement
                        return replacement

            else:
                matchStrength = fuzz.token_set_ratio(searchTerm, item)
                print(f'Possible match: {searchTerm} and {item} with a match confidence of {matchStrength}.    Replacement Candidate = {replacement}') if 80 < matchStrength < matchTolerance else None

                if matchStrength > matchTolerance:
                    # print(f'Matched {searchTerm} and {item} with a match confidence of {matchStrength}.    Replacing with {replacement}') if matchStrength < 99 else None
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

matched = 0
unmatched = 0
unmatchedItems = []

for i, line in enumerate(lines):
    splitLine = line.split(',')
    # remove last line
    splitLine.pop(-1)
    # print(splitLine)

    # convert date to 0d/0d/YYYY
    date = splitLine[1]
    d, m, y = date.split('/')
    d = '0' + d if len(d) < 2 else d
    m = '0' + m if len(m) < 2 else m
    convertedDate = "/".join((d, m, y))
    splitLine[1] = convertedDate

    # Search through third item in list.
    result = searchAndReplace(splitLine, lut.payees)

    if result:
        splitLine.extend(result)
        # Check if formatted ca:subcat
        if ":" in result[1]:
            cat, subcat = result[1].split(':')
            # print(f"formatted as x:y. Split {cat} and {subcat}.")
            result[1] = cat
            result[2] = subcat
        # Add updated line to new file
        with open("./FormattedExport.csv", "a") as f:
            write = csv.writer(f)
            write.writerow(splitLine)

        matched += 1
        continue

    # If nothing is found, add the current line and format it
    else:
        extraLines = ['','','',]
        splitLine.extend(extraLines)
        # Add updated line to new file
        with open("./FormattedExport.csv", "a") as f:
            write = csv.writer(f)
            write.writerow(splitLine)

        unmatched += 1
        unmatchedItems.append(splitLine[3])
        # print(splitLine[3])
        continue

print(f"{matched} matches.")
print(f"{unmatched} not matched.")

# setOfItems = set(unmatchedItems)
# (print(i) for i in unmatchedItems)


