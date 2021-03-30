import csv
import matplotlib.pyplot as plt

questionOrder = []
questionComplexity = []

with open("Analysis/study2shortlist.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')

    for row in csvReader:
        questionOrder.append(row)

print(len(questionOrder))

# 2d array for the pairwise ranking
rankings = []

for i in range(45):
    rankings.append([i + 1, 0])

with open('Analysis/Study1AnswersSheet.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter = ";")
    for row in csvReader: 
        questionComplexity.append([row[0],int(row[5])])


with open("Analysis/Study2Responses.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter = ",")

    for row in csvReader:
        i = 0
        for answer in row:

            question = questionOrder[i]
            if(answer == 'Figure 1 is more complex'):
                rankings[int(question[0]) - 1][1] += 10
                rankings[int(question[1]) - 1][1] -= 10
                
            elif(answer == 'Figure 2 is more complex'):
                rankings[int(question[0]) - 1][1] -= 10
                rankings[int(question[1]) - 1][1] += 10

            else: 
                rankings[int(question[0]) - 1][1] += 0
                rankings[int(question[1]) - 1][1] += 0


            i += 1

sortedRankings = sorted(rankings, key=lambda x:x[1])
mn = sortedRankings[0][1]
mx = sortedRankings[len(sortedRankings) - 1][1]

questionComplexity = sorted(questionComplexity, key = lambda x:x[1])
# normalize rankings: 

print(questionComplexity, "\n\n")
for i in range(len(rankings)): 
    normalize = ((rankings[i][1] - mn)/(mx - mn))*100
    rankings[i][1] = normalize

print(rankings, "\n")


# Order According to the order in the charts in study 1
orderedVisualComplexity = []

for i in range(len(questionComplexity)):
    diagramName = questionComplexity[i][0]
    diagramName = int(diagramName.replace('Diagram ',""))

    orderedVisualComplexity.append(rankings[diagramName - 1][1])

# for i in sortedRankings:
#     orderedVisualComplexity.append(i[0])


print(orderedVisualComplexity)

orderedRealComplexity = [(i[1] - 17)/(329)*100 for i in questionComplexity]

# orderedRealComplexity = [int(i[0].replace('Diagram ', '')) for i in questionComplexity]

# Graph the complexities from the 2 studies

x = list(range(45))
plt.plot(x,orderedVisualComplexity, color = 'blue')
plt.plot(x,orderedRealComplexity, color = "red")
plt.show()
