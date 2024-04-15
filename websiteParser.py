from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

def parseHTML(url):
    driver = webdriver.Chrome()
    
    # Abrir la URL en el navegador
    driver.get(url)
    
    # Simular el desplazamiento para cargar todo el contenido
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6)  # Esperar a que se cargue el contenido
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height
    
    # Obtener el HTML de la página después de cargar todo el contenido
    html = driver.page_source
    
    # Cerrar el navegador
    driver.quit()
    
    # Parsear el HTML utilizando BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def main():

    url = "https://www.ambasmanos.mx/nota-roja/capturan-a-cuatro-integrantes-de-los-monstruos-banda-dedicada-al-robo-de-camiones-de-carga/165105/"
    parsed_html = parseHTML(url)
    # Encontramos todos los contenedores con parrafos
    all_Paragraphs = parsed_html.find_all("p")
    
    for paragraph in all_Paragraphs:
        print(paragraph.text)
    
if __name__ == "__main__":
    main()
