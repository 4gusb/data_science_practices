import mysql.connector
import pandas as pd


# CONNECTION
try:
    conn = mysql.connector.connect(user=user, password=password,
                                    host= host, 
                                    database=database,
                                    port=port)
    print("MySQL Database connection successful")
except:
    print("Error")


df = pd.read_sql("SELECT * FROM chicago_schools;", conn)
print(df)

--------------------------------------------------


# Retrieve information about columns 
df = pd.read_sql("SELECT COLUMN_NAME, DATA_TYPE\
                 FROM INFORMATION_SCHEMA.COLUMNS \
                 WHERE TABLE_NAME = 'chicago_schools'", conn)
print(df)


# Query 1: How many Elementary Schools are in the dataset?.

df = pd.read_sql("SELECT count(*) as NUMBER_OF_ES\
                 FROM chicago_schools\
                 WHERE `Elementary, Middle, or High School` = 'ES'", conn)
print(df)


# Query 2: What is the highest Safety Score?.

df = pd.read_sql("SELECT * FROM chicago_schools;", conn)
print("\nHIGHEST SAFETY SCORE\n")
max = df.at[df['SAFETY_SCORE'].idxmax(), 'SAFETY_SCORE']
print(max)


# Query 3 : Which schools have highest Safety Score?

df = pd.read_sql("SELECT NAME_OF_SCHOOL, SAFETY_SCORE\
                  FROM chicago_schools\
                  WHERE `SAFETY_SCORE` = (SELECT MAX(SAFETY_SCORE)\
                                          FROM chicago_schools)", conn)
print(df)


# Query 4: What are the top 10 schools with the highest "Average Student Attendance"?.

df = pd.read_sql("SELECT NAME_OF_SCHOOL, AVERAGE_STUDENT_ATTENDANCE\
                  FROM chicago_schools\
                  ORDER BY AVERAGE_STUDENT_ATTENDANCE DESC\
                  LIMIT 10", conn)
print(df)


# Query 5: Retrieve the list of 5 Schools with the lowest Average Student Attendance sorted in ascending order based on attendance.

df = pd.read_sql("SELECT NAME_OF_SCHOOL, AVERAGE_STUDENT_ATTENDANCE\
                  FROM chicago_schools\
                  ORDER BY AVERAGE_STUDENT_ATTENDANCE\
                  LIMIT 5", conn)
print(df)


# Query 6: Now remove the '%' sign from the above result set for Average Student Attendance column.
 
df = pd.read_sql("SELECT NAME_OF_SCHOOL, REPLACE(AVERAGE_STUDENT_ATTENDANCE, '%', ' ') as AVERAGE_STUDENT_ATTENDANCE \
                  FROM chicago_schools\
                  ORDER BY AVERAGE_STUDENT_ATTENDANCE\
                  LIMIT 5", conn)
print(df)
  

# Query 7: Which Schools have Average Student Attendance lower than 70%?.

df = pd.read_sql("SELECT NAME_OF_SCHOOL, as AVERAGE_STUDENT_ATTENDANCE \
                  FROM chicago_schools\
                  ORDER BY AVERAGE_STUDENT_ATTENDANCE\
                  LIMIT 5", conn)
print(df)
  

# Query 8: Get the total College Enrollment for each Community Area.

df = pd.read_sql("SELECT COMMUNITY_AREA_NUMBER, COMMUNITY_AREA_NAME, SUM(COLLEGE_ENROLLMENT) AS TOTAL_ENROLLMENT\
                  FROM chicago_schools\
                  GROUP BY COMMUNITY_AREA_NAME, COMMUNITY_AREA_NUMBER\
                  ORDER BY COMMUNITY_AREA_NAME", conn)
print(df)


# Query 9: Get the 5 Community Areas with the least total College Enrollment sorted in ascending order.

df = pd.read_sql("SELECT COMMUNITY_AREA_NUMBER, COMMUNITY_AREA_NAME, SUM(COLLEGE_ENROLLMENT) AS TOTAL_ENROLLMENT\
                  FROM chicago_schools\
                  GROUP BY COMMUNITY_AREA_NAME, COMMUNITY_AREA_NUMBER\
                  ORDER BY TOTAL_ENROLLMENT\
                  LIMIT 5", conn)
print(df)


# Query 10: List 5 schools with lowest safety score.

df = pd.read_sql("SELECT NAME_OF_SCHOOL, SAFETY_SCORE\
                  FROM chicago_schools\
                  ORDER BY SAFETY_SCORE\
                  LIMIT 5", conn)
print(df)


# Query 11: Get the hardship index for the community area which has College Enrollment of 4600. 

df = pd.read_sql("SELECT `HARDSHIP INDEX`, COMMUNITY_AREA_NUMBER\
                  FROM\
                        (SELECT COMMUNITY_AREA_NUMBER, COMMUNITY_AREA_NAME, SUM(COLLEGE_ENROLLMENT) as TOTAL_ENROLLMENT, `HARDSHIP INDEX`\
                        FROM chicago_schools CS, census_chicago CC\
                        WHERE CS.COMMUNITY_AREA_NUMBER = CC.`COMMUNITY AREA NUMBER`\
                        GROUP BY COMMUNITY_AREA_NAME, COMMUNITY_AREA_NUMBER, `HARDSHIP INDEX` \
                        ORDER BY COMMUNITY_AREA_NUMBER) second_tab\
		              WHERE second_tab.TOTAL_ENROLLMENT = 4600;", conn)

print(df)


# Query 12: Get the hardship index for the community area which has the highest value for College Enrollment.

# This table will link hardship indexes with community areas and their total amount of enrollments.
enrollments = pd.read_sql("SELECT COMMUNITY_AREA_NUMBER, COMMUNITY_AREA_NAME, `HARDSHIP INDEX`, SUM(COLLEGE_ENROLLMENT) AS TOTAL_ENROLLMENT\
                           FROM chicago_schools CS, census_chicago CC\
                           WHERE CS.COMMUNITY_AREA_NUMBER = CC.`COMMUNITY AREA NUMBER`\
                           GROUP BY COMMUNITY_AREA_NUMBER, COMMUNITY_AREA_NAME, `HARDSHIP INDEX`"
                          , conn)
print(enrollments)

# Returns hardship index for the community with the highest total enrollment retrieved with the above tab.
print("\nHARDSHIP_INDEX:\n")
max = enrollments.at[enrollments['TOTAL_ENROLLMENT'].idxmax(), 'HARDSHIP INDEX']
print(max)

--
