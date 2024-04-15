from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup


def getHtmlText(url):
    driver = webdriver.Chrome()

    # Abrir la URL en el navegador
    driver.get(url)

    # Simular el desplazamiento para cargar todo el contenido
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6)  # Esperar a que se cargue el contenido
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == lastHeight:
            break
        lastHeight = new_height
    
    # Obtener el HTML de la página después de cargar todo el contenido
    html = driver.page_source
    driver.quit()
    # Parsear el HTML utilizando BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    # Encontramos todos los contenedores con parrafos
    all_Paragraphs = soup.find_all("p")
    output = ""
    for paragraph in all_Paragraphs:
        output += str(paragraph.text) + " "

    return output


def main():
    print(
        getHtmlText(
            "https://www.abc.es/cultura/musica/instrumentos-musicales/"
        )
    )


if __name__ == "__main__":
    main()
