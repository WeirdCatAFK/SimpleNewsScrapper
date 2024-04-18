import newsSearcher
import webScrapper
import os


def main():
    newsSearcher.set_DriverPath(
        r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    )  # Tu path de tu ejecutable de brave
    webScrapper.set_DriverPath(
        r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    )  # Tu path de tu ejecutable de brave

    database = "data.db"  # El nombre de tu base de datos de salida
    if not os.path.exists(database):
        with open(database, "w"):
            pass
    print(f"database {database} created successfully")
    
    # Create the table where we will store our content
    webScrapper.createDB(database, "content")
    newsSearcher.createDB(database, "searchResults")
    # Determine our queries
    search_queries = [
        "Asalto a camiones en",
        "Carreteras asaltos",
        "Violencia a conductores",
        "Robo de mercancia a camiones de carga",
        "Saqueo a camiones de carga",
        "Riesgos para camiones en",
        "Rutas peligrosas para transitar",
        "Aumento a asaltos a camiones en",
        "Carreteras peligrosas Mexico",
        "Robos y asaltos en carreteras en",
        "Peligros carretera",
        "Seguridad en carreteras en",
        "Incremento a la delincuencia en carreteras",
        "Robos y asaltos en vehículos en",
        "Crimenes en autopistas",
        "Peligros a camiones en áreas rurales en",
        "Peligros a transportistas",
        "Robo de mercancia en zonas metropolitanas",
        "Autopistas peligrosas en zonas metropolitanas",
        "Robos en gasolineras",
        "Peligros en carreteras durante días festivos en",
        "Riesgos de seguridad en carreteras secundarias en",
        "Desviamientos peligroso",
        "Asi operan las bandas delitctivas que roban camiones de carga",
        "Problemas en vehículos de carga en",
        "Delitos violentos contra camiones en",
        "Amenazas de seguridad para camiones en",
        "Crimen organizado contra camiones en",
        "Incidencias criminales en áreas de descanso en",
    ]

    # Initialize an empty list to store all news
    all_the_news = []

    # Batch size for fetching news URLs
    batch_size = 5

    # Fetch news URLs for each query and process them in batches
    for query in search_queries:
        # Fetch news URLs for the current query
        news_urls = newsSearcher.getSearchResults(query)

        # Write the current batch of news URLs to the database
        newsSearcher.insertDataIntoDatabase(database, "searchResults", news_urls)

    # Process news URLs in batches
    for i in range(0, len(news_urls), batch_size):
        batch_urls = news_urls[i : i + batch_size]
        print(
            f"Processing batch {i // batch_size + 1} of {len(news_urls) // batch_size + 1}"
        )
        for news_url in batch_urls:
            print(f"Retrieving {news_url} from database")
            # Fetch and write the content of the current news URL to the database
            webScrapper.writeTextToDB(
                database, "content", str(news_url), webScrapper.getHtmlText(news_url)
            )
            # Append the news URL to the list of all news
            all_the_news.append(news_url)

        # Close database connection after processing each batch
        webScrapper.getContentFromDB(database, "content")
    # Confirm that the data is in the database
    urls = newsSearcher.getResultsFromDatabase(database, "searchResults")
    print("Total news URLs retrieved:", len(urls))


if __name__ == "__main__":
    main()
