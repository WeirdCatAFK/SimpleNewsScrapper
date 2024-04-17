from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup
import random, time, sqlite3


filterClasses = ["kicker-aside-back", "kicker"]


def deleteNewLines(text):
    return text.replace("\n", "")


def getHtmlText(url):
    try:
        driver = webdriver.Firefox()

        # Configurar el tiempo máximo de espera para cargar la página
        driver.set_page_load_timeout(20)

        # Abrir la URL en el navegador
        driver.get(url)

        # Simular el desplazamiento para cargar todo el contenido
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        start = time.time()
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Agregar retraso aleatorio entre 1 y 3 segundos antes de desplazarse nuevamente
            time.sleep(random.uniform(1, 3))
            newHeight = driver.execute_script("return document.body.scrollHeight")
            now = time.time()
            if newHeight == lastHeight or (now - start) >= 20:
                break
            lastHeight = newHeight
        html = driver.page_source
        # Parsear el HTML a un soup de bs4
        soup = BeautifulSoup(html, "html.parser")

        # Data filtering
        output = ""
        paragraphs = []
        for tag in soup.find_all(["p"]):

            if tag.parent.name not in ["head", "script"] and not any(
                cls in tag.get("class", []) for cls in filterClasses
            ):  # Exclude <head>, <script>, and elements with specific classes
                paragraphs.append(deleteNewLines(str(tag.text)))
        # Data processing
        for tag in paragraphs[0:20]:
            output += deleteNewLines(tag) + " "
        driver.quit()
        return output

    except (WebDriverException, TimeoutException) as e:
        driver.quit()
        print("Error:", e)
        return ""


def createDB(sqliteDB_Path: str, tableName: str):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS " + tableName + ";")
    cursor.execute(
        f'CREATE TABLE "{tableName}" (\n\t"id"\tINTEGER NOT NULL UNIQUE,\n\t"url"\tTEXT UNIQUE,\n\t"text"\tTEXT,\n\tPRIMARY KEY("id")\n);'
    )
    connection.commit()
    connection.close()


def writeTextToDB(sqliteDB_Path: str, tableName: str, entryText: str):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()

    # Verificar si el texto ya existe en la tabla
    cursor.execute(f"SELECT text FROM {tableName} WHERE text = ?", (entryText,))
    existing_data = cursor.fetchone()
    if existing_data:
        print(
            f"El texto '{entryText}' ya existe en la tabla. No se insertará nuevamente."
        )
    else:
        cursor.execute(
            f"INSERT INTO {tableName} (url, text) VALUES (?, ?)", (None, entryText)
        )
        print(f"El dato '{entryText}' se inserto exitosamente a la base de datos.")

    connection.commit()
    connection.close()


def getContentFromDB(sqliteDB_Path: str, tableName: str):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {tableName};")
    results = cursor.fetchall()

    connection.close()
    return results
