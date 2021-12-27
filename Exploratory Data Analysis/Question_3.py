import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
sns.set_theme(style="whitegrid")

data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Correlation Matrix,Histogram and Scatter Matrix
##  Question 3
##
import ast
cols =['Cast', 'Genre', 'Studios', 'ListOfCertificate','Keywords', 'Languages', 'Countries']
for col in cols:
    data[col]=data[col].apply(ast.literal_eval)
cols=['Budget','Runtime','Release_Year','Gross_worldwide','Rating','Rating_Count','Release_Month']
data=data[cols]
sns.heatmap(data.corr(),annot=True)

data.hist(bins=50,figsize=(20,15))

scatter_matrix(data,figsize=(20,12),hist_kwds={'bins':50})