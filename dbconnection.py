import sqlite3


def connection(query):
    con = sqlite3.connect('imdb.db', timeout=10)
    cur = con.cursor()

    # Create table
    try:
        if type(query) == tuple:  # For insert query
            con.execute(*query)
        else:
            con.execute(query)  # For select query
        con.commit()

    # cur.execute('''CREATE TABLE stocks
    #                (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    # cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes


    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    except sqlite3.Error as error:
        print(error)
    finally:
        con.close()