import csv
from matplotlib import pyplot as plt
import numpy as np
import statistics

from sklearn.linear_model import LinearRegression


# #############################
# Calculate Score Section

answers = []
results = {}
participantAccuracy = []

with open("Analysis/Study1AnswersSheet.csv") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=';')

    linecount = 0

    for row in csvReader:
        row[5] = int(row[5])
        answers.append(row)
        if(row[0] not in results):
            results[row[0]] = {
                'questionCorrect':[0,0,0,0],
                'questionAppeared':[0,0,0,0],
                'complexity': row[5]
            }



# print(results)

with open("Analysis/QualtricsDataStudy1Prepped.csv") as csvFile:
    csv_reader = csv.reader(csvFile, delimiter=';')

    linecount = 0
    for row in csv_reader:
        if(linecount > 1):
            diagramCount = 0
            numCorrect = 0
            for i in range(0,len(row),4):
                diagramCount += 1
                q1 = row[i]
                q2 = row[i + 1]
                q3 = row[i + 2]
                q4 = row[i + 3]


                if(q1 != ''):
                    q1Answer = answers[diagramCount - 1][1]
                    q1 = q1.replace(" ","")
                    q1Answer = q1Answer.replace(" ", "")


                    if(q1.lower() == q1Answer.lower()):
                        numCorrect += 1
                        results['Diagram ' + str(diagramCount)]['questionCorrect'][0] += 1
                    
                    results['Diagram ' + str(diagramCount)]['questionAppeared'][0] += 1

                    
                
                if(q2 != ''):
                    q2Answer = answers[diagramCount-1][2]
                    q2 = q2.replace(" ","")
                    q2Answer = q2Answer.replace(" ", "")


                    if(q2.lower() == q2Answer.lower()):
                        numCorrect += 1
                        results['Diagram ' + str(diagramCount)]['questionCorrect'][1] += 1
                    results['Diagram ' + str(diagramCount)]['questionAppeared'][1] += 1

                
                if(q3 != ''):

                    
                    q3Answer = answers[diagramCount-1][3]

                    
                    q3 = q3.replace(" ","")
                    q3Answer = q3Answer.replace(" ", "")


                    if(q3.lower() == q3Answer.lower()):
                        numCorrect += 1
                        results['Diagram ' + str(diagramCount)]['questionCorrect'][2] += 1
                    results['Diagram ' + str(diagramCount)]['questionAppeared'][2] += 1


                    


                if(q4 != ''):
                    q4Answer = answers[diagramCount-1][4]
                    q4 = q4.replace(" ","")
                    q4Answer = q4Answer.replace(" ", "")


                    if(q4.lower() == q4Answer.lower()):
                        numCorrect += 1
                        results['Diagram ' + str(diagramCount)]['questionCorrect'][3] += 1
                    results['Diagram ' + str(diagramCount)]['questionAppeared'][3] += 1

            participantAccuracy.append(numCorrect)



        linecount += 1

print(results, "\n\n")

# #########################################
#  Participant Accuracy Stats
# ########################################


print("Average Participant Accuracy: ",(sum(participantAccuracy)/len(participantAccuracy))/18*100)
print("Min Participant Accuracy: ", (min(participantAccuracy))/18*100)
print("Max Participant Accuracy: ", (max(participantAccuracy))/18*100)
print("Median Participant Accuracy: ", statistics.median(participantAccuracy)/18*100)
print("Standard Deviation", np.std(participantAccuracy)/18 * 100)

# ##########################################
# Calculate the Accuracy of Each Diagram
# ##########################################

diagramAccuracy = []

with open('Analysis/study1questionAccuracy.csv','w') as csvFile:
    csvWriter = csv.writer(csvFile)
    

    for key in results.keys():
        tmp = results[key]
        acc = sum(tmp['questionCorrect'])/sum(tmp['questionAppeared']) * 100

        # acc = []
        # for i in range(len(tmp['questionCorrect'])):
        #     acc.append(tmp['questionCorrect'][i]/tmp['questionAppeared'][i] * 100)
        diagramAccuracy.append(acc)
        csvWriter.writerow([acc])
        # print(key, " ", acc)







# #####################################
# Generate Graph Section
# #####################################

answers = sorted(answers, key=lambda x:x[5])
# print(answers)

x = []
complexity = []
q1AccuracyTrain = []
q2AccuracyTrain = []
q3AccuracyTrain = []
q4AccuracyTrain = []
totalAccuracyTrain = []

# print(answers)
for i in range(len(answers)):
    
    x.append(i + 1)
    normalized = ((answers[i][5] - 17)/(329))*100
    complexity.append(normalized)
    # complexity.append(answers[i][5]/346 * 100)

    diagramNo = answers[i][0]

    q1AccuracyTrain.append((results[diagramNo]['questionCorrect'][0]/results[diagramNo]['questionAppeared'][0])*100)


    totalAccuracyTrain.append((sum(results[diagramNo]['questionCorrect'])/sum(results[diagramNo]['questionAppeared']))*100)
    # print((results[diagramNo]['questionCorrect'][0]/results[diagramNo]['questionAppeared'][0])*100)
    q2AccuracyTrain.append((results[diagramNo]['questionCorrect'][1]/results[diagramNo]['questionAppeared'][1])*100)
    q3AccuracyTrain.append((results[diagramNo]['questionCorrect'][2]/results[diagramNo]['questionAppeared'][2])*100)
    q4AccuracyTrain.append((results[diagramNo]['questionCorrect'][3]/results[diagramNo]['questionAppeared'][3])*100)


# Using linear regression to plot the accuracy so that we can flatten alot of the spikes 
xtrain = np.array(x).reshape((-1,1))
# print(xtrain)
q1reg = LinearRegression().fit(xtrain,np.array(q1AccuracyTrain))
q2reg = LinearRegression().fit(xtrain,np.array(q2AccuracyTrain))
q3reg = LinearRegression().fit(xtrain,np.array(q3AccuracyTrain))
q4reg = LinearRegression().fit(xtrain,np.array(q4AccuracyTrain))
totalreg = LinearRegression().fit(xtrain,np.array(totalAccuracyTrain))



q1Accuracy = q1reg.predict(xtrain)
q2Accuracy = q2reg.predict(xtrain)
q3Accuracy = q3reg.predict(xtrain)
q4Accuracy = q4reg.predict(xtrain)
totalAccuracy = totalreg.predict(xtrain)


plt.figure(figsize=(12,8)) 

plt.plot(x, complexity, color='red', label = "Dataset Complexity")
plt.plot(x, q1Accuracy, color='blue', label = "Largest # of Flows Between 2 Timesteps Accuracy")
plt.plot(x, q2Accuracy, color='green', label = "Largest Group Accuracy")
plt.plot(x, q3Accuracy, color='orange', label= "Largest Flow Accuracy")
plt.plot(x, q4Accuracy, color='purple', label = "Largest Number of Connections Accuracy")
plt.plot(x,totalAccuracy, color = 'black', label = "Overall Question Accuracy")
plt.legend()



plt.tick_params(labeltop=False, labelright=True)
plt.xlabel("Diagram Number")
plt.ylabel("Accuracy(%)/DatasetComplexity(%)")

plt.title("Question Accuracy vs Diagram Complexity")

# plt.show()


plt.savefig('PostLinearRegressionTrends.png')



