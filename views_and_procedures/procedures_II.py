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
    
   
# Drop table in case it exists

cursor.execute("DROP TABLE IF EXISTS pet_sale")
print("Table dropped")


# Create the table

cursor.execute("CREATE TABLE pet_sale (\
                    ID INTEGER NOT NULL,\
                    ANIMAL VARCHAR(20),\
                    SALEPRICE DECIMAL(6,2),\
                    SALEDATE DATE,\
                    QUANTITY INTEGER,\
                    PRIMARY KEY (ID))")
conn.commit()
print("Table created")


# Insert sample data into the table

cursor.execute("INSERT INTO pet_sale VALUES\
            (1,'Cat',450.09,'2018-05-29',9),\
            (2,'Dog',666.66,'2018-06-01',3),\
            (3,'Parrot',50.00,'2018-06-04',2),\
            (4,'Hamster',60.60,'2018-06-11',6),\
            (5,'Goldfish',48.48,'2018-06-14',24)")
conn.commit()
print("Values added")


#Drop procedure in case it exists

cursor.execute("DROP PROCEDURE IF EXISTS update_saleprice")
print("Procedure dropped")


#Start procedure

cursor.execute("CREATE PROCEDURE update_saleprice (IN animal_id INT, IN animal_health VARCHAR(6))\
                BEGIN\
                    IF UCASE(animal_health) = 'BAD' THEN\
                        UPDATE pet_sale\
                        SET SALEPRICE = SALEPRICE - (SALEPRICE * 0.25)\
                        WHERE ID = animal_id;\
                    ELSEIF UCASE(animal_health) = 'WORSE' THEN\
                        UPDATE pet_sale\
                        SET SALEPRICE = SALEPRICE - (SALEPRICE * 0.5)\
                        WHERE ID = animal_id;\
                    ELSE\
                        UPDATE pet_sale\
                        SET SALEPRICE = SALEPRICE\
                        WHERE ID = animal_id;\
                    END IF;\
                    SELECT *\
                    FROM pet_sale\
                    WHERE ID = animal_id;\
                END"\
            )
conn.commit()
print("Procedure created")


# Call procedure

try:
    asked_id = int(input("Animal ID you want to change the price to: "))
    health_status = input("Health condition (BAD-WORSE): ")
    cursor.callproc("update_saleprice", (asked_id, health_status))    
    df = pd.read_sql("SELECT *\
                    FROM pet_sale\
                    WHERE ID = {}".format(asked_id), conn)
    print(df)
except ValueError:
    print("ValueError")


cursor.close()
conn.close()
