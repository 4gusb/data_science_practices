import mysql.connector
import pandas as pd

# CONNECTION
try:
    conn = mysql.connector.connect(user=user, password=password,
                                    host=host, 
                                    database=database,
                                    port=port)
    print("MySQL Database connection successful")
except:
    print("Error")

df = pd.read_sql("SELECT * \
                  FROM crime_chicago", conn)
print(df)


# Problem 1: Find the total number of crimes recorded in the CRIME table.

df = pd.read_sql("SELECT count(*)\
                  FROM crime_chicago", conn)
print(df)


# Problem 2: List all case numbers for crimes involving minors.

df = pd.read_sql("SELECT CASE_NUMBER\
                  FROM crime_chicago\
                  WHERE DESCRIPTION LIKE '%MINOR%'", conn)
print(df)


# Problem 3: List all kidnapping crimes involving a child.

df = pd.read_sql("SELECT *\
                  FROM crime_chicago\
                  WHERE DESCRIPTION LIKE '%CHILD%'\
                  AND PRIMARY_TYPE LIKE '%KIDNAPPING%'", conn)
print(df)


# Problem 4: What kinds of crimes were recorded at schools?.

df = pd.read_sql("SELECT DISTINCT(PRIMARY_TYPE)\
                  FROM crime_chicago\
                  WHERE LOCATION_DESCRIPTION LIKE '%SCHOOL%'", conn)
print(df)


# Problem 5: Which community area number is most crime prone?

df = pd.read_sql("SELECT COUNT(COMMUNITY_AREA_NUMBER) as TOTAL_CASES, COMMUNITY_AREA_NUMBER\
                  FROM crime_chicago\
                  GROUP BY COMMUNITY_AREA_NUMBER\
                  ORDER BY TOTAL_CASES DESC\
                  LIMIT 1", conn)
print(df)


# Problem 6: Use a sub-query to determine the Community Area Name with most number of crimes.

df = pd.read_sql("SELECT *\
                  FROM (SELECT COUNT(COMMUNITY_AREA_NUMBER) as TOTAL, COMMUNITY_AREA_NUMBER, `COMMUNITY AREA NAME`\
                        FROM crime_chicago CRIME, census_chicago CENSUS\
                        WHERE `COMMUNITY AREA NUMBER` = COMMUNITY_AREA_NUMBER\
                        GROUP BY COMMUNITY_AREA_NUMBER, `COMMUNITY AREA NAME`\
                        ORDER BY TOTAL DESC\
                        LIMIT 1) t1"\
                 , conn)
print(df)

--
