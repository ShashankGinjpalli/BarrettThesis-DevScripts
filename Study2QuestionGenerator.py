import json
import csv

diagramDatabase = {}

with open('db.json') as f:
    diagramDatabase = json.load(f)

with open("study2shortlist.csv") as csvfile:
    csvReader = csv.reader(csvfile, delimiter=",")

    

    with open('QualtricsImport.txt', 'w') as file:
        file.write("[[AdvancedFormat]]\n\n")

        file.write("[[Block: Question Block]]\n\n")

        for row in csvReader:
            file.write("[[Question:MC:SingleAnswer:Horizontal]]\n")
            file.write("<span style=\"font-size:16px;\"><strong>Figure 1:</strong></span><img src=\""+diagramDatabase["Diagram"+str(row[0])]+"\"style=\"width: 1920px; height: 1080px;\"><br><br><br><strong><span style=\"font-size:16px;\">Figure 2:</span></strong><br><img src=\""+diagramDatabase["Diagram"+str(row[1])]+"\" style=\"width: 1920px; height: 1080px;\"><br><br><div><font size=\"3\"><b>Which figure do you think is more complex?</b></font></div>\n")
            file.write("[[AdvancedChoices]]\n")
            file.write("[[Choice]]\n")
            file.write("<span style=\"font-size:16px;\">Figure 1 is more complex</span>\n")
            file.write("[[Choice]]\n")
            file.write("<span style=\"font-size:16px;\">Figure 1 and Figure 2 are relatively similar in complexity</span>\n")
            file.write("[[Choice]]\n")
            file.write("<span style=\"font-size:16px;\">Figure 2 is more complex</span>\n\n")


            print(diagramDatabase["Diagram"+str(row[0])])
            print(diagramDatabase["Diagram"+str(row[1])])

