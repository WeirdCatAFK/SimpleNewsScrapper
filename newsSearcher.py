import os
import time
import json
import csv
from selenium import webdriver
from bs4 import BeautifulSoup


def getSearchResults(query: str) -> BeautifulSoup:
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
    return soup





def checkOrCreate_SystemFolders(pathName: str = "output/searchResults"):
    if not os.path.exists(pathName):
        os.makedirs(pathName)






def writeSearchResultsJSON(
    query: str, outPath="output/searchResults/searchResults.json"
):
    checkOrCreate_SystemFolders()
    soup = getSearchResults(query)

    # Encontramos todos los contenedores con hrefs y guardamos todos los valores en un diccionario
    results = soup.find_all("a")
    output_data = {"urlNoticias": []}
    for element in results:
        href = str(element.get("href"))
        if href.startswith("https://"):
            output_data["urlNoticias"].append(href)

    # Leemos el archivo JSON existente, si existe
    try:
        with open(outPath, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {"urlNoticias": []}

    # Agregamos los nuevos datos al diccionario existente
    existing_data["urlNoticias"].extend(output_data["urlNoticias"])

    # Escribimos el diccionario actualizado en el JSON
    with open(outPath, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)







def writeSearchResultsCSV(query: str, outPath = "output/searchResults/searchResults.csv"):
    checkOrCreate_SystemFolders()
    soup = getSearchResults(query)
    # Encontramos todos los contenedores con hrefs
    # Se abre primero el archivo para no estar abriendolo y cerrandolo pq vamos a escribir varias veces en el
    with open(outPath, "a", encoding="utf-8") as file:
        results = soup.find_all("a")
        for element in results:
            href = str(element.get("href"))
            if href.startswith("https://"):
                file.write(href + "\n")


def defaultJSON(outPath ="output/searchResults/searchResults.json"):
    checkOrCreate_SystemFolders()
    defaultJSON = {"results": None}
    # Crea un archivo JSON vacío
    with open(outPath, "w", encoding="utf-8") as file:
        json.dump(defaultJSON, file)


def defaultCSV(outPath ="output/searchResults/searchResults.csv"):
    checkOrCreate_SystemFolders()
    # Crea un archivo CSV vacío con encabezados
    with open(
        outPath, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)


def eliminateDuplicatesCSV(fileName: str):
    with open(fileName, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        seen = set()
        for line in lines:
            if line not in seen:
                seen.add(line)
                file.write(line)
        file.truncate()


def main():
    # Más que nada pruebas
    eliminateDuplicatesCSV("output\searchResults\searchResults.csv")


if __name__ == "__main__":
    main()
