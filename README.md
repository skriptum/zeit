# Zeit Online API in Python

A simple Python Wrapper for the [Zeit Online Content API](http://developer.zeit.de/index/), written in python by Marten Walk. Not official from Zeit Online !

For an overview of the API, view the original [Docs](http://developer.zeit.de/docs/) or try them out in their [explorer](http://developer.zeit.de/explorer/).

For all of this to work, you need an API-Key from their developer team, get one by writing a mail to [api@zeit.de](mailto:api@zeit.de). Be nice and state your intention.

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
api = API()
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
api.search_for("John Kennedy") # search the default content endpoint for "John Kennedy", returns a search class
```

For more documentation, look at the docs and the example Notebook

©made by Marten Walk

 