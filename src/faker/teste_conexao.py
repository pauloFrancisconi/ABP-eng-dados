import pyodbc

server = '' # Ex: 'localhost\\SQLEXPRESS' ou '192.168.1.10'
database = '' # Ex: 'MeuBanco'
username = '' # Ex: 'sa'
password = '' # Ex: '123456'
driver = '' # Nome do driver instalado

try:
    
    conn_str = f"""
        DRIVER={driver};
        SERVER={server};
        DATABASE={database};
        UID={username};
        PWD={password};
        TrustServerCertificate=yes;
    """
    connection = pyodbc.connect(conn_str)
    print("Conexão bem-sucedida com o SQL Server")

    cursor = connection.cursor()
    cursor.execute("SELECT GETDATE();")
    row = cursor.fetchone()
    print("Data/hora do servidor:", row[0])

    connection.close()

except Exception as e:
    print("Falha na conexão:")
    print(e)
