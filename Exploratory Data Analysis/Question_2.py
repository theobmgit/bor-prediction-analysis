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
## How are the number of release by month?
## 


month=data['Release_Month'].value_counts().sort_index().reset_index()
month=month.rename(columns={"index":"Release_Month","Release_Month":"Count"})
month.plot.bar(x='Release_Month',y='Count')




