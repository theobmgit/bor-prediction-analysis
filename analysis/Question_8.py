import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Question 8
## How distribution of gross by Countries
## 
## 
import ast
cols =['Cast', 'Genre', 'Studios', 'ListOfCertificate','Keywords', 'Languages', 'Countries']
for col in cols:
    data[col]=data[col].apply(ast.literal_eval)

def splitMultivaluedField(dataframe, colName):
    result = []
    budget=[]
    gross = []
    for i,record in enumerate(dataframe[colName]):
      for x in record:
        #Lưu kết quả vào mảng tương ứng
          result.append(x)
          budget.append(dataframe['Budget'][i])
          gross.append(dataframe['Gross_worldwide'][i])
    #Tạo dataFrame
    t = pd.DataFrame({colName:result,'Budget':budget, 'Money':gross})
    #Sắp xếp lại dataFrame
    sort_by_money = t.sort_values('Money', ascending = False)
    return sort_by_money

## This list get from Question_7.py 
list_country=['United States',
 'United Kingdom',
 'Canada',
 'Germany',
 'France',
 'Australia',
 'China',
 'Japan',
 'Mexico',
 'Hong Kong',
 'New Zealand',
 'Spain',
 'Italy',
 'India',
 'South Africa',
 'United Arab Emirates',
 'Hungary',
 'Czech Republic',
 'Ireland',
 'South Korea',
 'Belgium',
 'Denmark',
 'Switzerland',
 'Netherlands',
 'Sweden',
 'Russia']

country=splitMultivaluedField(data,'Countries')
country=country[country['Countries'].isin(list_country)]
plt.figure(figsize=(16,9))
#sns.scatterplot(data=country,x='Budget',y='Money',hue='Countries')
country.plot.scatter(x='Countries',y='Money',color='blue')
plt.xticks(rotation=90)
plt.show()