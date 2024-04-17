import newsSearcher, webScrapper, os


def main():
    database = 'data.db'
    if not os.path.exists(database):
        with open(database,'w') as f:
            pass
    print(f'database {database} created sucessfully')
    
    #Determinamos nuestras querys
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
    'Casos destacados de asaltos a camiones en áreas de descanso en'
]
    
    
    #Creamos donde vamos a guardar las noticias finales
    allTheNews = []
    #Iteramos para conseguir todas las noticias de cada petición
    for query in search_queries:
        allTheNews.append(newsSearcher.getSearchResults(query))
    
    
    #Escribimos los resultados a la base de datos
    newsSearcher.writeResultsToDatabase(database,'searchResults',allTheNews)
    #Confirmamos que los datos estan en la base de datos
    urls = newsSearcher.getResultsFromDatabase(database,'searchResults')
    

    #Creamos la base de datos para el contenido de las noticias
    webScrapper.createDB(database,'content')
    #Insertamos el contenido de las noticias a la base de datos
    for news in urls:
        print (f"retrieved {news} from database")
        webScrapper.writeTextToDB(database,'content',webScrapper.getHtmlText(str(news[1])))

if __name__ == "__main__":
    main()
