import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# CONNECTION
try:
    conn = mysql.connector.connect(user=user, password=password,
                                    host= host, 
                                    database=database,
                                    port=port)
    cursor = conn.cursor()
    print("MySQL Database connection successful")
except:
    print("Error")


df = pd.read_sql("SELECT * FROM census_chicago", conn)
print(df)



# Query 1: How many rows are in the dataset?

df = pd.read_sql("SELECT count(*) as NROWS FROM census_chicago", conn)
print(df)


# Query 2: How many community areas in Chicago have a hardship index greater than 50.0?

df= pd.read_sql("SELECT count(*) FROM census_chicago WHERE `HARDSHIP INDEX` > 50", conn)
print(df)


# Query 3: What is the maximum value of hardship index in this dataset

df = pd.read_sql("SELECT max(`HARDSHIP INDEX`) as max_hardship FROM census_chicago", conn)
print(df)


# Query 4: Which community area has the highest hardship index?

# opcion 1:
max = df.at[df['HARDSHIP INDEX'].idxmax(),'COMMUNITY AREA NAME']
print(max)
# opcion 2, con mas detalles:
df = pd.read_sql("SELECT `COMMUNITY AREA NAME`, `COMMUNITY AREA NUMBER`, `HARDSHIP INDEX` FROM census_chicago WHERE `HARDSHIP INDEX`= (SELECT max(`HARDSHIP INDEX`) FROM census_chicago)", conn)
print(df)


# Query 5: Which Chicago community areas have per-capita incomes greater than $60,000?

df = pd.read_sql("SELECT `COMMUNITY AREA NAME`, `COMMUNITY AREA NUMBER`, `PER CAPITA INCOME` FROM census_chicago WHERE `PER CAPITA INCOME` > 60000", conn)
print(df)



# ---------PLOTS---------


df = pd.read_sql("SELECT * FROM census_chicago", conn)


# Query 6: Create a scatter plot using the variables per_capita_income_ and hardship_index. Explain the correlation between the two variables.

jointplot = sns.jointplot(x='PER CAPITA INCOME', y="HARDSHIP INDEX", data=df)
plt.show()

# While per capita incomes get higher, the less hardship values there are. The points are somewhat crossing a negative curve, so we can say there is a negative correlation between the two variables.


# Query 7: Correlation between per_capita_income and percent_households_below_poverty.

jointplot = sns.jointplot(x='PER CAPITA INCOME', y="PERCENT HOUSEHOLDS BELOW POVERTY", data=df)
plt.show()

# The percent of households below poverty decreases with the per capita incomes increase.


# Query 8: Correlation between per_capita_income and percent_aged_16_unemployed.

jointplot = sns.jointplot(x='PER CAPITA INCOME', y="PERCENT AGED 16+ UNEMPLOYED", data=df)
plt.show()

# The higher per capita incomes are, the less 16+ unemployees there are. So, there are much more chances to be unemployed when the per capita incomes are low.

--
