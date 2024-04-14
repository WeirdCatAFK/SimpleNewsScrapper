from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import json
import csv
import os

def getSearchResults(query: str) -> list:
    driver = webdriver.Chrome()

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
    soup.findAll("a")
    return soup

def create_search_results_folder():
    if not os.path.exists(".gitignore/searchResults"):
        os.makedirs(".gitignore/searchResults")

def writeSearchResultsJSON(query: str):
    create_search_results_folder()
    soup = getSearchResults(query)
    # Encontramos todos los contenedores con hrefs y guardamos todos los valores en un diccionario
    results = soup.find_all("a")
    output_data = {"urlNoticias": []}
    for element in results:
        href = str(element.get("href"))
        if href.startswith("https://"):
            output_data["urlNoticias"].append(href)
    # Escribimos en un JSON
    with open(".gitignore/searchResults/output.json", "w", encoding="utf-8") as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)


def writeSearchResultsCSV(query: str):
    create_search_results_folder()
    soup = getSearchResults(query)
    # Encontramos todos los contenedores con hrefs
    # Se abre primero el archivo para no estar abriendolo y cerrandolo pq vamos a escribir varias veces en el
    with open(".gitignore/searchResults/output.csv", "w", encoding="utf-8") as file:
        results = soup.find_all("a")
        for element in results:
            href = str(element.get("href"))
            if href.startswith("https://"):
                file.write(href + ",\n")


def defaultJSON():
    create_search_results_folder()
    # Crea un archivo JSON vacío
    with open(".gitignore/searchResults/output.json", "w", encoding="utf-8") as file:
        json.dump({}, file)


def defaultCSV():
    create_search_results_folder()
    # Crea un archivo CSV vacío con encabezados
    with open(
        ".gitignore/searchResults/output.csv", "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["url"])  # Encabezado


def main():
    writeSearchResultsJSON('Clima')

if __name__ == "__main__":
    main()
