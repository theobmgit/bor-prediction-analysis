import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

data=pd.read_csv('../dataset/processed/cleanedData.csv')

import ast
cols =['Cast', 'Genre', 'Studios', 'ListOfCertificate','Keywords', 'Languages', 'Countries']
for col in cols:
    data[col]=data[col].apply(ast.literal_eval)

## Question 2
## How average gross depend on Release_Month and combine with Release_Year.
## We see that the movies release in the month [4,5,6,7,11,12]
## tend to have higher gross
cols=['Release_Month','Gross_worldwide']

month=data[cols]
month=month.groupby("Release_Month").mean().reset_index()
#1
month.plot.bar(x='Release_Month',y='Gross_worldwide')
plt.title("Average by Month")
#2
data.plot.scatter(x='Release_Month',y='Gross_worldwide')
plt.title("Scatter plot for Release_Month and Gross")
#3
rColor=[2,3,8] 
gColor=[4,5,6,7,11,12]
bColor=[1,9,10]
colorMap=dict()
for i in rColor:
    colorMap[i]='tab:red'
for i in gColor:
    colorMap[i]='tab:green'
for i in bColor:
    colorMap[i]='tab:blue'
C=colorMap
fig = plt.figure(figsize=(8,6))
sns.scatterplot(data=data,x='Release_Year',y='Gross_worldwide',hue='Release_Month',palette=C)
plt.title("How gross distributed by Month and Year")
plt.show()



