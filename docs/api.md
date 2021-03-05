# API

the API is the central class of the zeit-online package. Via it, you interact with the Web-API and have many different methods at hand to get contents of the API

### Initialize and set token

```python
from zeit import API
api = API() # initialize the api
api.set_token("api-key") #set your key here
```

The *set_token()* method of the API is used to authenticate with the API and set your API-Key. You should replace the code snippet with your key. IF this is invalid, it throws an error, so you know if something has gone wrong

---

### get_status()

This is just a simple method that checks whether your connection with the API is good.

```python
api.get_status()
```

Output: (if your status is ok)

```
"everything ok"
```

If something is wrong, it raises an Exception

---

### client()

similar to *get_status*, the *client()* method is used to get the client endpoint from the zeit-api, described [here](http://developer.zeit.de/docs/client/). This function returns a Client object, which is further described in the section **other classes**, but it has some simple methods to help you, for example it shows you how many requests you have left. This method is more useful if you want more information about your Client.

```python
client = api.client()
client.requests_left()
```

Output:

```
9999
```

---

### search_for(search_string, search_type = "content", limit = 10, time_range = False, facet_time = False)

This is the most important method of the API, it allows you to easily search for something and get some matches. It works by specifying a search string and a search_type, which is a endpoint of the api, e.g *"content"*, *"keyword"*, *"author"*, etc. It allows you to limit the number of matches and filter by a certain time range (specified by a tuple of two *datetime* objects) or facet your results, as explained in the original [documentation](http://developer.zeit.de/docs/)

**Arguments**:

- *search_string*: a string specifying which word or words you want to search for, e.g "Angela Merkel"
- *search_type*: a valid API Endpoint, e.g *"content"*, *"keyword"*, *"author"*, etc
- *limit*: the limit on the number of matches you want
- *time_range*: a tuple of two *datetime* or *pandas.Timestamp* objects, the one farer in the past first
- *facet_time*: if you want to facet the results with time, input here a valid time string like *"1year"* , *"3day"* or *"2month"* or a combination of it

This method returns a **Search** Object, more information in the section **Other Classes**

**Examples**

simple search

```python
#search all articles for Angela Merkel, limit the results to 1 and facet it by 1 year
api.search_for("Angela Merkel", limit=1)  
```

Output:

```
Search for 'Angela Merkel': 16491 results, limit: 1, matches : 
 
"Von den Schnelltests sind mehr als genug da": http://api.zeit.de/content/5OmCP26nAXSKQEWM2sPf8b
```

search in keywords

```python
#search for keywords containing "Angela Merkel"
api.search_for("Angela Merkel", "keyword")
```

Output:

```
Search for 'Angela Merkel': 2 results, limit: 10, matches : 
 
Angela Merkel: http://api.zeit.de/keyword/angela-merkels
Angela Merkel: http://api.zeit.de/keyword/angela-merkel
```

for more information, see the possible endpoints in the official documentation and the **Search** Class

---

### get_article(article_id)

This searches the *Content* Endpoint by ID and returns a **Article** Class, which is closer described in section Article. 

**Arguments**:

- *article_id*: the UUID of an article or its URI to search for

**Example**

```python
#lets reuse the search for Angela Merkel
api.get_article("5OmCP26nAXSKQEWM2sPf8b") #search by UUID, URI also possible
```

Output:

```
Article with title '"Von den Schnelltests sind mehr als genug da"' UUID: 5OmCP26nAXSKQEWM2sPf8b, URI: http://api.zeit.de/content/5OmCP26nAXSKQEWM2sPf8b            teaser_text: 'Bundesgesundheitsminister Jens Spahn hat die Corona-Strategie von Bund und Ländern verteidigt. Keine Öffnungsschritte zu wagen sei kaum verantwortbar gewesen.'
```

---

### get_keyword(keyword_id, limit = 1, facet_time = False)

This method is used to get a keyword from the *Keyword* Endpoint. It allows facetting to analyze the usage of a keyword over time and returns a **Keyword** Class, further defined in **Other classes**. If facetting is activated, this opens many possbilities, read more about it there

**Arguments**:

- *keyword_id*: a valid keyword like 'angela-merkel' or a URI of a keyword 
- *limit*: limits the articles linked to the keyword, default 1
- *facet_time*: facette the articles as described in the *search_for(...)* method;  input here a valid time string like *"1year"* , *"3day"* or *"2month"* or a combination of it

**Example**

```python
api.get_keyword("angela-merkel")
```

Output:

```
Keyword: 'Merkel, Angela' with id 'Angela Merkel' 
,keyword type: 'person' with score 93 and 9357 matches 

matches: [{'subtitle': 'Einer Umfrage von Infratest dimap zufolge liegen die Grünen kurz vor der Landtagswahl deutlich vor der CDU. Die Linke muss um den Einzug in den Landtag bangen.', 'uuid': '7KuHcKTSXn5IOZvQLYnpLM', 'title': 'Grüne mit acht Punkten Vorsprung derzeit stärkste Kraft', 'href': 'http://www.zeit.de/politik/deutschland/2021-03/baden-wuerttemberg-winfried-kretschmann-gruene-cdu-landtagswahl-infratest-dimap-umfrage', 'release_date': '2021-03-04T18:31:32Z', 'uri': 'http://api.zeit.de/content/7KuHcKTSXn5IOZvQLYnpLM', 'supertitle': 'Baden-Württemberg', 'teaser_text': 'Einer Umfrage von Infratest dimap zufolge liegen die Grünen kurz vor der Landtagswahl deutlich vor der CDU. Die Linke muss um den Einzug in den Landtag bangen.', 'teaser_title': 'Grüne mit acht Punkten Vorsprung derzeit stärkste Kraft'}]
```

---

### get_department(department_id, limit = 1)

get a department of the Zeit-Verlag, e.g Politik or Ausland. Returns a **Department** Object, further described in **Other Classes**

**Arguments:**

- *department_id*: the id of a department, can either be a URI or the ID.
- *limit* : limit the number of articles shown, default 1

**Example**

```python
#get the politik department
api.get_department("politik")
```

Output:

```
Department Politik 
 Articles: 35170; 
 uri:http://api.zeit.de/department/politik 
 no parent
```

---

### get_author(author_id, limit = 1)

This searches the *Author* Endpoint by ID or possibly the URI of the Author, returns the JSON given by the endpoint as described [here](http://developer.zeit.de/docs/author#by-id) 

**Arguments**:

- author_id*: the UUID of an author or its URI to search for

**Example**

```python
api.get_author("-Josef-Joffe", limit = 1)
```

Output:

```
{'matches': [{'subtitle': 'Ein etwas anderer Jahresrückblick: Es wurde immer schlimmer in diesem Jahr, weshalb die Habenseite der Bilanz zu feiern ist.',
   'uuid': '1WExS9cVBz0XM0yT9FkwmA',
   'title': 'Die Lage ist hoffnungslos, aber nicht ernst',
   'href': 'http://www.zeit.de/politik/2020-12/2020-jahresrueckblick-coronavirus-donald-trump-klimakrise',
   'release_date': '2020-12-30T12:36:43Z',
   'uri': 'http://api.zeit.de/content/1WExS9cVBz0XM0yT9FkwmA',
   'supertitle': '2020',
   'teaser_text': 'Ein etwas anderer Jahresrückblick: Es wurde immer schlimmer in diesem Jahr, weshalb die Habenseite der Bilanz zu feiern ist.',
   'teaser_title': 'Die Lage ist hoffnungslos, aber nicht ernst'}],
 'uri': 'http://api.zeit.de/author/-Josef-Joffe',
 'value': ' Josef Joffe',
 'href': '',
 'limit': 1,
 'offset': 0,
 'found': 1141,
 'type': 'author',
 'id': '-Josef-Joffe'}
```

---

### get(url = "http://api.zeit.de/content",  limit = 10,  search = False,  time_range = False, fields = False, facet_time = False)

the *get(...)* method is used to communicate with the API similar to a HTTP GET, but already preconfigured. 

**Argumemts**:

- *url*: the endpoint with which the api should communicate, default is the content endpoint
- *limit*: the limit on the number of matches shown in the response, default 10
- *search*: the string to search for, similiar to *q* in REST-APIs, default False
- *time_range*: expects a time_range in the form of a tuple of two *datetime* or *pandas.Timestamp* Instances
- *fields* : if you want the response just to contain certain fields
- *facet_time* : if you want to facet the results with time, input here a valid time string like *"1year"* , *"3day"* or *"2month"* or a combination of it

**Examples**

```python
api.get(url = "http://api.zeit.de/content", limit = 1, search = "Bundestag") # search for bundestag in the content endpoint and limit the results to 1
```

Output: 

```
{'matches': [{'subtitle': 'Der Unionsfraktionsvize kandidiert nicht erneut für den Bundestag. Die Staatsanwaltschaft durchsuchte jüngst sein Bundestagsbüro – er war in Masken-Geschäfte involviert.',
   'uuid': '7zJHkLefQuFQKQMgMx6WXW',
   'title': 'CSU-Politiker Nüßlein zieht sich aus der Politik zurück',
   'href': 'http://www.zeit.de/politik/deutschland/2021-03/georg-nuesslein-csu-bundestag-politik-masken-affaere-korruption',
   'release_date': '2021-03-05T16:04:47Z',
   'uri': 'http://api.zeit.de/content/7zJHkLefQuFQKQMgMx6WXW',
   'snippet': ' Rechtsanwalt mitteilte, wird er sein ruhendes Amt als stellvertretender Vorsitzender der Unionsfraktion im <em>Bundestag</em> niederlegen. Bei der Bundestagswahl im September will er nicht mehr kandidieren.\nDie',
   'supertitle': 'Corona-Maskenbeschaffung',
   'teaser_text': 'Der Unionsfraktionsvize kandidiert nicht erneut für den Bundestag. Die Staatsanwaltschaft durchsuchte jüngst sein Bundestagsbüro – er war in Masken-Geschäfte involviert.',
   'teaser_title': 'CSU-Politiker Nüßlein zieht sich aus der Politik zurück'}],
 'found': 22262,
 'limit': 1,
 'offset': 0}
```

As you can see, this output is very raw, and therefore there are other methods to search for something in the API

## Notebook

Take a look at the notebook api.ipynb to understand it further