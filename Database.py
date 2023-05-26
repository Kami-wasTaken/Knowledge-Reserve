import mysql.connector

db = mysql.connector.connect(
    host="brbjmpkm2lgsjfy1lfhx-mysql.services.clever-cloud.com",
    user="ukc8u9srhpdpi6qv",
    passwd="VPG7dB5QxCWQvMyUaWIw",
    database="brbjmpkm2lgsjfy1lfhx"
)

mycursor = db.cursor()


#mycursor.execute("CREATE TABLE booksavailable (username VARCHAR(255), bookslot1 VARCHAR(255), bookslot2 VARCHAR(255), bookslot3 VARCHAR(255))")
#mycursor.execute("CREATE TABLE books (bookname VARCHAR(255), authorname VARCHAR(255), publishername VARCHAR(255))")
#mycursor.execute("CREATE TABLE accounts (email VARCHAR(255), password VARCHAR(255), username VARCHAR (255))")
#mycursor.execute("DELETE FROM booksavailable")
#mycursor.execute("INSERT INTO books(bookname, authorname, publishername) VALUES ('Life Science (Holt Science And Technology)', 'Holt Rinehart & Winston', 'Holt Rinehart & Winston')")
#mycursor.execute("SELECT email FROM accounts")
#myresult = mycursor.fetchall()

#mycursor.execute("SELECT email FROM accounts")


#result = mycursor.fetchall()
#if ('Email',) in result:
 #  print("exists")
   
#print('Email',)
#print(result)

db.commit()