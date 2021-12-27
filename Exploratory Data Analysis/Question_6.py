import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Question 6
## Studio and total gross of the movies they work for
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

studio = parseWithMoneyAndCount(data,'Studios')
studio.reset_index(inplace=True)
studio=studio.assign(Average=studio['Money']/studio['Count'])
fig=plt.figure(figsize=(30,100))
plt.subplot(2,1,1)
data2=studio.sort_values(by='Money',ascending=False)[0:20]
plt.bar(data=data2,x='Studios',height='Money',color="salmon")
plt.xticks(rotation=90,fontsize=30)
plt.ylabel("Total Gross",fontsize=50)
plt.title("Studio and Total Gross of Movies they work for",fontsize=50)

plt.subplot(2,1,2)
data3=studio.sort_values(by='Average',ascending=False)[0:20]
plt.bar(data=data3,x='Studios',height='Average',color="salmon")
plt.xticks(rotation=90,fontsize=30)
plt.title("Studio and Average Gross per movie they workfor",fontsize=50)
plt.xlabel("Studio",fontsize=50)
plt.ylabel("Average Gross",fontsize=50)
plt.show()