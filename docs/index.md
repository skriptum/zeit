# Zeit Online API in Python

A simple Python Wrapper for the [Zeit Online Content API](http://developer.zeit.de/index/), written in python by Marten Walk. Not official from Zeit Online !

For an overview of the API, view the original [Docs](http://developer.zeit.de/docs/) or try them out in their [explorer](http://developer.zeit.de/explorer/).

For all of this to work, you need an API-Key from their developer team, get one by writing a mail to [api@zeit.de](mailto:api@zeit.de). Be nice and state your intention.

Developed by *Marten Walk*, view my [Github-Profile](https://github.com/skriptum) for more info or drop me a mail at [kkx@protonmail.com](mailto:kkx@protonmail.com). 

| More Information                              |
| --------------------------------------------- |
| **Overview**                                  |
| [**API Documentation**](api.md)               |
| [**Article Documentation**](article.md)       |
| [**Other Classes Documentation**](classes.md) |
| [**complete Documentation**](docs.md)         |
| [**Jupyter Example Notebooks**](notebooks.md) |

# Setup

you can install the package with [pip](https://pypi.org/project/pip/) from PYPI, the python package Index.

```bash
pip install zeit-online
```

To import the package into your file just run this simple command

```python
import zeit
```

To get started with interacting with the API, you need to initiate a API-Instance and set your API-Key you got from the developers

```python
api = zeit.API()
api.set_token("API-KEY") #put your key in here
```



# Examples

Now you have many different methods at your hands to interact with the API. Look at the full documentation to see everything.

A simple method is the get_status method to check the status of your connection

```python
api.get_status() #returns "everything ok" if it works
```

I would say the most important Method is the search_for method. With it, you can search all endpoints in the API for a specified string.

```python
api.search_for("Bundestag") # search the default content endpoint for "John Kennedy", returns a search class
```

```
Search for 'Bundestag': 42942 results, limit: 10, matches : 
 
Koalition streicht Begriff "Rasse" aus dem Grundgesetz: http://api.zeit.de/content/1NRyOjRaneKYH6JRs87m46
Bund einigt sich mit AKW-Betreibern auf Entschädigung: http://api.zeit.de/content/5A6U2BpxAaU1YV6Yx9xPY4
"Das Gift ist da": http://api.zeit.de/content/3vrvroDbLrfwJ5VtigrEbh
Die Losbürger: http://api.zeit.de/content/7jM8ZQEFHYM0slSPyL3AN2
"Eine Weigerung hätte schmerzhafte Folgen für die Türkei": http://api.zeit.de/content/7h40VsJ5r2wNJgg6Msld8K
Der nächste Schock nimmt schon Anlauf: http://api.zeit.de/content/j4LDNEBKPGN1vjbOJKpxz
Für Störungen im Bundestag kann künftig Ordnungsgeld verhängt werden: http://api.zeit.de/content/2GOxLhUi8B48g2OziIZPCA
Von Storch und Pazderski wollen gemeinsam Berliner AfD führen: http://api.zeit.de/content/JB8hW8UFGRB9NZyY0TgMM
Bundestag hebt Immunität von CDU-Abgeordnetem Axel Fischer auf: http://api.zeit.de/content/tjB5SFOmwOmzGyZfOpZMq
Bundestag verlängert Rechtsgrundlage für Pandemie-Maßnahmen: http://api.zeit.de/content/3eGseNLQSwHjA3SHwq22hP
```

Obviously, this is specific to today (05.03.2021), but it shows how it works. If we now select the first article and search for it via *get_article()* function, we get an Article Object, with which we can interact in different ways.

```python
Article = api.get_article("1NRyOjRaneKYH6JRs87m46") #you can use the complete uri or just the id
print(Article)
```

```
Article with title 'Koalition streicht Begriff "Rasse" aus dem Grundgesetz' 
UUID: 1NRyOjRaneKYH6JRs87m46, 
URI: http://api.zeit.de/content/1NRyOjRaneKYH6JRs87m46        
teaser_text: 'Die Bundesregierung hat sich auf eine Änderung des Grundgesetzes verständigt: Innen- und Justizministerium einigten sich darauf, wie das Wort "Rasse" ersetzt werden soll.'
```

Now we can access different attributes of the Article Instance and use different methods.

```python
print(Article.supertitle)#print the supertitle of the article instance
print(Article.title) 		#print title
print(Article.text)			#print the teaser text

```

```
Verfassungsänderung
Koalition streicht Begriff "Rasse" aus dem Grundgesetz
Die Bundesregierung hat sich auf eine Änderung des Grundgesetzes verständigt: Innen- und 		Justizministerium einigten sich darauf, wie das Wort "Rasse" ersetzt werden soll.
```

We can also get the keywords of the article with the *get_keywords()* method

```python
Article.get_keywords() #get the keywords linked to the article
```

```
Output:
{'http://api.zeit.de/keyword/grundgesetz': 'Grundgesetz',
 'http://api.zeit.de/keyword/rassismus': 'Rassismus',
 'http://api.zeit.de/keyword/diskriminierung': 'Diskriminierung',
 'http://api.zeit.de/keyword/justizministerium': 'Justizministerium',
 'http://api.zeit.de/keyword/horst-seehofer': 'Horst Seehofer',
 'http://api.zeit.de/keyword/berlin': 'Berlin',
 'http://api.zeit.de/keyword/alexanderplatz': 'Alexanderplatz',
 'http://api.zeit.de/keyword/usa': 'USA',
 'http://api.zeit.de/keyword/bundesregierung': 'Bundesregierung',
 'http://api.zeit.de/keyword/csu': 'CSU',
 'http://api.zeit.de/keyword/bundestag': 'Bundestag'}
```



The zeit package also has many more Classes and methods, you can read about them in the **Further Reading** Section. For example, there is a **Keyword** class to quickly get information about a keyword or the **Search** Class to extract information about a search you made in the API.

# Further reading

The package offers many possibilites, if you want to read further:

More Information about the **API** can be found [here](api.md) , definitely take a look at it to understand more.

More Information about the **Article Class** can be found [here](article.md)

If you want to know about all other Classes, look [here](classes.md)



If there are questions left: contact me at [kkx@protonmail.com](mailto:kkx@protonmail.com)

© made by Marten Walk

 

