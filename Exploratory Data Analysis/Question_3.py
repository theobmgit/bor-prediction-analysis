import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Correlation Matrix
##  Question 3
##
import ast
cols =['Cast', 'Genre', 'Studios', 'ListOfCertificate','Keywords', 'Languages', 'Countries']
for col in cols:
    data[col]=data[col].apply(ast.literal_eval)
cols=['Budget','Runtime','Release_Year','Gross_worldwide','Rating','Rating_Count']
data=data[cols]
sns.heatmap(data.corr(),annot=True)