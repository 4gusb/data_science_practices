import mysql.connector
import pandas as pd


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


# This view shows relation between communities info. and crime values throughout census information years.

cursor.execute("DROP VIEW communities_info_view")
cursor.execute("CREATE VIEW communities_info_VIEW AS\
                SELECT CENSUS.`COMMUNITY AREA NUMBER`, CENSUS.`COMMUNITY AREA NAME`, CENSUS.`PER CAPITA INCOME`,\
                CENSUS.`PERCENT HOUSEHOLDS BELOW POVERTY`, CRIME.PRIMARY_TYPE as CRIME_TYPE, CRIME.DATE, CRIME.BLOCK\
                FROM census_chicago CENSUS\
                LEFT JOIN crime_chicago CRIME\
                ON CENSUS.`COMMUNITY AREA NUMBER` = CRIME.COMMUNITY_AREA_NUMBER\
                WHERE YEAR(CRIME.DATE) BETWEEN 2008 AND 2012")
conn.commit()

df = pd.read_sql("SELECT * FROM communities_info_VIEW", conn)
print(df)


# Start a procedure that will return all of the view values.

cursor.execute("DROP PROCEDURE IF EXISTS select_all")
cursor.execute("CREATE PROCEDURE select_all()\
                BEGIN\
                     SELECT * FROM communities_info_VIEW;\
                END")
conn.commit()

df = pd.read_sql("CALL select_all", conn)
print(df)

cursor.close()
conn.close()

--
