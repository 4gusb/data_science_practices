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


# Write the structure of a query to create or replace a stored procedure called UPDATE_LEADERS_SCORE\
# that takes a School ID parameter as an integer and its new Leaders Score also as an integer parameter to update it.
# Inside your stored procedure, write a SQL IF statement to update the Leaders_Icon field in the CHICAGO_PUBLIC_SCHOOLS table for the school identified by in_School_ID using the following information.
# Score lower limit	    Score upper limit	    Icon
# 80	                        99         	Very strong
# 60	                        79  	    Strong
# 40	                        59        	Average
# 20	                        39  	    Weak
# 0	                            19  	    Very weak

cursor.execute("DROP PROCEDURE IF EXISTS UPDATE_LEADERS_SCORE")
cursor.execute("CREATE PROCEDURE UPDATE_LEADERS_SCORE(IN Actual_School_ID INT, IN Actual_Leaders_Score INT)\
                BEGIN\
                        UPDATE chicago_schools\
                        SET Leaders_Score = Actual_Leaders_Score\
                        WHERE School_ID = Actual_School_ID;\
                        \
                        IF Actual_Leaders_Score > 0 AND Actual_Leaders_Score < 19 THEN\
                            UPDATE chicago_schools\
                            SET Leaders_Icon = 'Very weak'\
                            WHERE School_ID = Actual_School_ID;\
                        \
                        ELSEIF Actual_Leaders_Score < 40 THEN\
                            UPDATE chicago_schools\
                            SET Leaders_Icon = 'Weak'\
                            WHERE School_ID = Actual_School_ID;\
                        \
                        ELSEIF Actual_Leaders_Score < 60 THEN\
                            UPDATE chicago_schools\
                            SET Leaders_Icon = 'Average'\
                            WHERE School_ID = Actual_School_ID;\
                        \
                        ELSEIF Actual_Leaders_Score < 80 THEN\
                            UPDATE chicago_schools\
                            SET Leaders_Icon = 'Strong'\
                            WHERE School_ID = Actual_School_ID;\
                        \
                        ELSEIF Actual_Leaders_Score < 100 THEN\
                            UPDATE chicago_schools\
                            SET Leaders_Icon = 'Very strong'\
                            WHERE School_ID = Actual_School_ID;\
                        END IF;\
                        \
                END")

conn.commit()
print("Stored Procedure Created")

cursor.callproc("UPDATE_LEADERS_SCORE", (610544, 1))
df = pd.read_sql("SELECT School_ID, NAME_OF_SCHOOL, Leaders_Score, Leaders_Icon\
                FROM chicago_schools\
                ORDER BY School_ID DESC", conn)
print(df)


# Update your stored procedure definition. Add a generic ELSE clause to the IF statement\
# that rolls back the current work if the score did not fit any of the preceding categories.

cursor.execute("DROP PROCEDURE IF EXISTS UPDATE_LEADERS_SCORE")
conn.commit()
cursor.execute("CREATE PROCEDURE UPDATE_LEADERS_SCORE(IN Actual_School_ID INT, IN Actual_Leaders_Score INT)\
                BEGIN\
                DECLARE `rollback` BOOL DEFAULT 0;\
                DECLARE CONTINUE HANDLER FOR SQLEXCEPTION\
                    SET `rollback` = 1;\
                START TRANSACTION;\
                \
                UPDATE chicago_schools\
                SET Leaders_Score = Actual_Leaders_Score\
                WHERE School_ID = Actual_School_ID;\
                \
                IF Actual_Leaders_Score > -1 AND Actual_Leaders_Score < 101 THEN\
                    IF Actual_Leaders_Score < 19 THEN\
                        UPDATE chicago_schools\
                        SET Leaders_Icon = 'Very weak'\
                        WHERE School_ID = Actual_School_ID;\
                    \
                    ELSEIF Actual_Leaders_Score < 40 THEN\
                        UPDATE chicago_schools\
                        SET Leaders_Icon = 'Weak'\
                        WHERE School_ID = Actual_School_ID;\
                    \
                    ELSEIF Actual_Leaders_Score < 60 THEN\
                        UPDATE chicago_schools\
                        SET Leaders_Icon = 'Average'\
                        WHERE School_ID = Actual_School_ID;\
                    \
                    ELSEIF Actual_Leaders_Score < 80 THEN\
                        UPDATE chicago_schools\
                        SET Leaders_Icon = 'Strong'\
                        WHERE School_ID = Actual_School_ID;\
                    \
                    ELSE\
                        UPDATE chicago_schools\
                        SET Leaders_Icon = 'Very strong'\
                        WHERE School_ID = Actual_School_ID;\
                    END IF;\
                ELSE\
                    SET `rollback` = 1;\
                END IF;\
                \
                \
                IF `rollback` THEN\
                    ROLLBACK;\
                ELSE\
                    COMMIT;\
                END IF;\
            \
            END"
        )

# the first IF-ELSE will verify that the parameter given is positive and under 100. If not, rollback var is "turned on". 
# Then, the nested IF and ELSES statements will change values following the information given before.  

conn.commit()
print("Procedure and Transaction created")
cursor.callproc("UPDATE_LEADERS_SCORE", (610544, -90))

df = pd.read_sql("SELECT School_ID, NAME_OF_SCHOOL, Leaders_Score, Leaders_Icon\
                FROM chicago_schools\
                ORDER BY School_ID DESC", conn)
print(df)

