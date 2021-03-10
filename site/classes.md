---
layout: post
title:  "Other Classes"
permalink: /classes/
---

# Other Classes

There are also a bunch of other classes defined in the zeit-online package, most of them the return of a *API.get_xxx()* method, and inherently useful to make the representation prettier and easier to extract information

## Excurse on Facetting

As described in the official Documentation, the API supports **facetting** the results. If you specify facetting in a call to the API, for example in *API.search_for(..., facet_time = "1year"), the Response from the server includes a facet field, which is automatically parsed into the Classes of your Response, described here. 

In these Classes, it is possible to use methods to get and set facets, which are the same in every class, so I describe them here.

```python
import zeit 
api = zeit.API()
api.set_token("api-key") #insert your key here

kw = api.get_keyword("angela-merkel", facet_time = "1year") # search for Merkel as a Keyword with a facetting of 1 year
print(kw)
```

Output:

```
Keyword: 'Merkel, Angela' with id 'Angela Merkel' 
, keyword type: 'person' with score 93 and 9358 matches 

matches: [{'subtitle': 'Die Kanzlerin warnt davor, in der Pandemie wieder in alte Rollenmuster zu fallen. Sie fordert: "Frauen müssen endlich so viel verdienen können wie Männer."', 'uuid': '7a1pFhYajBxkeQ02KK8vGY', 'title': 'Merkel fordert Parität in allen gesellschaftlichen Bereichen', 'href': 'http://www.zeit.de/politik/deutschland/2021-03/angela-merkel-video-podcast-frauen-gleichberechtigung-gender-pay-gap', 'release_date': '2021-03-06T11:02:02Z', 'uri': 'http://api.zeit.de/content/7a1pFhYajBxkeQ02KK8vGY', 'supertitle': 'Video-Podcast', 'teaser_text': 'Die Kanzlerin warnt davor, in der Pandemie wieder in alte Rollenmuster zu fallen. Sie fordert: "Frauen müssen endlich so viel verdienen können wie Männer."', 'teaser_title': 'Merkel fordert Parität in allen gesellschaftlichen Bereichen'}]
```

### has_facets()

This function is useful, if you want to find out, if your Instance has facets. It simply returns True, if the ibject has, or False if not

```python
kw.has_facets()
```

Output: 

```
True
```

### get_facets()

If you want to extract the facets, you need this function. It returns a *pandas* TimeSeries with the Time Intervalls as the Index and the number of occurrences in that Intervall as the Values. With that Time Series, you can do a lot of crazy stuff

```python
times = kw.get_facets()
print(times)
```

Outputs:

```
1990-03-09 10:55:48.911000+00:00      5
1991-03-09 10:55:48.911000+00:00      9
1992-03-09 10:55:48.911000+00:00      9
1993-03-09 10:55:48.911000+00:00     10
1994-03-09 10:55:48.911000+00:00      9
1995-03-09 10:55:48.911000+00:00     21
1996-03-09 10:55:48.911000+00:00     11
1997-03-09 10:55:48.911000+00:00     11
1998-03-09 10:55:48.911000+00:00      2
1999-03-09 10:55:48.911000+00:00     23
... 
dtype: int64
```

You could for example take the Series and plot it via pandas builtin plot function.

### set_facets()

This is just for the initialization of the object, to direct ot to extract the facets from the Response. It is used automatically, when you search for something with a facet



## Search

The Search Class is the Result of a *API.search_for("")* operation. It is very useful to better visualize the results via its \__repr__ method. It supports the facetting of its Results, described above.

### Attributes

- *self.name*: The search term of the Search Operation
- *self.found* : The number of results found in the API
- *self.limit:* The limit specified in the call for the search
- *self.matches*: the matches in json format, better use *Search.get_matches()* to extract them

Example 

```python
#example search
s = api.search_for("Bundestag", limit = 2)
print(s)
```

Output:

```
Search for 'Bundestag': 42961 results, limit: 2, matches : 
 
Korruptionsbekämpfer fordern Konsequenzen aus der Maskenaffäre: http://api.zeit.de/content/3Fizoi5qwm86G2afGt00Pw
Die Maskenaffären und ihre Konsequenzen: http://api.zeit.de/content/1G6CjaHX5S01zd2LElisSb
```

It is also possible to extract some attributes about the search, for example if you just want to know about the number of results

```python
s.found
```

Output:

```
42961
```

### get_matches()

This function returns all matches of the search, be it Articles or other things, in the form of a dictionary, with the URIs as keys and a tuple of a description and the json as the values, like {URI: (description, json)}. This makes it easier, to just take the dictionary keys and search for them in a separate call to the API.

```python
s.get_matches() #get the matches
```

```
Output:
{'http://api.zeit.de/content/3Fizoi5qwm86G2afGt00Pw': ('Korruptionsbekämpfer fordern Konsequenzen aus der Maskenaffäre',
  {'subtitle': 'Nach dem Skandal um private Abgeordnetengeschäfte beim Kauf von Corona-Masken mehren sich Rufe 			nach härteren Sanktionsregeln. Die Unionsfraktion plant einen neuen Kodex.',
  'uuid': '3Fizoi5qwm86G2afGt00Pw',
  'title': 'Korruptionsbekämpfer fordern Konsequenzen aus der Maskenaffäre',
  'href': 'http://www.zeit.de/politik/deutschland/2021-03/maskenaffaere-transparency-international-csu-							kritik',
  'release_date': '2021-03-09T06:15:03Z',
  'uri': 'http://api.zeit.de/content/3Fizoi5qwm86G2afGt00Pw',
  'snippet': ' International, Hartmut Bäumer, forderte den <em>Bundestag</em> auf, die Geschäftsordnung zu 					ergänzen, um bestimmte Formen von Lobbyismus zu bestrafen.\nEbenso sollten auch die Fraktionen einen 						"abgestuften',
  'supertitle': 'Maskenaffäre',
  'teaser_text': 'Nach dem Skandal um private Abgeordnetengeschäfte beim Kauf von Corona-Masken mehren sich 				Rufe nach härteren Sanktionsregeln. Die Unionsfraktion plant einen neuen Kodex.',
	'teaser_title': 'Korruptionsbekämpfer fordern Konsequenzen aus der Maskenaffäre'}),
  
  
 'http://api.zeit.de/content/1G6CjaHX5S01zd2LElisSb': ('Die Maskenaffären und ihre Konsequenzen',
   {'subtitle': 'Nikolas Löbel und Georg Nüßlein sollen sich an Maskenverkäufen bereichert haben. Welche 						Konsequenzen drohen der CDU? Und: Der Prozess um den Fall George Floyd beginnt.',
   'uuid': '1G6CjaHX5S01zd2LElisSb',
   'title': 'Die Maskenaffären und ihre Konsequenzen',
   'href': 'http://www.zeit.de/politik/2021-03/masken-affaere-union-korruption-nachrichtenpodcast',
   'release_date': '2021-03-09T04:56:17Z',
   'uri': 'http://api.zeit.de/content/1G6CjaHX5S01zd2LElisSb',
   'snippet': '250.000 Euro – das ist in etwa die Summe, welche die Firma des <em>Bundestagsabgeordneten</em> Nikolas Löbel (CDU) an Provisionen für Geschäfte mit Corona-Schutzmasken erhalten haben soll. Nachdem er die',
   'supertitle': 'Union',
   'teaser_text': 'Nikolas Löbel und Georg Nüßlein sollen sich an Maskenverkäufen bereichert haben. Welche Konsequenzen drohen der Union? Und: Der Prozess um den Fall George Floyd beginnt.',
   'teaser_title': 'Die Maskenaffären und ihre Konsequenzen'})}
```

As you can see, the Output is the two matches with their URIs and JSON.

### get_raw()

This simply returns the raw Response, with which the Object was initiated. Useful, if you want to take a look at it again.

Example: 

```python
s.get_raw()
```

Output:

```
{'matches': [{'subtitle': 'Nach dem Skandal um private Abgeordnetengeschäfte beim Kauf von Corona-Masken mehren sich Rufe nach härteren Sanktionsregeln. Die Unionsfraktion plant einen neuen Kodex.',
   'uuid': '3Fizoi5qwm86G2afGt00Pw',
   'title': 'Korruptionsbekämpfer fordern Konsequenzen aus der Maskenaffäre',
   'href': 'http://www.zeit.de/politik/deutschland/2021-03/maskenaffaere-transparency-international-csu-kritik',
   'release_date': '2021-03-09T06:15:03Z',
   'uri': 'http://api.zeit.de/content/3Fizoi5qwm86G2afGt00Pw',
   'snippet': ' International, Hartmut Bäumer, forderte den <em>Bundestag</em> auf, die Geschäftsordnung zu ergänzen, um bestimmte Formen von Lobbyismus zu bestrafen.\nEbenso sollten auch die Fraktionen einen "abgestuften',
   'supertitle': 'Maskenaffäre', 
   
...
```

And then all the facetting methods, described above

**get_facets()**

**has_facets()**

**set_facets**



## Client

The Client Class is a result of a call to *API.client()*, and is useful, if you want to get more information about your client and your connection to the API. 

### Attributes

- *self.name*: your Name
- *self.email*: your Email
- *self.reset*: the reset time
- *self.api_key*: this is your api key, do not show it to anybody
- *self.requests*: the number of requests you made
- *self.quota* = your quote, normally 10.000

```python
cli = api.client() #get the client class and save it
cli.name
```

Output:

```python
Marten Walk #or your name
```

### requests_left()

This method allows you to get the number of requests left with your client until the reset point. 

```python
cli.requests_left()
```

Output: (specific to my usage)

```
9989
```

### reset_time()

The API returns the time in a complicated ISO8601 string, not very useful. This function converts it to a pandas Timestamp object.

```python
cli.reset_time() #get the time as a timestamp
```

Output:

```
Timestamp('2021-03-08 14:01:30')
```

