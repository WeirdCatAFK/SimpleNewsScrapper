import newsSearcher, webScrapper, os


def main():
    database = 'data.db'
    if not os.path.exists(database):
        with open(database,'w') as f:
            pass
    print(f'database {database} created sucessfully')
    
    #Conseguimos los datos de las noticias
    news = newsSearcher.getSearchResults('Ataques Israel')
    #Escribimos los resultados a la base de datos
    newsSearcher.writeResultsToDatabase(database,'searchResults',news)
    #Confirmamos que los datos estan en la base de datos
    urls = newsSearcher.getResultsFromDatabase(database,'searchResults')
    

    #Creamos la base de datos para el contenido de las noticias
    webScrapper.createDB(database,'content')
    #Insertamos las noticias a la base de datos
    for new in news:
        print (f"retrieved {new} from database")
    
    webScrapper.writeTextToDB(database,'content',webScrapper.getHtmlText(str(new[1])))

if __name__ == "__main__":
    main()
