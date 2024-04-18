import time, sqlite3, math, random

from selenium import webdriver
from bs4 import BeautifulSoup

driver_path = None


def set_DriverPath(path:str):
    global driver_path
    driver_path = path

def getSearchResults(query: str) -> list:
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


    options.binary_location = brave_path
    driver = webdriver.Chrome(options = options)
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

def createDB(sqliteDB_Path: str, tableName: str):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS " + tableName + ";")
    cursor.execute(f"CREATE TABLE \"{tableName}\" (\n"
                   "\t\"id\" INTEGER NOT NULL UNIQUE,\n"
                   "\t\"urls\" TEXT UNIQUE,\n"
                   "\tPRIMARY KEY(\"id\" AUTOINCREMENT)\n"
                   ");")
    
    connection.commit()
    connection.close()
    
def insertDataIntoDatabase(sqliteDB_Path: str, tableName: str, data: list):
    connection = sqlite3.connect(sqliteDB_Path)
    cursor = connection.cursor()
    
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
                print(f"El dato '{content}' se insertó exitosamente en la base de datos.")
        
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
