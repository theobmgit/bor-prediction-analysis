import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Question 9
## How distribution of gross by Languages
## 
## 
import ast
cols =['Cast', 'Genre', 'Studios', 'ListOfCertificate','Keywords', 'Languages', 'Countries']
for col in cols:
    data[col]=data[col].apply(ast.literal_eval)


def parseWithMoneyAndCount(dataframe, colName):
    result = []
    count = []
    gross = []
    for i,record in enumerate(dataframe[colName]):
      for x in record:
        #Lưu kết quả vào mảng tương ứng
          result.append(x)
          gross.append(dataframe['Gross_worldwide'][i]/len(record))
          count.append(1)
    #Tạo dataFrame
    t = pd.DataFrame({colName:result, 'Money':gross, 'Count':count})
    #Loại bỏ các giá trị trùng nhau và cộng các hàng tương ứng lại 
    result = t.groupby(colName).sum()
    #Sắp xếp lại dataFrame
    sort_by_money = result.sort_values('Money', ascending = False)
    return sort_by_money

language=parseWithMoneyAndCount(data,'Languages')
language=language[language['Count']>20]
language.reset_index(inplace=True)
language=language.assign(Average=language['Money']/language['Count'])

fig=plt.figure(figsize=(30,100))
plt.subplot(2,1,1)
data2=language.sort_values(by='Money',ascending=False)
plt.bar(data=data2,x='Languages',height='Average',color="salmon")
plt.xticks(rotation=90,fontsize=30)
plt.ylabel("Average Gross",fontsize=50)

plt.subplot(2,1,2)
plt.bar(data=data2,x='Languages',height='Money',color="salmon")
plt.ylabel("Total Gross",fontsize=50)
plt.xticks(rotation=90,fontsize=30)
plt.xlabel("Languages",fontsize=50)
plt.show()

#Top languages
listLanguage=list(data2['Languages'])

def splitMultivaluedField(dataframe, colName):
    result = []
    budget=[]
    gross = []
    for i,record in enumerate(dataframe[colName]):
      for x in record:
        #Lưu kết quả vào mảng tương ứng
          result.append(x)
          budget.append(dataframe['Budget'][i]/len(record))
          gross.append(dataframe['Gross_worldwide'][i]/len(record))
    #Tạo dataFrame
    t = pd.DataFrame({colName:result,'Budget':budget, 'Money':gross})
    #Sắp xếp lại dataFrame
    sort_by_money = t.sort_values('Money', ascending = False)
    return sort_by_money

language=splitMultivaluedField(data,'Languages')
language=language[language['Languages'].isin(listLanguage)]
plt.figure(figsize=(16,9))
#sns.scatterplot(data=country,x='Budget',y='Money',hue='Countries')
language.plot.scatter(x='Languages',y='Money',color='blue')
plt.xticks(rotation=90)
plt.show()