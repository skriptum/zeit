#%%
import requests
import json 
import pandas as pd
import datetime

#%%

# helpful functions

def get_content(token, url = "http://api.zeit.de/content", limit = 10, search = False, time_range = False, fields = False, facet_time = False):
        """ function to get content from the api, really broadly defined
        Arguments: 
            url: content endpoint, default = api.zeit.de/content is standard content endpoint
            limit: number results, default : 10
            search: a specific search string
            time-range: expects tuple of two datetime objects, default False
            fields: return specific fields of the repsonse, expects a list
            facetting = the time frame specified, e.g "1year"

        Returns: 
            pure web response in json format
        """
        header = {"X-Authorization":token}

        parameters = {}
        parameters["limit"] = limit

        if search:
            parameters["q"] = search

        if fields:
            parameters["fields"] = f"{*fields,}"
        
        if time_range:
            time1, time2 = time_range[0].isoformat(), time_range[1].isoformat
            parameters["q"] = f'"+search+" AND release_date:[{time1.isoformat()} TO {time2.isoformat()}]'

        if facet_time:
            parameters["facet_date"] = facet_time
        response = requests.get(url, params = parameters, headers = header).json()
        return response


def facetter(response):
    """ takes in the json of a response, returns a time series of the facets""" 

    time_series = pd.Series()
    for a,b in response["facets"]["release_date"].items():
        if type(b) != str:
            date = pd.to_datetime(a)
            count = b
            time_series[date] = count

    time_series = time_series.sort_index()
    return time_series





#%%

#the central API Class
class API():
    def __init__(self):
        self.base_url = "http://api.zeit.de"
        
    
    #general check
    def get_status(self):
        """checks the status of the connection with the api, takes a API-KEY as input
        raises Error when not workin
        """
        header = {"X-Authorization":self.token}
        url = "http://api.zeit.de/client"
        status = requests.get(url, headers = header)

        if status:
            return "everything ok"
        else:
            assert f"something gone wrong, code: {status.status_code}"
    
    #definte the token method
    def set_token(self, api_key):
        """ set the api key, expects key
        raises Error when key is not proper"""
        #check
        check = requests.get(
            "http://api.zeit.de/client", headers = {"X-Authorization":api_key})
        if check:
            self.token = api_key
        else:
            assert "Not a good key"


    #speficif get functions
    def get_article(self, article_id):
        """ function to get an article by ist article id"""
        url = self.base_url + f"/content/{article_id}"
        response = get_content(self.token, url, limit=1)
        return response

    def get_author(self, author_id, limit = 1):
        """ get an author by id, expects a valid author id 
        and optionally a limit on the number of articles"""
        if author_id.startswith("http://"):
            url = author_id
        else:
            url = self.base_url + f"/content/{author_id}"

        response = get_content(self.token, url, limit = limit)
        return response

    def get_keyword(self, keyword_id, limit = 1, facet_time = False):
        """ get information about a keyword, expects keyword id and
        optionally a limit on the number of articles returned"""
        url = self.base_url + f"/keyword/{keyword_id}"

        if facet_time:
            response = get_content(self.token, url, limit = limit, facet_time=facet_time)
            keyword = Keyword(response)
            keyword.set_facets()
        else:
            response = get_content(self.token, url, limit = limit)
            keyword = Keyword(response)

        return keyword


    #search functions 

    def search_for(self, search_string, search_type = "content", limit = 10, time_range = False, facet_time = False):
        """ search the API for a specified string, one word only
            allowed search types = content, keyword, department, author, product author
            allows a time range of the format tuple(time1, time2)
            also allows for facetting by setting a facet_time line '1year' etc.

            returns a Search Class
        """
        string = "*"
        string += search_string
        string += "*"
        url = self.base_url+f"/{search_type}"

        if facet_time:
            response = get_content(self.token, url, limit = limit, search = string, time_range=time_range, facet_time=facet_time)
            search = Search(search_string, response)
            search.set_facets()

        else:
            response = get_content(self.token, url, limit = limit, search = string, time_range=time_range)
            search = Search(search_string, response)

        return search







#%%

#the simple response class
class Search():
    """ class which makes the response of a search prettier and easier to understand"""
    def __init__(self, search_term, response,):
        self.name = search_term
        self.found = response["found"]
        self.limit = response["limit"]
        self.matches = response["matches"]

        self.response = response
    
    def __repr__(self):
        string = f" Search for '{self.name}': {self.found} results, limit: {self.limit}, matches : \n \n"
        for m in self.matches:
            string += f"{m} \n \n"
        
        return string

    def set_facets(self):
        """ add facets to the search, only works if response has facettin activated """
        try:
            ts = facetter(self.response)
            self.time_series = ts
        except:
            raise Exception("no facets in the response")

    def get_facets(self):
        """ get facets of the search, needs set_facets called before
        returns a pandas time series """
        try:
            return self.time_series
        except:
            raise Exception("you forgot to set facets")

    def get_matches(self):
        """ get the matches of the search result , returns a list of dictionarys"""
        return self.matches

    def get_raw(self):
        """ get the pure json of the search"""
        return self.response

    def has_facets(self):
        """function to see if search has facets or not
        True if it has facets, False if not"""
        try:
            self.time_series
            return True
        except:
            return False






# %%

#the keyword class
class Keyword():
    def __init__(self, response):
        """ initialize a keyword instance from a json response""" 
        self.name = response["id"]
        self.uri = response["uri"]
        self.lexical = response["lexical"]
        self.score = response["score"]
        self.type = response["type"]
        self.matches = response["found"]

        #save response for possible later usage
        self.response = response

    def __repr__(self):
        string = f"Keyword: '{self.lexical}' with id '{self.name}',\
        keyword type: '{self.type}' with score {self.score} and {self.matches} matches"
        return string 

    def set_facets(self):
        """ set facets to a keyword, only 
        works if initilization was with facets"""
        try:
            ts = facetter(self.response)
            self.time_series = ts
        except:
            raise Exception("no facets in the response")

    def get_facets(self):
        """ get facets of the keyword, needs set_facets called before """
        try:
            return self.time_series
        except:
            raise Exception("you forgot to set facets")  

    def get_raw(self):
        """ get raw json response of the keyword"""
        return self.response

    def get_articles(self):
        """ get the articles associated with the response,
        only works if there were articles in the initilization
        
        returns a dict of keys : article ids and values : a list of type [title, subtitle, zeitonline link]"""
        articles = {}
        for a in self.response["matches"]:
            id = a["uuid"]
            title = a["title"]
            href = a["href"]
            sub = a["subtitle"]
            articles[id] = [title, sub, href]
        return articles

    def has_facets(self):
        """function to see if keyword has facets or not
        True if it has facets, False if not"""
        try:
            self.time_series
            return True
        except:
            return False

