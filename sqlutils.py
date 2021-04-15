import mysql.connector

def cria_server(host,usuario,senha,bd):
    return mysql.connector.connect(
            host=host,
            user=usuario,
            password=senha,
            database=bd
        )
