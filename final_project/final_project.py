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



# Write and execute a SQL query to list the school names, community names and average attendance for communities with a hardship index of 98.

df = pd.read_sql("SELECT S.NAME_OF_SCHOOL, S.COMMUNITY_AREA_NAME, S.AVERAGE_STUDENT_ATTENDANCE, C.`HARDSHIP INDEX`\
                FROM chicago_schools S\
                LEFT JOIN census_chicago C \
                ON S.COMMUNITY_AREA_NAME = C.`COMMUNITY AREA NAME`\
                WHERE C.`HARDSHIP INDEX` = 98;", conn)

print(df)


# Write and execute a SQL query to list all crimes that took place at a school. Include case number, crime type and community name.

df = pd.read_sql("SELECT CRI.CASE_NUMBER, CRI.PRIMARY_TYPE, CEN.`COMMUNITY AREA NAME`\
                FROM crime_chicago CRI\
                LEFT JOIN census_chicago CEN\
                ON CRI.COMMUNITY_AREA_NUMBER = CEN.`COMMUNITY AREA NUMBER`\
                WHERE CRI.LOCATION_DESCRIPTION LIKE '%SCHOOL%';", conn)

print(df)

# Write and execute a SQL statement to create a view showing the columns listed in the following table, with new column names as shown in the second column.
# Column name in CHICAGO_PUBLIC_SCHOOLS -> Column name in view
# NAME_OF_SCHOOL -> School_Name
# Safety_Icon -> Safety_Rating
# Family_Involvement_Icon -> Family_Rating
# Environment_Icon -> Environment_Rating
# Instruction_Icon -> Instruction_Rating
# Leaders_Icon -> Leaders_Rating
# Teachers_Icon -> Teachers_Rating

cursor.execute("DROP VIEW IF EXISTS schools_view")
cursor.execute("CREATE VIEW schools_view AS\
                SELECT NAME_OF_SCHOOL AS School_Name,\
                Safety_Icon AS Safety_Rating,\
                Family_Involvement_Icon AS Family_Rating,\
                Environment_Icon AS Environment_Rating,\
                Instruction_Icon AS Instruction_Rating,\
                Leaders_Icon AS Leaders_Rating,\
                Teachers_Icon AS Teachers_Rating\
                \
                FROM chicago_schools;")

conn.commit()
print("View created successfully")

df = pd.read_sql("SELECT * FROM schools_view", conn)
print(df)


# Write and execute a SQL statement that returns all of the columns from the view.

df = pd.read_sql("SHOW COLUMNS FROM schools_view", conn)
print(df)


# Write and execute a SQL statement that returns just the school name and leaders rating from the view

df = pd.read_sql("SELECT School_Name, Leaders_Rating\
                FROM schools_view", conn)
print(df)


