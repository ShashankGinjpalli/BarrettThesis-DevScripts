from pathlib import Path
import re
import json
import plotly.graph_objs as go 


pathlist = Path('Data/metadata/').glob('**/*.json')
for path in pathlist:
     # because path is object not string
     path_in_str = str(path)
     print(path_in_str)

     imageNum = re.findall(r"\d+", path_in_str)
     print(imageNum[0])

     labelNames = []
     
     diagramInfo = {
        "source": [],
        "target": [],
        "value": []
    }
     
     metaData = {}
     
     with open (path_in_str) as jsomFile:
          metaData = json.load(jsomFile)
          
     labelNames.extend(metaData["source"])
     labelNames.extend(metaData["target"])
     labelNames = set(labelNames)
     labelNames = list(labelNames)
     labelNames.sort()

     print(labelNames)

     for i in range(len(metaData["source"])):
          diagramInfo["source"].append(labelNames.index(metaData["source"][i]))
          diagramInfo["target"].append(labelNames.index(metaData["target"][i]))
          diagramInfo["value"].append(metaData["value"][i])

     
     fig = go.Figure(data=[go.Sankey(
          node = dict(
               pad = 20,
               thickness = 20,
               line = dict(color = "purple", width = 0),
               label = labelNames,
               color = "#574ae2"
          ),
          link = diagramInfo,
          textfont=dict(size = 28)
    )])

     fig.write_image('Data/static/Diagram'+str(imageNum[0])+'.jpg' , width=1920, height=1080, scale=1)


     






     