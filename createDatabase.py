import newsSearcher
import websiteParser
import csv


def main():
    
    newsSearcher.defaultCSV()
    # Las queries con las que buscaremos nuestras noticias
    searchQueries = [
        "Premios escolares en",
    ]
    # Normalizamos el archivo donde se generan los resultados
    newsSearcher.defaultCSV()

    # Conseguimos las noticias
    for querie in searchQueries:
        newsSearcher.writeSearchResultsCSV(querie)

    # Eliminamos los duplicados
    newsSearcher.eliminateDuplicatesCSV("output\searchResults\searchResults.csv")
    # Nombre del archivo CSV a abrir
    
    newsCSV = "output\searchResults\searchResults.csv"
    noticias = []

    # Abre el archivo CSV en modo lectura
    with open(newsCSV, newline="") as csvfile:
        # Crea un lector CSV
        datosCSV = csv.reader(csvfile)

        # Itera sobre cada línea del archivo
        for linea in datosCSV:
            # Haz algo con cada línea, por ejemplo, imprimir
            noticias.append(str(linea[0]))
            print(linea[0])
    websiteParser.writeToCSV(noticias, "output\searchResults\content.csv")


if __name__ == "__main__":
    main()
