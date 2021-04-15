import pandas as pd
from pingouin import ancova

df = pd.read_csv("Analysis/AncovaSpreadsheet.csv")

# print(df.head())

TimeStepsvsAcc = ancova(data=df, dv='Study1Question Accuracy', covar=['Number of Flows','Number of crossover flows', 'Number of Groups'], between='Number of Timesteps')
print(TimeStepsvsAcc.head(1))

FlowsvsAcc = ancova(data=df, dv='Study1Question Accuracy', covar=['Number of Timesteps','Number of crossover flows', 'Number of Groups'], between='Number of Flows')
print(FlowsvsAcc.head(1))

CrossovervsAcc = ancova(data=df, dv='Study1Question Accuracy', covar=['Number of Timesteps','Number of Flows', 'Number of Groups'], between='Number of crossover flows')
print(CrossovervsAcc.head(1))

GroupsvsAcc = ancova(data=df, dv='Study1Question Accuracy', covar=['Number of Flows','Number of crossover flows', 'Number of Timesteps'], between='Number of Groups')
print(GroupsvsAcc.head(1))

# InitialvsAcc = ancova(data=df, dv='Study1Question Accuracy', covar=['Number of Flows','Number of crossover flows', 'Number of Timesteps', 'Number of Groups'], between='Complexity Level')
# print(InitialvsAcc)

print("\n\n\n\n\n\n")


TimeStepsvsComplexity = ancova(data=df, dv='Study2 Complexity Score', covar=['Number of Flows','Number of crossover flows', 'Number of Groups'], between='Number of Timesteps')
print(TimeStepsvsComplexity.head(1))

FlowsvsComplexity = ancova(data=df, dv='Study2 Complexity Score', covar=['Number of Timesteps','Number of crossover flows', 'Number of Groups'], between='Number of Flows')
print(FlowsvsComplexity.head(1))

CrossovervsCompexity = ancova(data=df, dv='Study2 Complexity Score', covar=['Number of Timesteps','Number of Flows', 'Number of Groups'], between='Number of crossover flows')
print(CrossovervsCompexity.head(1))

GroupsvsComplexity = ancova(data=df, dv='Study2 Complexity Score', covar=['Number of Flows','Number of crossover flows', 'Number of Timesteps'], between='Number of Groups')
print(GroupsvsComplexity.head(1))

# InitialvsComplexity = ancova(data=df, dv='Study2 Complexity Score', covar=['Number of Flows','Number of crossover flows', 'Number of Timesteps', 'Number of Groups'], between='Complexity Level')
# print(InitialvsComplexity.head(1))


frames = [TimeStepsvsAcc, FlowsvsAcc,CrossovervsAcc, GroupsvsAcc, TimeStepsvsComplexity, FlowsvsComplexity, CrossovervsCompexity, GroupsvsComplexity]

newdf = pd.concat(frames)

print(newdf)

newdf.to_csv('Analysis/AncovaResults.csv')