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
    numTimeSteps = random.randint(3,3)
    timeStepGroups = []
    
    # generate numbers beween 2 and 4 for the number of indexes for each time step
    for i in range(numTimeSteps):
        timeStepGroups.append(random.randint(3,4))

    # returns the labels in a grouped format
    groupedLabels = labelGen(timeStepGroups)
    generatePaths(groupedLabels,"low")



def mediumComplexity():
    labelNames.clear()
    # 3 - 5
    numTimeSteps = random.randint(4,5)
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
        groupsPerTimeStep = []
        for count in range(timeStepGroups[i]):
            # list flattented list of all the timesteps
            labelNames.append(letter + str(count + 1))
            # nestedLabels organized by index
            groupsPerTimeStep.append(letter + str(count + 1))
        groupedLabels.append(groupsPerTimeStep)

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

    # print(groupedLabels)
    flowsCount = []
    
    # figuring out how many flows should be between timesteps
    for timestep in range(len(groupedLabels) - 1):
        nextTimeStepLength = len(groupedLabels[timestep + 1])
        currentTimeStepLength = len(groupedLabels[timestep])

        flowNumber = random.randint(currentTimeStepLength, nextTimeStepLength*currentTimeStepLength)
        while(flowNumber in flowsCount and len(flowsCount) != (nextTimeStepLength*currentTimeStepLength) - nextTimeStepLength): 
            flowNumber = random.randint(currentTimeStepLength, nextTimeStepLength*currentTimeStepLength)

        

        flowsCount.append(flowNumber)

    print(groupedLabels)
    print(flowsCount)

   
    for timeStep in range(len(groupedLabels) - 1):
        timeStepFlows = flowsCount.pop(0)
        print("\n\n")

        flowsPerGroup = generateSetSum(len(groupedLabels[timeStep]), timeStepFlows, len(groupedLabels[timestep + 1]), 1)
        print(flowsPerGroup)

        for group in range(len(groupedLabels[timeStep])):

        
            # checking if the label is the starting
            if(groupedLabels[timeStep][group] not in diagramInfo['target']):
                availableFlow = 200

            else: 
                # figure out how much flow a business has
                i = labelNames.index(groupedLabels[timeStep][group])
                indexes = [j for j in diagramInfo["target"][j] if j == i]
                values = [dictionaryInfo["value"][i] for i in indexes]
                availableFlow = sum(values)

            if(len(flowsPerGroup) != 0):
                numberOfFlows = flowsPerGroup.pop(0)
            else: 
                numberOfFlows = 0

            # generate random flows

            # minimum number of flow units per flow is 5 to make sure that the number of paths shown matches the number of paths
            flows = [10] * numberOfFlows
            availableFlow -= 10*numberOfFlows
            for temp in range(numberOfFlows):
                if(temp == numberOfFlows-1):
                    flow = availableFlow
                else: 
                    flow = round(random.randint(availableFlow//4, availableFlow)/10)*10
                    
                # randomIndex = random.randint(0, len(flows) - 1)
                # flows[randomIndex] += flow
                flows[temp] += flow
                availableFlow -= flow

            print(flows)






                


               



    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 20,
      thickness = 20,
      line = dict(color = "purple", width = 0),
      label = labelNames,
      color = "#574ae2"
    ),
    link = diagramInfo
    )])

    fig.update_layout(title_text="Sankey Diagram " + str(imageCount), font_size=10)
    # fig.show()

   
    # fig.write_image('Data/static/Diagram'+str(imageCount)+'.svg')

    # generateMetaData(diagramInfo)
 

# mode 1 is generating for the flows 
# mode 2 
def generateSetSum(n, sumVal, maxVal, mode):
    # there should be a minimum of one flow per group
    temp = [1] * n

    for num in range(sumVal - n):
        # generatinng a random index to add to
        index = random.randint(0, len(temp) - 1)

        # if that index is greater than the max
        if(maxVal != -1 and mode == 1):
            while(temp[index] + 1 > maxVal):
                index = random.randint(0, len(temp) - 1)

        temp[index] += 1
    
    return temp




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


# while imageCount <= 48:
#     lowComplexity()
#     imageCount += 1
#     mediumComplexity()
#     imageCount += 1
#     highComplexity()
#     imageCount += 1

    


lowComplexity()
# mediumComplexity()
# highComplexity()