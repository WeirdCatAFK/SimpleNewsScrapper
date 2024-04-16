from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException
from bs4 import BeautifulSoup
import csv, random, time

def deleteNewLines(text):
    return text.replace("\n", "")


filterClasses = ["kicker-aside-back", "kicker"]

def getHtmlText(url):
    try:
        driver = webdriver.Firefox()

        # Configurar el tiempo máximo de espera para cargar la página
        driver.set_page_load_timeout(5)

        # Abrir la URL en el navegador
        driver.get(url)

        # Simular el desplazamiento para cargar todo el contenido
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Agregar retraso aleatorio entre 1 y 3 segundos antes de desplazarse nuevamente
            time.sleep(random.uniform(1, 3))
            newHeight = driver.execute_script("return document.body.scrollHeight")
            
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
        
        # Obtener el HTML de la página después de cargar todo el contenido
        html = driver.page_source
        
        # Parsear el HTML a un soup de bs4
        soup = BeautifulSoup(html, "html.parser")
        
        # Data filtering
        output = ""
        paragraphs = []
        for tag in soup.find_all(["p"]):
            
            if tag.parent.name not in ['head', 'script'] and not any(cls in tag.get('class', []) for cls in filterClasses):  # Exclude <head>, <script>, and elements with specific classes
                paragraphs.append(deleteNewLines(str(tag.text)))
        #Data processing 
        for tag in paragraphs[0:20]:    
            output += deleteNewLines(tag) + " "
        driver.quit()
        print(output)
        return output
    
    except (WebDriverException, TimeoutException) as e:
        driver.quit()
        print("Error:", e)
        return ""


def writeToCSV(urls: list, filename: str):
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL', 'Text'])
        for url in urls:
            text = getHtmlText(url)
            writer.writerow([url, text])