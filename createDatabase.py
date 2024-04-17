import newsSearcher, webScrapper, os


def main():
    database = 'data.db'
    if not os.path.exists(database):
        with open(database,'w'):
            pass
    print(f'database {database} created successfully')
    
    # Determine our queries
    search_queries = [
    'Asaltos a camiones de carga en',
    'Robos a camiones de transporte de mercancías en',
    'Incidentes de robo a mano armada a camiones en',
    'Noticias sobre bandas criminales que roban camiones en',
    'Casos destacados de asaltos a camiones en zonas urbanas en',
    'Aumento de robos a camiones en',
    'Respuesta de las autoridades ante el aumento de asaltos a camiones en',
    'Impacto económico de los robos a camiones en la industria del transporte en',
    'Carreteras Peligrosas en',
    'Robos a mano armada en carreteras principales en',
    'Casos de secuestros exprés en carreteras transitadas en',
    'Falsos retenes en',
    'Incidentes de vandalismo en vehículos en',
    'Asaltos a camiones de carga durante la noche en',
    'Robos a camiones de transporte de mercancías durante el día en',
    'Incidentes de robo a mano armada a camiones en autopistas en',
    'Noticias sobre bandas criminales que roban camiones en áreas rurales en',
    'Casos destacados de asaltos a camiones en zonas industriales en',
    'Aumento de robos a camiones en áreas metropolitanas en',
    'Respuesta de las autoridades ante el aumento de asaltos a camiones en regiones fronterizas en',
    'Impacto económico de los robos a camiones en la cadena de suministro en',
    'Carreteras Peligrosas en días festivos en',
    'Robos a mano armada en carreteras secundarias en días laborables en',
    'Casos de secuestros exprés en carreteras aisladas en fines de semana en',
    'Falsos retenes en áreas de construcción en',
    'Incidentes de vandalismo en vehículos de carga en',
    'Asaltos a camiones de carga con violencia en',
    'Robos a camiones de transporte de mercancías con intimidación en',
    'Incidentes de robo a mano armada a camiones con toma de rehenes en',
    'Noticias sobre bandas criminales que roban camiones con armas de fuego en',
    'Casos destacados de asaltos a camiones en áreas de descanso en']  # Your list of search queries
    
    # Initialize an empty list to store all news
    all_the_news = []
    
    # Create the search results table in the database
    newsSearcher.writeResultsToDatabase(database, 'searchResults', [])
    
    # Batch size for fetching news URLs
    batch_size = 10
    
    # Fetch news URLs for each query and process them in batches
    for query in search_queries:
        # Fetch news URLs for the current query
        news_urls = newsSearcher.getSearchResults(query)
        
        # Write the current batch of news URLs to the database
        newsSearcher.writeResultsToDatabase(database, 'searchResults', news_urls)
        
        #Create the table where we will store our content
        webScrapper.createDB(database,'content')
        
        # Process news URLs in batches
        for i in range(0, len(news_urls), batch_size):
            batch_urls = news_urls[i:i + batch_size]
            print(f"Processing batch {i // batch_size + 1} of {len(news_urls) // batch_size + 1}")
            for news_url in batch_urls:
                print(f"Retrieving {news_url} from database")
                # Fetch and write the content of the current news URL to the database
                webScrapper.writeTextToDB(database, 'content', webScrapper.getHtmlText(str(news_url)))
                # Append the news URL to the list of all news
                all_the_news.append(news_url)
    
    # Confirm that the data is in the database
    urls = newsSearcher.getResultsFromDatabase(database, 'searchResults')
    print("Total news URLs retrieved:", len(urls))

if __name__ == "__main__":
    main()

