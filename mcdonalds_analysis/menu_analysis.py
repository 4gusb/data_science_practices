import os
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import seaborn as sns

try:
    conn = mysql.connector.connect(user=user, password=password,
                                    host=host, 
                                    database=database,
                                    port=port)
    print("MySQL Database connection successful")
except:
    print("Error")


print("\n--------------DATAFRAME--------------\n")
df = pd.read_sql("SELECT * FROM mcmenu", conn)
print(df)
 

print("\n--------------STATISTICS--------------\n")
stats = df.describe(include="all")
print(stats)


print("\n--------------FOOD ITEM W THE MAXIMUM SODIUM CONTENT--------------\n")
max = df.at[df['Sodium'].idxmax(), 'Item']
print(max)


print("\n--------------SODIUM AMOUNT--------------\n")
swarmplot = sns.swarmplot(x='Category', y= 'Sodium', data=df)
plt.setp(swarmplot.get_xticklabels(), rotation=70)


print("\n--------------SODIUM-TOTAL FAT CORRELATION--------------")
jointplot = sns.jointplot(x='Sodium', y='Total Fat', data=df)
plt.show()


print("\n--------------SODIUM VALUES DISTRIBUTION\n--------------")
boxplot = sns.set_style("darkgrid")
ax = sns.boxplot(x=df['Sodium'])
plt.show()

--
