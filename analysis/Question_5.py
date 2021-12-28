import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Question 5
## Cast and average gross of the movies they cast for
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

cast = parseWithMoneyAndCount(data,'Cast')
cast.reset_index(inplace=True)
cast=cast.assign(Average=cast['Money']/cast['Count'])
fig=plt.figure(figsize=(30,30))
plt.subplot(2,1,1)
data2=cast.sort_values(by='Money',ascending=False)[0:50]
plt.bar(data=data2,x='Cast',height='Money',color="salmon")
plt.xticks(rotation=90)
plt.xlabel("Cast")
plt.xlabel("Total Gross")
plt.title("Cast and Total Gross of Movies they cast for")

plt.subplot(2,1,2)
data3=cast.sort_values(by='Average',ascending=False)[0:50]
plt.bar(data=data3,x='Cast',height='Average',color="salmon")
plt.xticks(rotation=90)
plt.title("Cast and Average Gross of Movies they cast for")
plt.xlabel("Cast")
plt.xlabel("Average Gross")
plt.show()