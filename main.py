import os
import pyodbc

PATH_TO_PROJECT= r'C:\Users\KennethLindalen\RiderProjects\Kenneth\Fagmann\Fagmann\Migrations'
PRODUCT_VERSION = '8.0.8'


conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=tcp:rokeagruppensqlserver.database.windows.net,1433;"
    "DATABASE=FagmannDB;"
    "UID=Fagmann_write;"
    "PWD=Dreamer123!;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

cursor = conn.cursor()
cursor.execute("SELECT @@version;")
row = cursor.fetchone()
while row:
    print(row[0])
    row = cursor.fetchone()

def insert_into_database(table, field_list, values):    
    sql = f"INSERT INTO {table} ({', '.join(field_list)}) VALUES ({', '.join(['?']*len(field_list))})"
    cursor.execute(sql, values)
    conn.commit()



def parse_filename(filename):
    fileArr = filename.split('_')
    file_id = fileArr[0]
    file_name = '_'.join(fileArr[1:])
    return file_id, file_name

for filename in os.listdir(PATH_TO_PROJECT):
    if not filename[0].isdigit() or ".Designer.cs" in filename:
        continue
    
    filename = filename.replace('.cs','')
    print(filename)
    
    insert_into_database("_EFMigrationHistory", ["MigrationId", "ProductVersion"], [filename, PRODUCT_VERSION])
    
    