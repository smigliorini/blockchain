import psycopg2
connection = psycopg2.connect(user = "deboni",
                                  password = "eth2004",
                                  host = "localhost" ,
                                  port = "5437 ",
                                  database = "ethdb")
with connection :
    with connection.cursor() as cursore :
        
        cursor.execute(
                """CREATE TABLE IF NOT EXISTS Tabella(
                    id INTEGER PRIMARY KEY,
                    importo Numeric );
                """)
        print(cursore.statusmessage)
connection.close()           
            

