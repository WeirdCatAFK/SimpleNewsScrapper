import newsSearcher
import websiteParser
import csv


def main():
    news = []
    newsSearcher.defaultCSV()
    # Las queries con las que buscaremos nuestras news
    searchQueries = [
        "Asalto de camiones en",
    ]
    # Normalizamos el archivo donde se generan los resultados
    newsSearcher.defaultCSV()

    # Conseguimos las news
    for querie in searchQueries:
        newsSearcher.writeSearchResultsCSV(querie)

    # Eliminamos los duplicados
    newsSearcher.eliminateDuplicatesCSV("output/searchResults/searchResults.csv")
    
    # Abre el archivo CSV en modo lectura
    with open("output/searchResults/searchResults.csv", newline="") as csvfile:
        datosCSV = csv.reader(csvfile)
        for linea in datosCSV:
            news.append(str(linea[0]))
            print(linea[0])
            
    websiteParser.writeToCSV(news, "output/content.csv")

if __name__ == "__main__":
    main()
