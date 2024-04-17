import time, sqlite3

from selenium import webdriver
from bs4 import BeautifulSoup




def getSearchResults(query: str) -> list:
    driver = webdriver.Firefox()

    try:
        # Abrir la URL en el navegador
        driver.get("https://www.bing.com/news/search?q=" + query)

        # Simular el desplazamiento para cargar todo el contenido
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Esperar a que se cargue el contenido
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

        # Obtener el HTML de la página después de cargar todo el contenido
        soup = BeautifulSoup(driver.page_source, "html.parser")

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
        
        
def getResultsFromDatabase(sqliteDB_Path: str, tableName: str):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {tableName};")
    results = cursor.fetchall()

    connection.close()

    return results
