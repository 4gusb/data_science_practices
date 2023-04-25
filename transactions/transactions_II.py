import mysql.connector
import pandas as pd


# CONNECTION
try:
    conn = mysql.connector.connect(user=root, password=password,
                                    host=host, 
                                    database=database,
                                    port=port)
    cursor = conn.cursor()
    print("MySQL Database connection successful")
except:
    print("Error")

df = pd.read_sql("SELECT * FROM shoe_shop", conn)
print(df)

# First transaction 
# Buys James four pair of trainers. Then attempt to buy James a pair of Brogues.

# Drop procedure in case it exists

cursor.execute("DROP PROCEDURE IF EXISTS james_transaction")
print("Procedure dropped")

cursor.execute("CREATE PROCEDURE james_transaction()\
                BEGIN\
                    DECLARE `rollback` BOOL DEFAULT 0;\
                    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION\
                        SET `rollback` = 1;\
                    \
                    START TRANSACTION;\
                    \
                    UPDATE bank_accounts\
                    SET Balance = Balance - 1200\
                    WHERE AccountName = 'James';\
                    \
                    UPDATE bank_accounts\
                    SET Balance = Balance + 1200\
                    WHERE AccountName = 'Shoe Shop';\
                    \
                    UPDATE shoe_shop\
                    SET Stock = Stock - 4\
                    WHERE Product = 'Trainers';\
                    \
                    UPDATE bank_accounts\
                    SET Balance = Balance - 150\
                    WHERE AccountName = 'James';\
                    \
                    UPDATE bank_accounts\
                    SET Balance = Balance + 150\
                    WHERE AccountName = 'Shoe Shop';\
                    \
                    UPDATE shoe_shop\
                    SET Stock = Stock - 4\
                    WHERE Product = 'Brogues';\
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
print("Stored Procedure created")

# Call procedure

cursor.execute("CALL james_transaction")

# Show results 

accounts = pd.read_sql("SELECT *\
                FROM bank_accounts"\
                , conn)
print(accounts)

shop = pd.read_sql("SELECT *\
                FROM shoe_shop"\
                , conn)
print(shop)

# As a result, no change was made due an exception with the Brogues purchase.

--
