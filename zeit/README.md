# Zeit Online API in Python

A simple Python Wrapper for the [Zeit Online Content API](http://developer.zeit.de/index/), written in python by Marten Walk. Not official from Zeit Online !

For an overview of the API, view the original [Docs](http://developer.zeit.de/docs/) or try them out in their [explorer](http://developer.zeit.de/explorer/).

For all of this to work, you need an API-Key from their developer team, get one by writing a mail to [api@zeit.de](mailto:api@zeit.de). Be nice and state your intention.

# Documentation

## API 
This is the central class of the API. To use all functions of it, initialize a class and set your API-Key.

```python
#Example Initiliaztion of class
api = zeit.API()
api.set_token("API-Key") # copy your key in here
```

Now you have many different methods at your hands to interact with the API. A simple one is the get_status method to check your client

```python
api.get_status() #returns "everything ok" if it works
```

I would say the most important Method is the search_for method. With it, you can search all endpoints in the API for a specified string.

```python
api.search_for("John Kennedy") # search the default content endpoint for "John Kennedy", returns a search class (explained later)
```

For more Documentation and Examples, visit [the github repo](https://github.com/skriptum/zeit)