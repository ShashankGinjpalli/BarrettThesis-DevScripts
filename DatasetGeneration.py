import random
import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go 
import math
import os
import json

imageCount = 1

labelHeaders = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelHeaders = [char for char in labelHeaders]
labelNames = []


def lowComplexity():
    labelNames.clear()
    # 2 - 3 
    numTimeSteps = random.randint(2,3)
    timeStepGroups = []
    
    # generate numbers beween 2 and 4 for the number of indexes for each time step
    for i in range(numTimeSteps):
        timeStepGroups.append(random.randint(2,4))

    # returns the labels in a grouped format
    groupedLabels = labelGen(timeStepGroups)
  

    generatePaths(groupedLabels,"low")



def mediumComplexity():
    labelNames.clear()
    # 3 - 5
    numTimeSteps = random.randint(3,5)
    timeStepGroups = []
    

    for i in range(numTimeSteps):
        timeStepGroups.append(random.randint(3,5))
    groupedLabels = labelGen(timeStepGroups)
    generatePaths(groupedLabels, "med")

    


def highComplexity():
    labelNames.clear()
    # 5 - 8
    numTimeSteps = random.randint(5,8)
    timeStepGroups = []
    

    for i in range(numTimeSteps):
        timeStepGroups.append(random.randint(4,5))

    groupedLabels = labelGen(timeStepGroups)
    generatePaths(groupedLabels,"high")
    

# generates the labels for each of the time steps
def labelGen(timeStepGroups):

    # LABELS INDEXED BY LETTER
    groupedLabels = []
    for i in range(len(timeStepGroups)):
        letter = labelHeaders[i]
        timeStepLabels = []
        for count in range(timeStepGroups[i]):
            labelNames.append(letter + str(count + 1))
            timeStepLabels.append(letter + str(count + 1))
        groupedLabels.append(timeStepLabels)

    # LABELS INDEXED BY NUMBER
    
    # for i in range(len(timeStepGroups)):
    #     labelLetters = labelHeaders[0:timeStepGroups[i]]
    #     # where each label goes for each of the time steps
    #     timeStepLabels = []
    #     for letter in labelLetters:
    #         # makes a flattened list of label names
    #         labelNames.append(letter + str(i + 1))
    #         timeStepLabels.append(letter + str(i + 1))

    #     groupedLabels.append(timeStepLabels)
    # returns a nested list of label names

    return groupedLabels


def generatePaths(groupedLabels, complexityLevel):

    diagramInfo = {
        "source": [],
        "target": [],
        "value": []
    }

    # generating flow and paths
    availableFlow = 0
    for i in range(len(groupedLabels)):
        for j in range(len(groupedLabels[i])):
            if(i != len(groupedLabels) - 1):

                # If the labelName is in Target that means that its not a starting index
                if(labelNames.index(groupedLabels[i][j]) in diagramInfo["target"]):
                    # Finding all of the indexes for a label in the target
                    indexes = [index for index,x in enumerate(diagramInfo["target"]) if x == labelNames.index(groupedLabels[i][j])]
                    availableFlow = 0
                    for index in indexes:
                        availableFlow += diagramInfo["value"][index]

                # setting the starting flow with 100 each
                else:
                    availableFlow = 100

                flow = []
                for a in range(len(groupedLabels[i + 1])):
                    if(a == len(groupedLabels[i + 1]) - 1):
                        # makes sure no flow gets wasted when it is on the last group of that timestep
                        flowAmount = availableFlow
                    else:
                        # building a sliding scale for the flow

                        # flow minimum can be 25% but maximum of all of the flow if it is greater than 100
                        if(availableFlow >= 100):
                            flowAmount = round(random.randint(availableFlow//4, availableFlow)/10)*10
                        # if availible flow is less than 100 then minimum flow increases to 50%
                        elif (availableFlow >= 50 and availableFlow < 100):
                            flowAmount = round(random.randint(availableFlow//2, availableFlow)/10)*10
                        elif(availableFlow < 50 and availableFlow >= 10): 
                            flowAmount = round(random.randint(availableFlow - 10, availableFlow)/10)*10
                        else:
                            flowAmount = round(random.randint(availableFlow//2, availableFlow)/10)*10
                    
                    availableFlow -= flowAmount
                    flow.append(flowAmount)
                    


                for k in range(len(groupedLabels[i + 1])):
                    # print(groupedLabels[i][j], groupedLabels[i + 1][k])
                    diagramInfo["source"].append(labelNames.index(groupedLabels[i][j]))
                    diagramInfo["target"].append(labelNames.index(groupedLabels[i + 1][k]))
                    # assiging the flow to a random index
                    randomIndex = random.randint(0, len(flow) - 1)
                       
                    # print(randomValue)
                    diagramInfo["value"].append(flow[randomIndex])
                    flow.pop(randomIndex)
                    # diagramInfo["value"].append(1)

    print(labelNames)
    print(diagramInfo, "\n\n\n")
    

    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 20,
      thickness = 20,
      line = dict(color = "purple", width = 0),
      label = labelNames,
    ),
    link = diagramInfo
    )])

    fig.update_layout(title_text="Sankey Diagram " + str(imageCount), font_size=10)
    # fig.show()

   
    fig.write_image('Data/static/Diagram'+str(imageCount)+'.svg')

    generateMetaData(diagramInfo)
 

def generateMetaData(diagramMetadata):
    tempSource = []
    for i in diagramMetadata['source']:
        tempSource.append(labelNames[i])
    tempTarget = []
    for i in diagramMetadata['target']:
        tempTarget.append(labelNames[i])

    diagramMetadata['source'] = tempSource
    diagramMetadata['target'] = tempTarget

    with open('Data/metadata/image'+str(imageCount)+'_metadata.json','w') as outfile:
        json.dump(diagramMetadata, outfile, indent=4, sort_keys=True)


while imageCount <= 48:
    lowComplexity()
    imageCount += 1
    mediumComplexity()
    imageCount += 1
    highComplexity()
    imageCount += 1

    


# lowComplexity()
# mediumComplexity()
# highComplexity()