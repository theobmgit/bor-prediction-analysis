import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")
data=pd.read_csv('../dataset/processed/cleanedData.csv')
## Question 7
## Average gross of each countries and Total Cost
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

country = parseWithMoneyAndCount(data,'Countries')
country=country[country['Count']>20]
country.reset_index(inplace=True)
country=country.assign(Average=country['Money']/country['Count'])
fig=plt.figure(figsize=(30,100))
plt.subplot(2,1,1)
data2=country.sort_values(by='Money',ascending=False)
plt.bar(data=data2,x='Countries',height='Average',color="salmon")
plt.xticks(rotation=90,fontsize=30)
plt.ylabel("Average Gross",fontsize=50)

plt.subplot(2,1,2)
plt.bar(data=data2,x='Countries',height='Money',color="salmon")
plt.ylabel("Total Gross",fontsize=50)
plt.xticks(rotation=90,fontsize=30)
plt.xlabel("Countries",fontsize=50)
plt.show()