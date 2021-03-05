

# Overview over all Classes and methods

## API 

self.base_url = the url of the zeit api
self.token = the current API Key given by the user

### set_token()

### get_status()

### client()



### get(url, limit = 10, seatch = False, time_range = False, fields = False, facet_time = False)



### get_article(article_id)

### get_author(author_id, limit = 1)

### get_keyword(keyword_id, limit = 1, facet_time = False)

### get_department(department_id, limit = 1)



### search_for(search_string, search_type = "content", limit = 10, time_range = False, facet_time = False)



## Article
self.title
self.href
self.text
self.id
self.supertitle
self.uri

### get_keywords()

### get_authors()

### get_date()

### get_raw()



## Client

self.name = your name 
self.email = your email
self.reset = the reset time
self.api_key = your key
self.requests = your requests already made
self.quota = your quote, normally 10.000

### requests_left()

### reset_time()



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
self.matches = the articles
self.found = the number of articles found with the keyword

### get_articles()

### set_facets()

### get_facets()

### has_facets()

### get_raw()



## Department

self.name = the name of the department
self.uri = the Identifier 
self.parent= the parent, if it has one
self.href = the link to the department on Zeit Online
self.found =  the number of articles linked to the department
self.matches = the articles

### get_articles()

### set_facets()

### get_facets()

### has_facets()

### get_raw()

### has_parent()