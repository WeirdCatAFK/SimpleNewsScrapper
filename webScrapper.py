from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup
import random, time, sqlite3, re


filterClasses = ["kicker-aside-back", "kicker"]

driver_path = None

def set_DriverPath(path:str):
    global driver_path
    driver_path = path


def depurer(text):
    # Function to remove newlines
    def deleteNewLines(text):
        return text.replace("\n", "")

    # Remove newlines
    text = deleteNewLines(text)
    
    # Remove anything between curly braces
    text = re.sub(r'\{[^\}]*\}', '', text)
    
    # Remove anything between square brackets
    text = re.sub(r'\[[^\]]*\]', '', text)
    
    return text


def getHtmlText(url):
    try:
        global driver_path
        brave_path = driver_path
        options = webdriver.ChromeOptions()
        options.add_argument('--enable-chrome-browser-cloud-management')
        options.add_argument(    "--disable-extensions")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--ignore-certificate-errors")
        user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4896.79 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4896.79 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15; rv:101.0) Gecko/20100101 Firefox/101.0"
    ]

    # Randomly select a user-agent string from the list
        random_user_agent = random.choice(user_agents)

        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={random_user_agent}")
        option = webdriver.ChromeOptions()

        option.binary_location = brave_path
        driver = webdriver.Chrome(options = option)


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
            if newHeight == lastHeight or (now - start) >= 60:
                break
            lastHeight = newHeight

        # Parsear el HTML a un soup de bs4 directamente desde el navegador
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Data filtering and processing
        output = ""
        paragraphs_count = 0
        for tag in soup.find_all(["p"]):
            if tag.parent.name not in ["head", "script"] and not any(
                cls in tag.get("class", []) for cls in filterClasses
            ):  # Exclude <head>, <script>, and elements with specific classes
                text = depurer(str(tag.text))
                output += text + " "
                paragraphs_count += 1
                if paragraphs_count >= 20:
                    break

        driver.quit()
        return output

    except (WebDriverException, TimeoutException) as e:
        if 'driver' in locals() and driver:
            driver.quit()
        print("Error:", e)
        return ""


def createDB(sqliteDB_Path: str, tableName: str):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS " + tableName + ";")
    cursor.execute(
        f'CREATE TABLE "{tableName}" (\n\t"id"\tINTEGER NOT NULL UNIQUE,\n\t"url"\tTEXT UNIQUE,\n\t"text"\tTEXT,\n\t"analisis"\tTEXT,\n\tPRIMARY KEY("id")\n);'
    )
    connection.commit()
    connection.close()



def writeTextToDB(sqliteDB_Path: str, tableName: str, url: str, entryText: str):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"INSERT INTO {tableName} (url, text) VALUES (?, ?)", (url, entryText)
        )
        print(f"El dato '{entryText}' se insertó exitosamente a la base de datos.")
    except sqlite3.IntegrityError:
        print(f"El URL '{url}' ya existe en la tabla. No se insertará nuevamente.")

    connection.commit()
    connection.close()


def getContentFromDB(sqliteDB_Path: str, tableName: str):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {tableName};")
    results = cursor.fetchall()

    connection.close()
    return results