import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats        
sns.set_theme(style="whitegrid")

data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Question 4
## Relation between Budget and Gross_worldwide
## Budget and Gross_worldwide may have linear relation

sns.lmplot(data=data,x='Budget',y='Gross_worldwide')