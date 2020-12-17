import random
import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go 
import math

labelHeaders = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labelHeaders = [char for char in labelHeaders]
labelNames = []

def lowComplexity():
    labelNames.clear()
    numTimeSteps = 3
    timeStepGroups = []
    
    # generate numbers beween 2 and 4 for the number of indexes for each time step
    for i in range(numTimeSteps):
        timeStepGroups.append(random.randint(1,3))

    # returns the labels in a grouped format
    groupedLabels = labelGen(timeStepGroups)
    print(groupedLabels)
    print(labelNames)

    generatePaths(groupedLabels)



def mediumComplexity():
    labelNames.clear()
    numTimeSteps = 6
    timeStepGroups = []
    

    for i in range(numTimeSteps):
        timeStepGroups.append(random.randint(1,4))
    groupedLabels = labelGen(timeStepGroups)
    generatePaths(groupedLabels)

    


def highComplexity():
    labelNames.clear()
    numTimeSteps = 10
    timeStepGroups = []
    

    for i in range(numTimeSteps):
        timeStepGroups.append(random.randint(2,5))

    # print(timeStepGroups)
    groupedLabels = labelGen(timeStepGroups)
    generatePaths(groupedLabels)
    print(labelNames)
    

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


def generatePaths(groupedLabels):

    diagramInfo = {
        "source": [],
        "target": [],
        "value": []
    }

    # generating flow and paths

    for i in range(len(groupedLabels)):
        for j in range(len(groupedLabels[i])):
            # print(groupedLabels[i][j])
            if(i != len(groupedLabels) - 1):
                
                for k in range(len(groupedLabels[i + 1])):
                    # print(groupedLabels[i][j], groupedLabels[i + 1][k])
                    diagramInfo["source"].append(labelNames.index(groupedLabels[i][j]))
                    diagramInfo["target"].append(labelNames.index(groupedLabels[i + 1][k]))
                   
                       
                        # print(randomValue)
                        # diagramInfo["value"].append(pathCosts[randomValue])
                        # pathCosts.pop(randomValue)
                    diagramInfo["value"].append(1)

    
    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 1),
      label = labelNames,
      color = "red"
    ),
    link = diagramInfo
    )])

    fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
    fig.show()






lowComplexity()
# mediumComplexity()
# highComplexity()