import newsSearcher, webScrapper, os


def main():
    database = 'data.db'
    if not os.path.exists(database):
        with open(database,'w'):
            pass
    print(f'database {database} created successfully')
    
    # Determine our queries
    search_queries = [ ... ]  # Your list of search queries
    
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

