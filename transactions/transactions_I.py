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


# ----------------------------------------------------------------
#TABLES CREATION

# Creation of shop table

# Drop the table in case it exists

cursor.execute("DROP TABLE shoe_shop")
print("Table dropped")


# Create the table

cursor.execute("CREATE TABLE shoe_shop (\
                product VARCHAR(25) NOT NULL,\
                stock INTEGER NOT NULL,\
                price DECIMAL(8,2) CHECK(Price>0) NOT NULL,\
                PRIMARY KEY (Product))")
print("Table created")
conn.commit()


# Insert sample data into the table
    
cursor.execute("INSERT INTO shoe_shop VALUES\
                ('Boots',11,200),\
                ('High heels',8,600),\
                ('Brogues',10,150),\
                ('Trainers',14,300)")
print("Values added")
conn.commit()


# Retrieve all records from the table

# df = pd.read_sql("SELECT * FROM shoe_shop", conn)
# print(df)


# Creation of Bank Table

# Drop the table in case it exists

cursor.execute("DROP TABLE bank_accounts")
print("Table dropped")


# Create the table

cursor.execute("CREATE TABLE bank_accounts (\
                AccountNumber VARCHAR(5) NOT NULL,\
                AccountName VARCHAR(25) NOT NULL,\
                Balance DECIMAL(8,2) CHECK(Balance>=0) NOT NULL,\
                PRIMARY KEY (AccountNumber))")
print("Table created")
conn.commit()


# Insert sample data into the table
    
cursor.execute("INSERT INTO bank_accounts VALUES\
                ('B001','Rose',300),\
                ('B002','James',1345),\
                ('B003','Shoe Shop',124200),\
                ('B004','Corner Shop',76000)")
print("Values added")
conn.commit()


# Retrieve all records from the table

# df = pd.read_sql("SELECT * FROM bank_accounts", conn)
# print(df)


# ----------------------------------------------------------------
# PROCEDURE AND TRANSACTION


# Drop procedure in case it exists

cursor.execute("DROP PROCEDURE transaction")
print("Procedure dropped")

# Starts procedure
# The procedure will manage the exceptions in case of error, the transaction is nested.

cursor.execute("CREATE PROCEDURE transaction()\
                BEGIN\
                    DECLARE `rollback` BOOL DEFAULT 0;\
                    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION\
                        SET `rollback` = 1;\
                        \
                        START TRANSACTION;\
                        \
                        UPDATE bank_accounts\
                        SET Balance = Balance - 200\
                        WHERE AccountName = 'Rose';\
                        \
                        UPDATE bank_accounts\
                        SET Balance = Balance + 200\
                        WHERE AccountName = 'Shoe Shop';\
                        \
                        UPDATE shoe_shop\
                        SET Stock = Stock - 1\
                        WHERE Product = 'Boots';\
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
conn.commit()
# print("Procedure created")

# Call procedure

cursor.execute("CALL transaction")


#Show results 

accounts = pd.read_sql("SELECT *\
                FROM bank_accounts"\
                , conn)
print(accounts)

shop = pd.read_sql("SELECT *\
                FROM shoe_shop"\
                , conn)
print(shop)

# As a result, it can be visualized that the number of boots stock has decreased and Rose's balance gotten lower. 


# ----------------------------------------------------------------
# SECOND TRY OF PROCEDURE AND TRANSACTION


# Drop procedure because it already exists

cursor.execute("DROP PROCEDURE transaction")
print("Procedure dropped")


# Starts procedure
# Now, the exact same work will be executed plus another purchase attempt, which will raise an exception due Rose's insufficient funds.

cursor.execute("CREATE PROCEDURE transaction()\
                BEGIN\
                    DECLARE `rollback` BOOL DEFAULT 0;\
                    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION\
                        SET `rollback` = 1;\
                        \
                        START TRANSACTION;\
                        \
                        UPDATE bank_accounts\
                        SET Balance = Balance - 200\
                        WHERE AccountName = 'Rose';\
                        \
                        UPDATE bank_accounts\
                        SET Balance = Balance + 200\
                        WHERE AccountName = 'Shoe Shop';\
                        \
                        UPDATE shoe_shop\
                        SET Stock = Stock - 1\
                        WHERE Product = 'Boots';\
                        \
                        UPDATE bank_accounts\
                        SET Balance = Balance - 300\
                        WHERE AccountName = 'Rose';\
                        \
                        UPDATE bank_accounts\
                        SET Balance = Balance + 300\
                        WHERE AccountName = 'Shoe Shop';\
                        \
                        UPDATE shoe_shop\
                        SET Stock = Stock - 1\
                        WHERE Product = 'Trainers';\
                        \
                        IF `rollback` THEN\
                            ROLLBACK;\
                        ELSE\
                            COMMIT;\
                        END IF;\
                    \
                END"
            )
conn.commit()
print("Procedure created")


# Call procedure

cursor.execute("CALL transaction")


# Show results 

accounts = pd.read_sql("SELECT *\
                FROM bank_accounts"\
                , conn)
print(accounts)

shop = pd.read_sql("SELECT *\
                FROM shoe_shop"\
                , conn)
print(shop)


# Here no data was modified since there was at least one exception during this transaction.

cursor.close()
conn.close()

--
