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
    
    # generate numbers beween 2 and 3 for the number of indexes for each time step
    for i in range(numTimeSteps):
        timeStepGroups.append(random.randint(2,3))

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

    print("\n\n",complexityLevel)

    # print(groupedLabels)
    flowsCount = []
    
    # figuring out how many flows should be between timesteps
    for timestep in range(len(groupedLabels) - 1):
        nextTimeStepLength = len(groupedLabels[timestep + 1])
        currentTimeStepLength = len(groupedLabels[timestep])

        flowNumber = random.randint(currentTimeStepLength, nextTimeStepLength*currentTimeStepLength)
        while(flowNumber in flowsCount and len(flowsCount) != (nextTimeStepLength*currentTimeStepLength) - nextTimeStepLength): 
            flowNumber = random.randint(currentTimeStepLength, nextTimeStepLength*currentTimeStepLength)
            # print("Regenerating Flows")

        

        flowsCount.append(flowNumber)

    print(groupedLabels)
    print(flowsCount)

   
    for timestep in range(len(groupedLabels) - 1):
        timeStepFlows = flowsCount.pop(0)
        print("\n\n")

        print((len(groupedLabels[timestep]), len(groupedLabels[timestep + 1]), timestep, groupedLabels[timestep], groupedLabels[timestep + 1]))
        flowsPerGroup = generateSetSum(len(groupedLabels[timestep]), timeStepFlows, len(groupedLabels[timestep + 1]), 1)
        print("Number of Flows Per Group", flowsPerGroup)

        for group in range(len(groupedLabels[timestep])):

        
            # checking if the label is the starting
            if(labelNames.index(groupedLabels[timestep][group]) not in diagramInfo["target"]):
                availableFlow = 100

            else: 
                # figure out how much flow a group has
                i = labelNames.index(groupedLabels[timestep][group])
                indexes = [index for index,x in enumerate(diagramInfo["target"]) if x == i]
                values = [diagramInfo["value"][i] for i in indexes]
                availableFlow = sum(values)

                

            if(len(flowsPerGroup) != 0):
                numberOfFlows = flowsPerGroup.pop(0)
            else: 
                numberOfFlows = 0

            # generate random flows

            # minimum number of flow units per flow is 10 to make sure that the number of paths shown matches the number of paths


            print("\n\nGroup: ", groupedLabels[timestep][group])
            print("Starting Availible Flow", availableFlow)

            # TODO fill out starting flows as 10% of the availible

            flowFraction = round(availableFlow/10)
            if(flowFraction == 0):
                flowFraction = 1
            flows = [flowFraction] * numberOfFlows

            print("Starting Flows", flows)
            availableFlow -= flowFraction*numberOfFlows

            for temp in range(numberOfFlows):
                if(availableFlow <= 0):
                    break

                if(temp == numberOfFlows-1):
                    flow = availableFlow
                else: 
                    
                    flow = round(random.randint(availableFlow//4, availableFlow))
                    
                flows[temp] += flow
                availableFlow -= flow

                print("flow, amount left: ", (flow, availableFlow))

            print("Flow Amount Per Group", flows)

            # Fill the rest of the flow array with 0's 



            targets = []
            for path in flows:
                diagramInfo["source"].append(labelNames.index(groupedLabels[timestep][group]))
                diagramInfo["value"].append(path)

                # Make sure that each one of the groups in the next timestep get at least one flow going to it from the previous timestep

                randomIndex = random.randint(0,len(groupedLabels[timestep + 1]) - 1)

                while(groupedLabels[timestep + 1][randomIndex] in targets):
                    randomIndex = random.randint(0,len(groupedLabels[timestep + 1]) - 1)

                targets.append(groupedLabels[timestep + 1][randomIndex])
                diagramInfo["target"].append(labelNames.index(groupedLabels[timestep + 1][randomIndex]))


            
    # print(diagramInfo, "\n\n\n")



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
    fig.show()

   
    # fig.write_image('Data/static/Diagram'+str(imageCount)+'.svg')

    # generateMetaData(diagramInfo)
 

# mode 1 is generating for the flows 
# mode 2 
def generateSetSum(n, sumVal, maxVal, mode):
    # there should be a minimum of one flow per group
    temp = [1] * n

    for num in range(sumVal - n):
        # generating a random index to add to
        index = random.randint(0, len(temp) - 1)

        # if that index is greater than the max
        if(maxVal != -1 and mode == 1):
            # print("Generating Index", temp, maxVal, sumVal)
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
mediumComplexity()
highComplexity()