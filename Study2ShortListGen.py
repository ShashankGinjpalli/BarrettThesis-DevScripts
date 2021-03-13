
import csv

d = {}

totalSet = set()

with open("Study 2 Shortlist - Sheet1.csv") as csvfile:
    csvReader = csv.reader(csvfile, delimiter=",")

    rowCount = 0
    for row in csvReader:
        if(rowCount != 0):
            if(row[1] not in d.keys()):
                d[row[1]] = []
            d[row[1]].append(row[0].replace("Diagram ", ""))

        rowCount += 1

print(d)


MAXDISTANCEAWAY = 10

for i in d:

    searchList = []
    MINDIST = int(i) - MAXDISTANCEAWAY
    MAXDIST = int(i) + MAXDISTANCEAWAY

    r = list(range(MINDIST, MAXDIST))
    # print(r)

    for j in r:
        if(i == str(j)):
            continue
        try:
            searchList.extend(d[str(j)])
        except KeyError:
            continue

    # print(d[i])
    # print(searchList)

    for elem1 in d[i]:
        for elem2 in searchList:

            if(tuple(sorted((elem1, elem2))) in totalSet):
                continue
            else:
                totalSet.add((elem1, elem2))

print(sorted(totalSet))
print(len(totalSet))

with open("study2shortlist.csv", "w") as csvFile:
    csvWriter = csv.writer(csvFile)
    for i in sorted(totalSet):
        csvWriter.writerow(i)
    

