import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Question 10
## How distribution of gross by Keywords
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
          gross.append(dataframe['Gross_worldwide'][i])
          count.append(1)
    #Tạo dataFrame
    t = pd.DataFrame({colName:result, 'Money':gross, 'Count':count})
    #Loại bỏ các giá trị trùng nhau và cộng các hàng tương ứng lại 
    result = t.groupby(colName).sum()
    #Sắp xếp lại dataFrame
    sort_by_money = result.sort_values('Money', ascending = False)
    return sort_by_money

keyword=parseWithMoneyAndCount(data,'Keywords')
keyword=keyword[keyword['Count']>20]
keyword.reset_index(inplace=True)
keyword=keyword.assign(Average=keyword['Money']/keyword['Count'])
fig=plt.figure(figsize=(30,100))
plt.subplot(2,1,1)
data2=keyword.sort_values(by='Average',ascending=False)[0:50]
plt.bar(data=data2,x='Keywords',height='Average',color="salmon")
plt.xticks(rotation=90,fontsize=30)
plt.ylabel("Average Gross",fontsize=50)


listKeywords=list(data2['Keywords'])

def splitMultivaluedField(dataframe, colName):
    result = []
    gross = []
    budget=[]
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



keyword=splitMultivaluedField(data,'Keywords')
keyword=keyword[keyword['Keywords'].isin(listKeywords)]
# plt.figure(figsize=(16,9))
# plt.subplot(2,1,2)

fig, ax = plt.subplots(figsize=(12,9)) 
max=np.max(keyword['Money'])
sentinel, = ax.plot(listKeywords, np.linspace(0, max, len(listKeywords)))
sentinel.remove()

ax=plt.scatter(data=keyword,x='Keywords',y='Money')
plt.xticks(rotation=90)
plt.xlabel("Keyword",fontsize=30)
plt.title("Distribution of Gross by Keywords",fontsize=40)
plt.show()
