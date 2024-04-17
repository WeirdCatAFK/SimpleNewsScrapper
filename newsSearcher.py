import time, sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup


def getSearchResults(query: str) -> BeautifulSoup:
    driver = webdriver.Firefox()

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
    html = driver.page_source

    # Cerrar el navegador
    driver.quit()

    # Parsear el HTML utilizando BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    link = soup.find_all('a')
    results =[]
    for element in link:
        href = str(element.get("href"))
        if href.startswith("https://"):
            results.append(str(href))
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
    
    for content in data:
        # Verificar si el contenido ya existe en la tabla
        cursor.execute(f"SELECT urls FROM {tableName} WHERE urls = ?", (content,))
        existing_data = cursor.fetchone()
        if existing_data:
            print(f"El dato '{content}' ya existe en la tabla. No se insertará nuevamente.")
        else:
            cursor.execute(f"INSERT INTO {tableName}(urls) VALUES (?)", (content,))
            print(f"El dato '{content}' se inserto exitosamente a la base de datos.")

    
    connection.commit()
    connection.close()
def getResultsFromDatabase(sqliteDB_Path: str, tableName: str):
    import sqlite3
    
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {tableName};")
    results = cursor.fetchall()

    connection.close()

    return results
