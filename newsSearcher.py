import time, sqlite3, math

from selenium import webdriver
from bs4 import BeautifulSoup


driver_path = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"


def getSearchResults(query: str) -> list:
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

    option = webdriver.ChromeOptions()

    option.binary_location = brave_path
    driver = webdriver.Chrome(options = option)
    try:
        # Abrir la URL en el navegador
        driver.get("https://www.bing.com/news/search?q=" + query)

        # Simular el desplazamiento para cargar todo el contenido
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Esperar a que se cargue el contenido
            new_height = driver.execute_script("return document.body.scrollHeight")
        # Simular el desplazamiento para cargar todo el contenido
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Esperar a que se cargue el contenido
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height
            if new_height == last_height:
                break
            last_height = new_height

        # Obtener el HTML de la página después de cargar todo el contenido
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Obtener el HTML de la página después de cargar todo el contenido
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Encontrar todos los enlaces y filtrar solo los que comienzan con "https://"
        links = soup.find_all('a')
        results = [str(link.get("href")) for link in links if str(link.get("href")).startswith("https://")]
    finally:
        # Cerrar el navegador
        driver.quit()
        # Encontrar todos los enlaces y filtrar solo los que comienzan con "https://"
        links = soup.find_all('a')
        results = [str(link.get("href")) for link in links if str(link.get("href")).startswith("https://")]
    finally:
        # Cerrar el navegador
        driver.quit()

    return results

    
def writeResultsToDatabase(sqliteDB_Path: str, tableName: str, data: list):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS " + tableName + ";")
    cursor.execute(f"CREATE TABLE \"{tableName}\" (\n"
                   "\t\"id\" INTEGER NOT NULL UNIQUE,\n"
                   "\t\"urls\" TEXT UNIQUE,\n"
                   "\tPRIMARY KEY(\"id\" AUTOINCREMENT)\n"
                   ");")
    
    try:
        # Iniciar transacción
        cursor.execute("BEGIN TRANSACTION;")
        
        for content in data:
            # Verificar si el contenido ya existe en la tabla
            cursor.execute(f"SELECT COUNT(*) FROM {tableName} WHERE urls = ?", (content,))
            existing_count = cursor.fetchone()[0]
            if existing_count > 0:
                print(f"El dato '{content}' ya existe en la tabla. No se insertará nuevamente.")
            else:
                cursor.execute(f"INSERT INTO {tableName}(urls) VALUES (?)", (content,))
                print(f"El dato '{content}' se inserto exitosamente a la base de datos.")
        
        # Finalizar transacción
        connection.commit()
    except Exception as e:
        # Revertir la transacción en caso de error
        print("Error:", e)
        connection.rollback()
    finally:
        connection.close()
        
        
    
    try:
        # Iniciar transacción
        cursor.execute("BEGIN TRANSACTION;")
        
        for content in data:
            # Verificar si el contenido ya existe en la tabla
            cursor.execute(f"SELECT COUNT(*) FROM {tableName} WHERE urls = ?", (content,))
            existing_count = cursor.fetchone()[0]
            if existing_count > 0:
                print(f"El dato '{content}' ya existe en la tabla. No se insertará nuevamente.")
            else:
                cursor.execute(f"INSERT INTO {tableName}(urls) VALUES (?)", (content,))
                print(f"El dato '{content}' se inserto exitosamente a la base de datos.")
        
        # Finalizar transacción
        connection.commit()
    except Exception as e:
        # Revertir la transacción en caso de error
        print("Error:", e)
        connection.rollback()
    finally:
        connection.close()
        
        
def getResultsFromDatabase(sqliteDB_Path: str, tableName: str):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {tableName};")
    results = cursor.fetchall()

    connection.close()

    return results

def distributeDataEqually(sqliteDB_Path, tableName: str, num_files: int):
    try:
        # Connect to the original database
        conn = sqlite3.connect(sqliteDB_Path)
        cursor = conn.cursor()

        # Retrieve data from the original database
        cursor.execute(f"SELECT * FROM {tableName}")
        data = cursor.fetchall()

        # Split the data into equal parts
        chunk_size = math.ceil(len(data) / num_files)
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        # Write each chunk to a new database file
        for i, chunk in enumerate(chunks):
            new_sqliteDB_Path = f"database_part_{i}.db"
            conn_new = sqlite3.connect(new_sqliteDB_Path)
            cursor_new = conn_new.cursor()

            # Create a table with the same schema as the original
            cursor_new.execute(f"CREATE TABLE IF NOT EXISTS {tableName} (id INTEGER NOT NULL UNIQUE, urls TEXT UNIQUE, PRIMARY KEY(id AUTOINCREMENT))")

            # Insert data into the new table
            for row in chunk:
                try:
                    cursor_new.execute("INSERT INTO YourTableName (urls) VALUES (?)", (row[1],))
                except sqlite3.IntegrityError:
                    print(f"Skipping duplicate entry: {row[1]}")

            conn_new.commit()
            conn_new.close()

        print(f"Data distributed equally among {num_files} new database files.")

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        conn.close()
