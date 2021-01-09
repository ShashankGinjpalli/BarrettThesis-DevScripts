import random
import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go 
import math
import os

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
            # print(groupedLabels[i][j])
            if(i != len(groupedLabels) - 1):

                if(labelNames.index(groupedLabels[i][j]) in diagramInfo["target"]):
                    # calculate the path cost availible to use
                    indexes = [index for index,x in enumerate(diagramInfo["target"]) if x == labelNames.index(groupedLabels[i][j])]
                    availableFlow = 0
                    for index in indexes:
                        availableFlow += diagramInfo["value"][index]

                else:
                    availableFlow = 10

                flow = []
                for a in range(len(groupedLabels[i + 1])):
                    if(a == len(groupedLabels[i + 1]) - 1):
                        # makes sure no flow gets wasted 
                        flowAmount = availableFlow
                    else:
                        # flow minimum can be 1/2 but maximum of all of the flow
                        flowAmount = random.randint(availableFlow//2, availableFlow)
                    availableFlow -= flowAmount
                    flow.append(flowAmount)
                    


                # print(flow)
                


                for k in range(len(groupedLabels[i + 1])):
                    # print(groupedLabels[i][j], groupedLabels[i + 1][k])
                    diagramInfo["source"].append(labelNames.index(groupedLabels[i][j]))
                    diagramInfo["target"].append(labelNames.index(groupedLabels[i + 1][k]))
                    randomIndex = random.randint(0, len(flow) - 1)
                       
                    # print(randomValue)
                    diagramInfo["value"].append(flow[randomIndex])
                    flow.pop(randomIndex)
                    # diagramInfo["value"].append(1)

    
    print(diagramInfo)
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

    # interactive Images
    if(complexityLevel == "low"):
        fig.write_html('Data/interactive/DiagramLow'+str(imageCount)+'.html')
    elif(complexityLevel == "med"):
        fig.write_html('Data/interactive/DiagramMed'+str(imageCount)+'.html')
    else:
        fig.write_html('Data/interactive/DiagramHigh'+str(imageCount)+'.html')

    # Static
    if(complexityLevel == "low"):
        fig.write_image('Data/static/DiagramLow'+str(imageCount)+'.svg')
    elif(complexityLevel == "med"):
        fig.write_image('Data/static/DiagramMed'+str(imageCount)+'.svg')
    else:
        fig.write_image('Data/static/DiagramHigh'+str(imageCount)+'.svg')

 



while imageCount <= 40:
    lowComplexity()
    mediumComplexity()
    highComplexity()

    imageCount += 1


# lowComplexity()
# mediumComplexity()
# highComplexity()