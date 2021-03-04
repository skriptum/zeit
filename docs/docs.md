
## API 
self.base_url = the url of the zeit api, currently [http://api.zeit.de], used because of a possible change in the future
self.token = the current API Key given by the user

### set_token()

### get_status()

### get(url, limit = 10, seatch = False, time_range = False, fields = False, facet_time = False)

### get_article(article_id)

### get_author(author_id, limit = 1)

### get_keyword(keyword_id, limit = 1, facet_time = False)

### search_for(search_string, search_type = "content", limit = 10, time_range = False, facet_time = False)


## Search
self.name = The String searched for
self.found = the number of results found
self.limit = the given limit of results
self.matches = the raw json matches

### get_matches()

### set_facets()

### get_facets()

### has_facets()

### get_raw()

## Keyword
self.name = the name of the keyword
self.uri = the Identifier used for example by get_keyword()
self.lexical = the lexical representation of the keyword
self.score = a internal keyword score of the API, based on frequency
self.type = the type of the Keyword, one of "organization", "person", "location"
self.matches

### get_articles()

### set_facets()

### get_facets()

### has_facets()

### get_raw()

## Article
self.title
self.href
self.text
self.id
self.supertitle

### get_keyowrds

### get_authors

### get_date

### get_raw()