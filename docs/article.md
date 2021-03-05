# Article

The article Class is another central Class of the zeit-online package and allows us to extract a lot of metadate and useful information about an Article. Sadly, Zeit Online does not allow one to get the full Text, just  a teaser text and sometimes a snippet, but we can still get a lot of value from it.

| More Information                              |
| --------------------------------------------- |
| [**Overview**](index.md)                      |
| [**API Documentation**](api.md)               |
| [**Article Documentation**](article.md)       |
| [**Other Classes Documentation**](classes.md) |
| [**complete Documentation**](docs.md)         |

### Initilization

Normally, you get an Article Class as a Return from a *API.get_article(...)* call, but you can also initiate it yourself, altough rather tedious. After Initilization, the Class has a bunch of different Attributes, for example you can get the Name, title etc.

**Attributes**:

- *self.title*: the title of the article
- *self.href*: the link to the article on zeit.de
- *self.text*: the teaser text
- *self.supertitle*: the supertitle associated with the article
- *self.id* : the UUID of the article
- *self.uri*: the Unique Resource Identifier URI of the Article

**Example**

```python
#search for an article
api.search_for("Bundestag", limit=1)
```

Output:

```
Search for 'Bundestag': 42945 results, limit: 1, matches : 
 
CSU-Politiker Nüßlein zieht sich aus der Politik zurück: http://api.zeit.de/content/7zJHkLefQuFQKQMgMx6WXW
```

now we get the article

```python
article = api.get_article("7zJHkLefQuFQKQMgMx6WXW") #get the article we just searched for
print(article)
```

Output: 

```
Article with title 'CSU-Politiker Nüßlein zieht sich aus der Politik zurück' UUID: 7zJHkLefQuFQKQMgMx6WXW, URI: http://api.zeit.de/content/7zJHkLefQuFQKQMgMx6WXW 
teaser_text: 'Nach Korruptionsvorwürfen kandidiert der Unionsfraktionsvize nicht wieder für den Bundestag. Er war in Masken-Geschäfte involviert. Von den Koalitionspartnern kam Kritik.'
```

***

### get_keywords()

this method allows you to extract the keywords from the article. It returns a dictionary of form { uri : name, uri : name ...} to make it easy to extract the keywords by using dictionary.keys() method

**Example**

```python
article.get_keywords() #extract the keywords from the article
```

Output:

```
{'http://api.zeit.de/keyword/csu': 'CSU',
 'http://api.zeit.de/keyword/bundestag': 'Bundestag',
 'http://api.zeit.de/keyword/bundestagswahl': 'Bundestagswahl',
 'http://api.zeit.de/keyword/korruption': 'Korruption',
 'http://api.zeit.de/keyword/staatsanwaltschaft': 'Staatsanwaltschaft'}
```

***

### get_authors()

get the authors who have written the article or contributed . This also returns a dictionary of form {uri:name} for the same reason as above

**Example:**

```python
article.get_authors() #get the authors associated with the article
```

Output:

```
{'http://api.zeit.de/author/Tilman-Steffen': 'Tilman Steffen'}
```

***

### get_date()

The API returns as the release date a ISO time, and to make it easier to extract it, this function exists. It returns a simple Pandas Timestamp

**Example:**

```python
article.get_date()
```

Output:

```
Timestamp('2021-03-05 16:04:47+0000', tz='UTC')
```

## Notebook

Take a look at the article.ipynb notebook to understand it further