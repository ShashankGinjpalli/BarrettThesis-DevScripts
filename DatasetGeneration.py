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
    # 4 - 5
    numTimeSteps = random.randint(4,5)
    timeStepGroups = []
    

    for i in range(numTimeSteps):
        timeStepGroups.append(random.randint(3,5))
    groupedLabels = labelGen(timeStepGroups)
    generatePaths(groupedLabels, "med")

    

def highComplexity():
    labelNames.clear()
    # 5 - 8
    numTimeSteps = random.randint(5,6)
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

    return groupedLabels


def generatePaths(groupedLabels, complexityLevel):

    diagramInfo = {
        "source": [],
        "target": [],
        "value": []
    }

    print("\n\n",complexityLevel)

    flowsCount = []
    flowValuesUsed = []
    
    # figuring out how many flows should be between timesteps
    for timestep in range(len(groupedLabels) - 1):
        nextTimeStepLength = len(groupedLabels[timestep + 1])
        currentTimeStepLength = len(groupedLabels[timestep])

        flowNumber = random.randint(nextTimeStepLength, nextTimeStepLength*currentTimeStepLength)
        while(flowNumber in flowsCount and len(flowsCount) != (nextTimeStepLength*currentTimeStepLength) - nextTimeStepLength): 
            flowNumber = random.randint(nextTimeStepLength, nextTimeStepLength*currentTimeStepLength)

        flowsCount.append(flowNumber)

    print(groupedLabels)
    print(flowsCount)

   
    # Generating the Flow Amount for Each group in the diagram
    for timestep in range(len(groupedLabels) - 1):
        timeStepFlows = flowsCount.pop(0)
        print("\n\n")

        print((len(groupedLabels[timestep]), len(groupedLabels[timestep + 1]), timestep, groupedLabels[timestep], groupedLabels[timestep + 1]))
        flowsPerGroup = generateSetSum(len(groupedLabels[timestep]), timeStepFlows, len(groupedLabels[timestep + 1]), 1)
        print("Number of Flows Per Group", flowsPerGroup)


        # make a tracker dictionary that keeps track of the number of times a group gets flow in the next timestep
        # we want every group to have at least 
        tracker = {}
        for groupName in groupedLabels[timestep + 1]:
            tracker[groupName] = 0


        for group in range(len(groupedLabels[timestep])):

            # checking if the label is the starting
            if(labelNames.index(groupedLabels[timestep][group]) not in diagramInfo["target"]):
                if(complexityLevel == 'easy'):
                    availableFlow = 30
                elif (complexityLevel == 'med'):
                    availableFlow = 50
                else:
                    availableFlow = 80

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



            print("\n\nGroup: ", groupedLabels[timestep][group])
            print("Starting Availible Flow", availableFlow)

            

            # flowFraction = round(availableFlow/10)
            # if(flowFraction == 0):
            #     flowFraction = 1

            flows = generateFlowPerGroup(flowValuesUsed, availableFlow, numberOfFlows)

            retry = 0
            while((max(flows) in flowValuesUsed and max(flows) != 100 and len(flows) != 1  and retry <= 50)):
                flows = generateFlowPerGroup(flowValuesUsed, availableFlow, numberOfFlows)

            flowValuesUsed.append(max(flows))
                
            targets = []
            groupsVisited = []
            for path in flows:
                diagramInfo["source"].append(labelNames.index(groupedLabels[timestep][group]))
                diagramInfo["value"].append(path)

                # Make sure that each one of the groups in the next timestep get at least one flow going to it from the previous timestep
                
                for target in tracker.keys():

                    if(0 in list(tracker.values())):
                        if(tracker[target] == 0):
                            targets.append(target)
                    # only open up complete randomness when every single flow in the next timestep has a flow going to it
                    else:
                        targets.append(target)
                
                # Use the Tracker Dictionary to figure out which group to send the flow to 
                print("Availible Targets: ",targets )
                randomIndex = random.randint(0,len(targets) - 1)

                # make sure that the same group doesnt go to the same target group more than once
                while(targets[randomIndex] in groupsVisited):
                    randomIndex = random.randint(0,len(targets) - 1)

                tracker[targets[randomIndex]] += 1
                print("targetChosen", targets[randomIndex])
                groupsVisited.append(targets[randomIndex])
                diagramInfo["target"].append(labelNames.index(targets[randomIndex]))
                targets.clear()
                


            
    print(diagramInfo, "\n\n\n")
    print(max(diagramInfo['value']), diagramInfo['value'].index(max(diagramInfo['value'])))



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

   
    fig.write_image('Data/static/Diagram'+str(imageCount)+'.jpg' , width=1920, height=1080, scale=1)
    generateMetaData(diagramInfo)


# used to generate the number of flows in each of the timesteps
def generateFlowPerGroup(flowValuesUsed, availableFlow, numberOfFlows): 
    flows = [0] * numberOfFlows

    # print("Starting Flows", flows)
    # availableFlow -= flowFraction*numberOfFlows
    flowStorage = availableFlow

    for temp in range(numberOfFlows):
        if(availableFlow <= 0):
                    break

        if(temp == numberOfFlows-1):
            flow = availableFlow
        else:
            rangeSet = range(availableFlow//4, availableFlow//2 + 1)
            if(set(rangeSet).issubset(flowValuesUsed)):
                flow = round(random.randint((availableFlow*2)//7, (availableFlow * 6)//7))
            else:
                flow = round(random.randint(availableFlow//4, (availableFlow)//2))
    
        flows[temp] += flow
        availableFlow -= flow

        # print("flow, amount left: ", (flow, availableFlow))

    print("Flow Amount Per Group", flows)
    return flows

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