import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Question 11
## How distribution of gross by Certificate
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

certificate=parseWithMoneyAndCount(data,'ListOfCertificate')
certificate.reset_index(inplace=True)
certificate=certificate.assign(Average=certificate['Money']/certificate['Count'])
fig=plt.figure(figsize=(12,8))
data2=certificate.sort_values(by='Average',ascending=False)
plt.bar(data=data2,x='ListOfCertificate',height='Average',color="salmon")
plt.xticks(rotation=90,fontsize=10)
plt.ylabel("Average Gross",fontsize=20)
plt.show()



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


certificate=splitMultivaluedField(data,'ListOfCertificate')
fig, ax = plt.subplots(figsize=(12,8)) 
ax=plt.scatter(data=certificate,x='ListOfCertificate',y='Money')
plt.xticks(rotation=90)
plt.xlabel("ListOfCertificate",fontsize=10)
plt.title("Distribution of Gross by Certificate",fontsize=30)
plt.show()
